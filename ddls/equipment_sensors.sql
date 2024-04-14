CREATE TABLE IF NOT EXISTS equipment_sensors (
    equipment_id INT,
    sensor_id INT,
    load_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (equipment_id, sensor_id),
    FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id)
);