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