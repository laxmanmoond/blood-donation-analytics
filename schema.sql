-- ============================================================
-- Blood Donation Analytics & Donor Intelligence Platform
-- schema.sql  —  Full MySQL database schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS blood_donation_analytics
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE blood_donation_analytics;

-- ─────────────────────────────────────────────
-- Drop tables in correct FK order
-- ─────────────────────────────────────────────
DROP TABLE IF EXISTS donation_records;
DROP TABLE IF EXISTS blood_requests;
DROP TABLE IF EXISTS donors;

-- ─────────────────────────────────────────────
-- TABLE 1: donors
-- ─────────────────────────────────────────────
CREATE TABLE donors (
    donor_id            VARCHAR(10)      NOT NULL,
    name                VARCHAR(100)     NOT NULL,
    age                 TINYINT UNSIGNED NOT NULL,
    gender              ENUM('Male','Female','Other','Unknown') NOT NULL DEFAULT 'Unknown',
    blood_group         ENUM('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL,
    city                VARCHAR(60)      NOT NULL,
    state               VARCHAR(60)      NOT NULL,
    last_donation_date  DATE             NULL,
    availability_status ENUM('Available','Unavailable') NOT NULL DEFAULT 'Available',
    latitude            DECIMAL(9,6)     NOT NULL,
    longitude           DECIMAL(9,6)     NOT NULL,
    created_at          TIMESTAMP        DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (donor_id),
    INDEX idx_blood_group        (blood_group),
    INDEX idx_city               (city),
    INDEX idx_state              (state),
    INDEX idx_availability       (availability_status),
    INDEX idx_last_donation_date (last_donation_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─────────────────────────────────────────────
-- TABLE 2: blood_requests
-- ─────────────────────────────────────────────
CREATE TABLE blood_requests (
    request_id      VARCHAR(10)      NOT NULL,
    hospital_name   VARCHAR(120)     NOT NULL,
    blood_group     ENUM('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL,
    units_required  TINYINT UNSIGNED NOT NULL,
    urgency_level   ENUM('Critical','High','Medium','Low') NOT NULL DEFAULT 'Medium',
    city            VARCHAR(60)      NOT NULL,
    request_date    DATE             NOT NULL,
    created_at      TIMESTAMP        DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (request_id),
    INDEX idx_req_blood_group (blood_group),
    INDEX idx_req_urgency     (urgency_level),
    INDEX idx_req_city        (city),
    INDEX idx_req_date        (request_date),
    INDEX idx_req_hospital    (hospital_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─────────────────────────────────────────────
-- TABLE 3: donation_records
-- ─────────────────────────────────────────────
CREATE TABLE donation_records (
    donation_id     VARCHAR(12)      NOT NULL,
    donor_id        VARCHAR(10)      NOT NULL,
    hospital_name   VARCHAR(120)     NOT NULL,
    blood_group     ENUM('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL,
    donation_date   DATE             NOT NULL,
    units_donated   TINYINT UNSIGNED NOT NULL,
    created_at      TIMESTAMP        DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (donation_id),
    FOREIGN KEY (donor_id) REFERENCES donors(donor_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_don_donor_id    (donor_id),
    INDEX idx_don_blood_group (blood_group),
    INDEX idx_don_date        (donation_date),
    INDEX idx_don_hospital    (hospital_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─────────────────────────────────────────────
-- VIEWS
-- ─────────────────────────────────────────────
CREATE OR REPLACE VIEW vw_dataset_overview AS
    SELECT 'donors'           AS table_name, COUNT(*) AS row_count FROM donors
    UNION ALL
    SELECT 'blood_requests',                 COUNT(*) FROM blood_requests
    UNION ALL
    SELECT 'donation_records',               COUNT(*) FROM donation_records;

CREATE OR REPLACE VIEW vw_donor_availability AS
    SELECT
        blood_group,
        COUNT(*)                                                          AS total_donors,
        SUM(availability_status = 'Available')                            AS available,
        SUM(availability_status = 'Unavailable')                          AS unavailable,
        ROUND(SUM(availability_status = 'Available') / COUNT(*) * 100, 1) AS availability_pct
    FROM donors
    GROUP BY blood_group
    ORDER BY total_donors DESC;

CREATE OR REPLACE VIEW vw_blood_demand AS
    SELECT
        blood_group,
        COUNT(*)                          AS total_requests,
        SUM(units_required)               AS total_units_demanded,
        ROUND(AVG(units_required), 2)     AS avg_units_per_request,
        SUM(urgency_level = 'Critical')   AS critical_requests
    FROM blood_requests
    GROUP BY blood_group
    ORDER BY total_units_demanded DESC;

CREATE OR REPLACE VIEW vw_donation_summary AS
    SELECT
        blood_group,
        COUNT(*)                          AS total_donations,
        SUM(units_donated)                AS total_units_donated,
        ROUND(AVG(units_donated), 2)      AS avg_units_per_donation,
        COUNT(DISTINCT donor_id)          AS unique_donors
    FROM donation_records
    GROUP BY blood_group
    ORDER BY total_units_donated DESC;

-- ─────────────────────────────────────────────
-- STORED PROCEDURE: find available donors
-- ─────────────────────────────────────────────
DROP PROCEDURE IF EXISTS sp_find_available_donors;

DELIMITER $$
CREATE PROCEDURE sp_find_available_donors(
    IN p_blood_group VARCHAR(5),
    IN p_city        VARCHAR(60)
)
BEGIN
    SELECT
        d.donor_id,
        d.name,
        d.age,
        d.gender,
        d.blood_group,
        d.city,
        d.last_donation_date,
        DATEDIFF(CURDATE(), d.last_donation_date) AS days_since_last_donation
    FROM donors d
    WHERE d.blood_group         = p_blood_group
      AND d.city                = p_city
      AND d.availability_status = 'Available'
    ORDER BY d.last_donation_date ASC;
END$$
DELIMITER ;

-- ─────────────────────────────────────────────
-- DATA LOAD TEMPLATE (update path before running)
-- ─────────────────────────────────────────────
/*
SET GLOBAL local_infile = 1;

LOAD DATA LOCAL INFILE '/absolute/path/data/cleaned/donors_clean.csv'
INTO TABLE donors
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES  TERMINATED BY '\n'
IGNORE 1 ROWS
(donor_id, name, age, gender, blood_group, city, state,
 @last_donation_date, availability_status, latitude, longitude)
SET last_donation_date = NULLIF(@last_donation_date, '');

LOAD DATA LOCAL INFILE '/absolute/path/data/cleaned/blood_requests_clean.csv'
INTO TABLE blood_requests
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES  TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE '/absolute/path/data/cleaned/donation_records_clean.csv'
INTO TABLE donation_records
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES  TERMINATED BY '\n'
IGNORE 1 ROWS;
*/
