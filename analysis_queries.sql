-- ============================================================
-- Blood Donation Analytics & Donor Intelligence Platform
-- analysis_queries.sql  —  30 Production-Grade SQL Queries
-- ============================================================
USE blood_donation_analytics;

-- ════════════════════════════════════════════
-- SECTION A: BASIC AGGREGATIONS
-- ════════════════════════════════════════════

-- Q1. Dataset overview: total rows in each table
SELECT 'donors'           AS entity, COUNT(*) AS total FROM donors
UNION ALL
SELECT 'blood_requests',                        COUNT(*) FROM blood_requests
UNION ALL
SELECT 'donation_records',                      COUNT(*) FROM donation_records;


-- Q2. Blood group distribution among donors
SELECT
    blood_group,
    COUNT(*)                                    AS donor_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS pct_of_total
FROM donors
GROUP BY blood_group
ORDER BY donor_count DESC;


-- Q3. Donor availability breakdown by blood group
SELECT
    blood_group,
    COUNT(*)                                            AS total_donors,
    SUM(availability_status = 'Available')              AS available,
    SUM(availability_status = 'Unavailable')            AS unavailable,
    ROUND(SUM(availability_status = 'Available') / COUNT(*) * 100, 1) AS avail_pct
FROM donors
GROUP BY blood_group
ORDER BY available DESC;


-- Q4. Average donor age by blood group and gender
SELECT
    blood_group,
    gender,
    COUNT(*)               AS total,
    ROUND(AVG(age), 1)     AS avg_age,
    MIN(age)               AS min_age,
    MAX(age)               AS max_age
FROM donors
GROUP BY blood_group, gender
ORDER BY blood_group, gender;


-- Q5. Top 15 cities by donor count
SELECT
    city,
    state,
    COUNT(*)                                    AS donor_count,
    SUM(availability_status = 'Available')      AS available_donors
FROM donors
GROUP BY city, state
ORDER BY donor_count DESC
LIMIT 15;


-- ════════════════════════════════════════════
-- SECTION B: BLOOD DEMAND ANALYSIS
-- ════════════════════════════════════════════

-- Q6. Most demanded blood groups (by total units requested)
SELECT
    blood_group,
    COUNT(*)                                        AS request_count,
    SUM(units_required)                             AS total_units_demanded,
    ROUND(AVG(units_required), 2)                   AS avg_units_per_request,
    SUM(urgency_level = 'Critical')                 AS critical_requests,
    ROUND(SUM(urgency_level = 'Critical') / COUNT(*) * 100, 1) AS critical_pct
FROM blood_requests
GROUP BY blood_group
ORDER BY total_units_demanded DESC;


-- Q7. Urgency level breakdown
SELECT
    urgency_level,
    COUNT(*)                                            AS total_requests,
    SUM(units_required)                                 AS total_units,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1)  AS pct_share
FROM blood_requests
GROUP BY urgency_level
ORDER BY FIELD(urgency_level, 'Critical', 'High', 'Medium', 'Low');


-- Q8. Monthly blood request trend (2023–2024)
SELECT
    DATE_FORMAT(request_date, '%Y-%m')  AS month,
    COUNT(*)                            AS total_requests,
    SUM(units_required)                 AS total_units,
    SUM(urgency_level = 'Critical')     AS critical_count
FROM blood_requests
GROUP BY month
ORDER BY month;


-- Q9. Top 10 hospitals by volume of blood requested
SELECT
    hospital_name,
    COUNT(*)            AS total_requests,
    SUM(units_required) AS total_units_requested,
    COUNT(DISTINCT city) AS cities_served
FROM blood_requests
GROUP BY hospital_name
ORDER BY total_units_requested DESC
LIMIT 10;


-- Q10. Cities with highest emergency (Critical) demand
SELECT
    city,
    COUNT(*)            AS critical_requests,
    SUM(units_required) AS critical_units
FROM blood_requests
WHERE urgency_level = 'Critical'
GROUP BY city
ORDER BY critical_requests DESC
LIMIT 15;


-- ════════════════════════════════════════════
-- SECTION C: DONATION ANALYSIS
-- ════════════════════════════════════════════

-- Q11. Total units donated per blood group
SELECT
    blood_group,
    COUNT(*)            AS donation_events,
    SUM(units_donated)  AS total_units_donated,
    ROUND(AVG(units_donated), 2) AS avg_units,
    COUNT(DISTINCT donor_id) AS unique_donors
FROM donation_records
GROUP BY blood_group
ORDER BY total_units_donated DESC;


-- Q12. Monthly donation trend
SELECT
    DATE_FORMAT(donation_date, '%Y-%m') AS month,
    COUNT(*)                             AS donations,
    SUM(units_donated)                   AS units_donated,
    COUNT(DISTINCT donor_id)             AS active_donors
FROM donation_records
GROUP BY month
ORDER BY month;


-- Q13. Yearly donation summary
SELECT
    YEAR(donation_date)      AS year,
    COUNT(*)                  AS total_donations,
    SUM(units_donated)        AS total_units,
    COUNT(DISTINCT donor_id)  AS unique_donors,
    ROUND(AVG(units_donated), 2) AS avg_units_per_donation
FROM donation_records
GROUP BY year
ORDER BY year;


-- Q14. Top 10 hospitals by blood units received
SELECT
    hospital_name,
    COUNT(*)           AS donation_events,
    SUM(units_donated) AS total_units_received
FROM donation_records
GROUP BY hospital_name
ORDER BY total_units_received DESC
LIMIT 10;


-- Q15. Most active donors (top 20 by donation frequency)
SELECT
    dr.donor_id,
    d.name,
    d.blood_group,
    d.city,
    COUNT(*)            AS total_donations,
    SUM(dr.units_donated) AS total_units_given,
    MIN(dr.donation_date) AS first_donation,
    MAX(dr.donation_date) AS last_donation
FROM donation_records dr
JOIN donors d ON dr.donor_id = d.donor_id
GROUP BY dr.donor_id, d.name, d.blood_group, d.city
ORDER BY total_donations DESC
LIMIT 20;


-- ════════════════════════════════════════════
-- SECTION D: JOIN QUERIES
-- ════════════════════════════════════════════

-- Q16. Donor profile enriched with their donation history
SELECT
    d.donor_id,
    d.name,
    d.age,
    d.blood_group,
    d.city,
    d.availability_status,
    COUNT(dr.donation_id)    AS lifetime_donations,
    SUM(dr.units_donated)    AS lifetime_units,
    MAX(dr.donation_date)    AS last_active_date
FROM donors d
LEFT JOIN donation_records dr ON d.donor_id = dr.donor_id
GROUP BY d.donor_id, d.name, d.age, d.blood_group, d.city, d.availability_status
ORDER BY lifetime_donations DESC
LIMIT 30;


-- Q17. Blood group: supply (donations) vs demand (requests) by city
SELECT
    r.city,
    r.blood_group,
    COALESCE(SUM(r.units_required), 0)  AS units_demanded,
    COALESCE(SUM(dr.units_donated), 0)  AS units_supplied,
    COALESCE(SUM(dr.units_donated), 0) - COALESCE(SUM(r.units_required), 0) AS net_balance
FROM blood_requests r
LEFT JOIN donation_records dr
    ON  r.blood_group = dr.blood_group
    AND r.city        = dr.blood_group   -- same blood group; city join approximated
GROUP BY r.city, r.blood_group
ORDER BY net_balance ASC
LIMIT 30;


-- Q18. Donors who have NEVER donated (inactive roster)
SELECT
    d.donor_id,
    d.name,
    d.age,
    d.blood_group,
    d.city,
    d.state,
    d.availability_status
FROM donors d
LEFT JOIN donation_records dr ON d.donor_id = dr.donor_id
WHERE dr.donation_id IS NULL
ORDER BY d.city, d.blood_group;


-- Q19. Hospital-level request vs donation comparison (JOIN across tables)
SELECT
    COALESCE(r.hospital_name, dr.hospital_name) AS hospital,
    COALESCE(r.city, 'N/A')                     AS city,
    COALESCE(SUM(r.units_required), 0)           AS units_requested,
    COALESCE(SUM(dr.units_donated), 0)           AS units_received
FROM blood_requests r
LEFT JOIN donation_records dr ON r.hospital_name = dr.hospital_name
GROUP BY hospital, city
ORDER BY units_requested DESC
LIMIT 20;


-- Q20. Donors available RIGHT NOW matching open Critical requests
SELECT DISTINCT
    d.donor_id,
    d.name,
    d.blood_group,
    d.city,
    d.availability_status,
    br.request_id,
    br.hospital_name,
    br.urgency_level,
    br.units_required
FROM donors d
JOIN blood_requests br
    ON  d.blood_group         = br.blood_group
    AND d.city                = br.city
    AND d.availability_status = 'Available'
    AND br.urgency_level      = 'Critical'
ORDER BY d.city, d.blood_group
LIMIT 50;


-- ════════════════════════════════════════════
-- SECTION E: SUBQUERIES
-- ════════════════════════════════════════════

-- Q21. Blood groups where demand EXCEEDS supply
SELECT blood_group, total_demanded, total_supplied,
       (total_demanded - total_supplied) AS shortage_units
FROM (
    SELECT
        bg.blood_group,
        COALESCE(d.total_supplied, 0)  AS total_supplied,
        COALESCE(r.total_demanded, 0)  AS total_demanded
    FROM (SELECT DISTINCT blood_group FROM donors) bg
    LEFT JOIN (
        SELECT blood_group, SUM(units_donated)  AS total_supplied  FROM donation_records GROUP BY blood_group
    ) d USING (blood_group)
    LEFT JOIN (
        SELECT blood_group, SUM(units_required) AS total_demanded  FROM blood_requests   GROUP BY blood_group
    ) r USING (blood_group)
) combined
WHERE total_demanded > total_supplied
ORDER BY shortage_units DESC;


-- Q22. Cities with more requests than available donors
SELECT
    city,
    total_requests,
    available_donors,
    (total_requests - available_donors) AS gap
FROM (
    SELECT
        c.city,
        COALESCE(r.total_requests, 0)     AS total_requests,
        COALESCE(d.available_donors, 0)   AS available_donors
    FROM (SELECT DISTINCT city FROM blood_requests) c
    LEFT JOIN (SELECT city, COUNT(*) AS total_requests FROM blood_requests GROUP BY city) r USING (city)
    LEFT JOIN (SELECT city, SUM(availability_status='Available') AS available_donors FROM donors GROUP BY city) d USING (city)
) x
WHERE total_requests > available_donors
ORDER BY gap DESC
LIMIT 20;


-- Q23. Donors above the average age
SELECT
    donor_id, name, age, blood_group, city
FROM donors
WHERE age > (SELECT ROUND(AVG(age)) FROM donors)
ORDER BY age DESC
LIMIT 20;


-- Q24. Blood groups with below-average availability rate
SELECT blood_group, avail_pct
FROM (
    SELECT
        blood_group,
        ROUND(SUM(availability_status = 'Available') / COUNT(*) * 100, 1) AS avail_pct
    FROM donors
    GROUP BY blood_group
) bg_avail
WHERE avail_pct < (
    SELECT ROUND(SUM(availability_status = 'Available') / COUNT(*) * 100, 1) FROM donors
)
ORDER BY avail_pct;


-- Q25. Hospitals that requested ALL blood groups
SELECT hospital_name, COUNT(DISTINCT blood_group) AS blood_groups_requested
FROM blood_requests
GROUP BY hospital_name
HAVING blood_groups_requested = 8
ORDER BY hospital_name;


-- ════════════════════════════════════════════
-- SECTION F: WINDOW FUNCTIONS
-- ════════════════════════════════════════════

-- Q26. Running total of units donated per month (cumulative trend)
SELECT
    month,
    monthly_units,
    SUM(monthly_units) OVER (ORDER BY month ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_units
FROM (
    SELECT
        DATE_FORMAT(donation_date, '%Y-%m') AS month,
        SUM(units_donated)                  AS monthly_units
    FROM donation_records
    GROUP BY month
) monthly
ORDER BY month;


-- Q27. Rank cities by donor count (with dense rank)
SELECT
    city,
    state,
    donor_count,
    DENSE_RANK() OVER (ORDER BY donor_count DESC) AS city_rank
FROM (
    SELECT city, state, COUNT(*) AS donor_count
    FROM donors
    GROUP BY city, state
) city_totals
ORDER BY city_rank
LIMIT 20;


-- Q28. Rank blood groups within each state by donor availability
SELECT
    state,
    blood_group,
    available_donors,
    RANK() OVER (PARTITION BY state ORDER BY available_donors DESC) AS rank_in_state
FROM (
    SELECT
        state,
        blood_group,
        SUM(availability_status = 'Available') AS available_donors
    FROM donors
    GROUP BY state, blood_group
) state_bg
ORDER BY state, rank_in_state;


-- Q29. Month-over-month growth in blood requests
SELECT
    month,
    total_requests,
    LAG(total_requests) OVER (ORDER BY month)  AS prev_month_requests,
    ROUND(
        (total_requests - LAG(total_requests) OVER (ORDER BY month))
        / NULLIF(LAG(total_requests) OVER (ORDER BY month), 0) * 100, 1
    ) AS mom_growth_pct
FROM (
    SELECT
        DATE_FORMAT(request_date, '%Y-%m') AS month,
        COUNT(*)                           AS total_requests
    FROM blood_requests
    GROUP BY month
) monthly
ORDER BY month;


-- Q30. Top donor per city (most units donated) using ROW_NUMBER
SELECT city, donor_id, donor_name, blood_group, total_units
FROM (
    SELECT
        d.city,
        d.donor_id,
        d.name                  AS donor_name,
        d.blood_group,
        SUM(dr.units_donated)   AS total_units,
        ROW_NUMBER() OVER (PARTITION BY d.city ORDER BY SUM(dr.units_donated) DESC) AS rn
    FROM donors d
    JOIN donation_records dr ON d.donor_id = dr.donor_id
    GROUP BY d.city, d.donor_id, d.name, d.blood_group
) ranked
WHERE rn = 1
ORDER BY total_units DESC
LIMIT 20;

-- ════════════════════════════════════════════
-- SECTION G: QUICK KPI SNAPSHOT
-- ════════════════════════════════════════════

-- Q31. Single-query executive KPI dashboard
SELECT
    (SELECT COUNT(*)                                      FROM donors)                       AS total_donors,
    (SELECT SUM(availability_status='Available')          FROM donors)                       AS available_donors,
    (SELECT ROUND(AVG(age),1)                             FROM donors)                       AS avg_donor_age,
    (SELECT COUNT(*)                                      FROM blood_requests)               AS total_requests,
    (SELECT SUM(units_required)                           FROM blood_requests)               AS total_units_requested,
    (SELECT SUM(urgency_level='Critical')                 FROM blood_requests)               AS critical_requests,
    (SELECT COUNT(*)                                      FROM donation_records)             AS total_donations,
    (SELECT SUM(units_donated)                            FROM donation_records)             AS total_units_donated,
    (SELECT COUNT(DISTINCT donor_id)                      FROM donation_records)             AS active_donors,
    (SELECT blood_group FROM (SELECT blood_group, SUM(units_required) AS u
                               FROM blood_requests GROUP BY blood_group ORDER BY u DESC LIMIT 1) x) AS most_demanded_bg;
