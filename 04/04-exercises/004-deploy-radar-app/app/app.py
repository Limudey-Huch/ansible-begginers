#!/usr/bin/env python3
"""Radar API — serves the current aircraft snapshot from Postgres.
The poller (poller.py, run on a timer) is what actually keeps this data fresh;
this process only ever reads."""
import os
import psycopg2
import psycopg2.extras
from flask import Flask, jsonify, abort

DB_HOST = os.environ["RADAR_DB_HOST"]
DB_NAME = os.environ.get("RADAR_DB_NAME", "radar")
DB_USER = os.environ.get("RADAR_DB_USER", "radar")
DB_PASSWORD = os.environ["RADAR_DB_PASSWORD"]

app = Flask(__name__)


def get_conn():
    return psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/aircraft")
def list_aircraft():
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                "SELECT icao24, callsign, lat, lon, baro_altitude, velocity, true_track, updated_at "
                "FROM aircraft ORDER BY updated_at DESC"
            )
            rows = cur.fetchall()
    finally:
        conn.close()
    return jsonify(rows)


@app.get("/api/aircraft/<icao24>")
def aircraft_detail(icao24):
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                "SELECT icao24, callsign, lat, lon, baro_altitude, velocity, true_track, last_contact, updated_at "
                "FROM aircraft WHERE icao24 = %s",
                (icao24,),
            )
            row = cur.fetchone()
    finally:
        conn.close()
    if row is None:
        abort(404)
    return jsonify(row)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
