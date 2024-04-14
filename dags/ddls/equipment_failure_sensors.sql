CREATE TABLE IF NOT EXISTS equipment_failure_sensors (
    item TEXT,
    timestamp TEXT,
    log_level TEXT,
    sensor_id INT,
    temperature FLOAT,
    vibration FLOAT,
    load_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);