#!/usr/bin/env python3
"""Simulates aircraft moving on the radar and writes their state to Postgres.
Run on a timer (see radar-poller.service/.timer) — not a long-running daemon.

This replaced an earlier version that polled the real OpenSky Network API.
OpenSky (and similar free flight-tracking APIs) block anonymous requests from
AWS/cloud IP ranges, so that version worked from a laptop but not from the
app tier itself. A simulator has no such problem — and gives clearly visible
motion between polls, which real (slow-moving, 15s-apart) data mostly didn't."""
import math
import os
import random
import time
import psycopg2
import psycopg2.extras

CENTER_LAT = float(os.environ.get("RADAR_CENTER_LAT", "59.5"))
CENTER_LON = float(os.environ.get("RADAR_CENTER_LON", "18.0"))
MAX_RANGE_KM = float(os.environ.get("RADAR_RANGE_KM", "150"))
MAX_AIRCRAFT = int(os.environ.get("RADAR_MAX_AIRCRAFT", "10"))
TICK_SECONDS = int(os.environ.get("RADAR_TICK_SECONDS", "5"))
# Displayed speed in the info panel stays realistic; this only scales how far the
# blip actually moves each tick, so motion is obvious on a human timescale instead
# of real (barely-perceptible-per-poll) aircraft speed.
SPEED_MULTIPLIER = float(os.environ.get("RADAR_SPEED_MULTIPLIER", "12"))
EARTH_RADIUS_KM = 6371

DB_HOST = os.environ["RADAR_DB_HOST"]
DB_NAME = os.environ.get("RADAR_DB_NAME", "radar")
DB_USER = os.environ.get("RADAR_DB_USER", "radar")
DB_PASSWORD = os.environ["RADAR_DB_PASSWORD"]

CALLSIGN_PREFIXES = ["BAW", "KLM", "DLH", "SAS", "AFR", "UAE", "RYR", "EZY", "FIN", "NAX"]


def rand_icao24():
    return "".join(random.choice("0123456789abcdef") for _ in range(6))


def rand_callsign():
    return random.choice(CALLSIGN_PREFIXES) + str(random.randint(100, 999))


def destination_point(lat, lon, bearing_deg, distance_km):
    """Given a start point, bearing, and distance, compute the destination point."""
    d_r = distance_km / EARTH_RADIUS_KM
    brng = math.radians(bearing_deg)
    lat1, lon1 = math.radians(lat), math.radians(lon)

    lat2 = math.asin(math.sin(lat1) * math.cos(d_r) + math.cos(lat1) * math.sin(d_r) * math.cos(brng))
    lon2 = lon1 + math.atan2(
        math.sin(brng) * math.sin(d_r) * math.cos(lat1),
        math.cos(d_r) - math.sin(lat1) * math.sin(lat2),
    )
    return math.degrees(lat2), math.degrees(lon2)


def distance_km(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return EARTH_RADIUS_KM * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def spawn_aircraft():
    """A new aircraft entering from a random point on the edge of the range,
    heading generally toward the center so it flies into view, not away."""
    edge_bearing = random.uniform(0, 360)
    lat, lon = destination_point(CENTER_LAT, CENTER_LON, edge_bearing, MAX_RANGE_KM * 0.95)
    heading_toward_center = (edge_bearing + 180) % 360
    heading = (heading_toward_center + random.uniform(-50, 50)) % 360
    return {
        "icao24": rand_icao24(),
        "callsign": rand_callsign(),
        "lat": lat,
        "lon": lon,
        "baro_altitude": random.uniform(3000, 11000),
        "velocity": random.uniform(150, 260),  # m/s
        "true_track": heading,
    }


def step(ac):
    """Move one aircraft forward by one tick, with a little random heading drift."""
    heading = (ac["true_track"] + random.uniform(-6, 6)) % 360
    dist_km = (ac["velocity"] * SPEED_MULTIPLIER * TICK_SECONDS) / 1000.0
    lat, lon = destination_point(ac["lat"], ac["lon"], heading, dist_km)
    altitude = max(500, ac["baro_altitude"] + random.uniform(-40, 40))
    return {**ac, "lat": lat, "lon": lon, "true_track": heading, "baro_altitude": altitude}


def main():
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    try:
        with conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM aircraft")
            current = cur.fetchall()

            alive = []
            for ac in current:
                moved = step(dict(ac))
                if distance_km(moved["lat"], moved["lon"], CENTER_LAT, CENTER_LON) > MAX_RANGE_KM:
                    continue  # flew out of range — leave it out, it disappears from the radar
                alive.append(moved)

            while len(alive) < MAX_AIRCRAFT:
                alive.append(spawn_aircraft())

            cur.execute("DELETE FROM aircraft")  # simplest way to drop the ones that left
            now = int(time.time())
            for ac in alive:
                cur.execute(
                    """
                    INSERT INTO aircraft
                        (icao24, callsign, lat, lon, baro_altitude, velocity, true_track, last_contact, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())
                    """,
                    (ac["icao24"], ac["callsign"], ac["lat"], ac["lon"],
                     ac["baro_altitude"], ac["velocity"], ac["true_track"], now),
                )
            print(f"Simulated tick: {len(current)} -> {len(alive)} aircraft")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
