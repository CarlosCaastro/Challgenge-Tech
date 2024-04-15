CREATE TABLE IF NOT EXISTS equipment (
    equipment_id INT PRIMARY KEY,
    name VARCHAR(255),
    group_name VARCHAR(255),
    load_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);