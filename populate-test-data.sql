DROP TABLE TRACKING_DATA;

CREATE TABLE TRACKING_DATA (
            -- incrementing, starts at zero, example: 12
            id INTEGER PRIMARY KEY,
            -- YYYY-MM-DD, example: 2025-02-01
            date DATETIME,
            -- Kilometers, example: 12.01
            distance REAL,
            -- Number of steps, example: 3215
            steps INTEGER,
            -- Calory estimation, example: 147.35
            calories REAL,
            -- Km/h, example: 3.47
            avgspeed REAL
        );

INSERT INTO TRACKING_DATA (id, date, distance, steps, calories, avgspeed)
VALUES
(1, '2025-02-01', 22.40, 6000, 250.60, 4.80),
(2, '2025-02-02', 15.50, 4200, 200.50, 4.10),
(3, '2025-02-03', 10.25, 2800, 120.25, 6.70),
(4, '2025-02-04', 18.75, 5000, 220.75, 4.30),
(5, '2025-02-05', 12.40, 6000, 125.60, 5.80);
