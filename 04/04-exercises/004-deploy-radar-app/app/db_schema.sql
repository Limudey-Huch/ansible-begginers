CREATE TABLE IF NOT EXISTS aircraft (
    icao24       VARCHAR(16) PRIMARY KEY,
    callsign     VARCHAR(16),
    lat          DOUBLE PRECISION,
    lon          DOUBLE PRECISION,
    baro_altitude DOUBLE PRECISION,
    velocity     DOUBLE PRECISION,
    true_track   DOUBLE PRECISION,
    last_contact BIGINT,
    updated_at   TIMESTAMP NOT NULL DEFAULT now()
);

-- The table above is created as the postgres superuser (via become_user: postgres),
-- so the app's own "radar" role has no privileges on it by default — hand it over.
ALTER TABLE aircraft OWNER TO radar;
