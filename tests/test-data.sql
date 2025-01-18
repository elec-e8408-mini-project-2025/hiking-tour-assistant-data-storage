-- If the table does not yet exist, this creates it
CREATE TABLE IF NOT EXISTS TRACKING_DATA (
    id INTEGER PRIMARY KEY,
    date DATETIME,
    name TEXT,
    distance REAL,
    steps INTEGER,
    calories REAL
);

-- Insert test data entries
INSERT INTO TRACKING_DATA (date, name, distance, steps, calories) VALUES
('2024-12-31 10:00:12', 'Töölön lahti', 3500.50, 4500, 202.11),
('2025-01-02 12:30:00', 'Espan ranta', 2800.23, 3500, 181.67),
('2025-01-03 08:15:00', 'Otaniemen lenkki', 5000.15, 6000, 303.12),
('2025-01-04 09:00:45', 'Westendin ranta', 4200.17, 5000, 248.56);