<div align="center">

# 🩸 Blood Donation Analytics & Donor Intelligence Platform

### An end-to-end Data Analytics project built for real-world impact

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-lightgrey?style=flat-square&logo=pandas)](https://pandas.pydata.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?style=flat-square&logo=mysql)](https://www.mysql.com/)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow?style=flat-square&logo=powerbi)](https://powerbi.microsoft.com/)
[![NumPy](https://img.shields.io/badge/NumPy-1.24+-blue?style=flat-square&logo=numpy)](https://numpy.org/)

</div>

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Problem Statement](#-problem-statement)
- [Objectives](#-objectives)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Dataset Description](#-dataset-description)
- [Project Structure](#-project-structure)
- [Python Workflow](#-python-workflow)
- [SQL Analysis](#-sql-analysis)
- [Power BI Dashboard](#-power-bi-dashboard)
- [Key Insights](#-key-insights)
- [How to Run](#-how-to-run)
- [Screenshots](#-screenshots)
- [Resume Description](#-resume-description)

---

## 🔍 Project Overview

The **Blood Donation Analytics & Donor Intelligence Platform** is a comprehensive, production-grade data analytics solution that transforms raw blood donation and hospital request data into actionable intelligence. Built entirely on Python, SQL, and Power BI, this project demonstrates the full data analyst workflow — from synthetic data generation and cleaning through exploratory analysis, SQL querying, and interactive dashboarding.

The platform tracks 5,000+ donors, 2,000+ hospital blood requests, and 3,500+ donation events across 50 major Indian cities, providing stakeholders with critical visibility into blood supply chains, donor availability, and demand patterns.

---

## 🚨 Problem Statement

India's blood supply system faces three critical challenges:

1. **Supply-demand mismatch** — Certain blood groups (especially O- and AB-) are chronically undersupplied relative to demand, with hospitals frequently unable to fulfil critical requests.
2. **Donor visibility gap** — Blood banks lack real-time intelligence on available donors by location and blood group, causing delays in emergency situations.
3. **No predictive demand insight** — Seasonal and geographic patterns in blood demand are not tracked systematically, preventing proactive donor recruitment.

This platform addresses all three challenges through data-driven analytics.

---

## 🎯 Objectives

| # | Objective | Status |
|---|-----------|--------|
| 1 | Design and populate a relational MySQL database for donors, requests, and donations | ✅ |
| 2 | Generate 10,000+ realistic synthetic records for 50 Indian cities | ✅ |
| 3 | Build a reusable Python data cleaning pipeline | ✅ |
| 4 | Perform comprehensive EDA and statistical analysis | ✅ |
| 5 | Write 30 production-grade SQL queries (JOINs, subqueries, window functions) | ✅ |
| 6 | Create a multi-page interactive Power BI dashboard | ✅ |
| 7 | Identify key blood shortage patterns and donor retention insights | ✅ |

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Data Generation | Python + NumPy | Synthetic realistic datasets |
| Data Cleaning | Python + Pandas | Missing values, standardisation, validation |
| Exploratory Analysis | Python + Pandas + Matplotlib + Seaborn | Statistical summaries, visualisations |
| Database | MySQL 8.0 | Structured storage, relational queries |
| SQL Analysis | MySQL (JOINs, CTEs, Window Functions) | Business intelligence queries |
| Dashboard | Microsoft Power BI Desktop | Interactive reporting |
| Notebooks | Jupyter Notebook | Reproducible analysis |
| Version Control | Git / GitHub | Project tracking |

---

## 🏗 Project Architecture

```
Raw Data Generation (Python)
         │
         ▼
   data/raw/*.csv
         │
         ▼
 Data Cleaning Pipeline (Python)
         │
         ▼
  data/cleaned/*.csv
    ┌────┴────┐
    │         │
    ▼         ▼
MySQL DB   Power BI
(SQL       (Dashboard)
Analysis)
    │
    ▼
Reports & Insights
```

**Data Flow:**
1. `data_generation.py` → generates synthetic realistic CSVs
2. `data_cleaning.py` → validates, deduplicates, standardises, outputs clean CSVs
3. `eda_analysis.py` → statistical EDA, exports summary tables and insight reports
4. `schema.sql` → creates MySQL database with proper indexes, constraints, views, and stored procedures
5. `analysis_queries.sql` → 30 business intelligence queries covering all analytical requirements
6. Power BI → connects to cleaned CSVs, applies DAX measures, renders 4-page dashboard

---

## 📊 Dataset Description

All datasets are synthetically generated using Python with realistic Indian distributions.

### donors.csv (5,000 records)
| Column | Type | Description |
|--------|------|-------------|
| donor_id | VARCHAR | Unique donor ID (D00001–D05000) |
| name | VARCHAR | Full name (Indian first + last names) |
| age | INT | Age 18–65 |
| gender | ENUM | Male / Female / Other |
| blood_group | ENUM | A+, A-, B+, B-, AB+, AB-, O+, O- |
| city | VARCHAR | One of 50 major Indian cities |
| state | VARCHAR | Corresponding Indian state |
| last_donation_date | DATE | NULL for never-donated donors |
| availability_status | ENUM | Available / Unavailable |
| latitude | DECIMAL | Geo-coordinate (with noise) |
| longitude | DECIMAL | Geo-coordinate (with noise) |

### blood_requests.csv (2,000 records)
| Column | Type | Description |
|--------|------|-------------|
| request_id | VARCHAR | Unique request ID (R00001–R02000) |
| hospital_name | VARCHAR | One of 25 real Indian hospital names |
| blood_group | ENUM | Requested blood group |
| units_required | INT | Units needed (1–10) |
| urgency_level | ENUM | Critical / High / Medium / Low |
| city | VARCHAR | City of request |
| request_date | DATE | Date of request (2023–2024) |

### donation_records.csv (3,500 records)
| Column | Type | Description |
|--------|------|-------------|
| donation_id | VARCHAR | Unique donation ID (DON000001–) |
| donor_id | VARCHAR | FK → donors.donor_id |
| hospital_name | VARCHAR | Hospital receiving blood |
| blood_group | ENUM | Blood group donated |
| donation_date | DATE | Date of donation (2020–2024) |
| units_donated | INT | Units donated (1–3) |

---

## 📁 Project Structure

```
blood-donation-analytics/
│
├── data/
│   ├── raw/
│   │   ├── donors.csv                    # 5,000 raw donor records
│   │   ├── blood_requests.csv            # 2,000 raw request records
│   │   └── donation_records.csv          # 3,500 raw donation records
│   │
│   └── cleaned/
│       ├── donors_clean.csv              # Validated & standardised donors
│       ├── blood_requests_clean.csv      # Validated requests
│       └── donation_records_clean.csv    # Validated donations
│
├── notebooks/
│   └── blood_donation_analysis.ipynb    # Full EDA notebook (13 cells)
│
├── python/
│   ├── data_generation.py               # Synthetic data generator
│   ├── data_cleaning.py                 # Cleaning & validation pipeline
│   └── eda_analysis.py                  # EDA with 8 analysis sections
│
├── sql/
│   ├── schema.sql                       # DB schema, views, stored procedure
│   └── analysis_queries.sql             # 30 analytical SQL queries
│
├── dashboard/
│   └── powerbi_guide.md                 # Complete Power BI setup guide
│
├── reports/
│   ├── insights_report.txt              # Auto-generated KPI summary
│   ├── blood_group_analysis.csv         # Supply vs demand by blood group
│   ├── city_donor_analysis.csv          # City-level donor stats
│   ├── monthly_donation_trends.csv      # Month-wise trends
│   └── kpi_summary.csv                  # Executive KPI table
│
├── screenshots/                          # Dashboard screenshots (add after PBI setup)
│
├── README.md                             # This file
├── requirements.txt                      # Python dependencies
└── .gitignore                            # Git exclusions
```

---

## 🐍 Python Workflow

### Step 1 — Data Generation
```bash
python python/data_generation.py
```
Generates three CSV files in `data/raw/` with:
- Realistic Indian names, cities, and coordinates
- Blood group distribution matching India's national profile
- Date ranges spanning 2020–2024
- ~3% missing values injected for cleaning practice

### Step 2 — Data Cleaning
```bash
python python/data_cleaning.py
```
Performs:
- **Duplicate removal** — exact row deduplication
- **Missing value handling** — age filled with median; gender set to 'Unknown'
- **Standardisation** — blood groups upper-cased, city/state title-cased
- **Validation** — blood group checked against valid set; coordinates validated to India bounds
- **Date parsing** — future dates removed; format standardised to YYYY-MM-DD
- **Range checks** — units clipped to valid ranges

### Step 3 — EDA Analysis
```bash
python python/eda_analysis.py
```
Generates 8 analysis sections:
1. Statistical summaries (describe, nulls, shape)
2. Blood group analysis (supply/demand/availability)
3. City-wise donor analysis (top 15 cities)
4. Monthly & yearly donation trends
5. Urgency level analysis
6. Donor activity (repeat vs one-time)
7. Hospital analysis
8. Auto-exported CSV reports and insights_report.txt

---

## 🗄 SQL Analysis

### Database Setup
```sql
-- 1. Run schema
source sql/schema.sql;

-- 2. Load cleaned data (update paths)
LOAD DATA LOCAL INFILE 'data/cleaned/donors_clean.csv' INTO TABLE donors ...;

-- 3. Run analysis queries
source sql/analysis_queries.sql;
```

### SQL Capabilities Demonstrated

| Category | Queries | Examples |
|----------|---------|---------|
| Basic Aggregations | Q1–Q5 | Blood group distribution, city rankings |
| Blood Demand Analysis | Q6–Q10 | Most demanded groups, urgency breakdown, monthly trends |
| Donation Analysis | Q11–Q15 | Units donated, active donors, hospital rankings |
| JOIN Queries | Q16–Q20 | Donor + donation profiles, supply vs demand by city |
| Subqueries | Q21–Q25 | Shortage analysis, cities with gaps, above-average age donors |
| Window Functions | Q26–Q30 | Running totals, city rankings, MoM growth, top donor per city |
| KPI Snapshot | Q31 | Single-query executive dashboard metrics |

### Sample Queries

```sql
-- Most demanded blood groups
SELECT blood_group, SUM(units_required) AS total_units_demanded
FROM blood_requests
GROUP BY blood_group
ORDER BY total_units_demanded DESC;

-- Running cumulative donation trend (Window Function)
SELECT month, monthly_units,
       SUM(monthly_units) OVER (ORDER BY month) AS cumulative_units
FROM (
    SELECT DATE_FORMAT(donation_date,'%Y-%m') AS month,
           SUM(units_donated) AS monthly_units
    FROM donation_records GROUP BY month
) m ORDER BY month;

-- Blood shortage: demand exceeds supply
SELECT blood_group, total_demanded - total_supplied AS shortage
FROM (
    SELECT bg.blood_group,
           COALESCE(d.total_supplied, 0) AS total_supplied,
           COALESCE(r.total_demanded, 0) AS total_demanded
    FROM (SELECT DISTINCT blood_group FROM donors) bg
    LEFT JOIN (SELECT blood_group, SUM(units_donated)  AS total_supplied FROM donation_records GROUP BY blood_group) d USING(blood_group)
    LEFT JOIN (SELECT blood_group, SUM(units_required) AS total_demanded FROM blood_requests   GROUP BY blood_group) r USING(blood_group)
) x WHERE total_demanded > total_supplied ORDER BY shortage DESC;
```

---

## 📊 Power BI Dashboard

The dashboard contains **4 interactive pages**, fully guided in `dashboard/powerbi_guide.md`.

### Page 1 — Executive Summary
KPI cards · Blood group donut · Urgency breakdown · Monthly trends · Supply vs Demand bar chart

### Page 2 — Blood Demand Analysis
Demand by blood group · Critical requests map · Monthly area chart · Hospital treemap

### Page 3 — Donor Analytics
Availability gauge · Gender donut · Age group histogram · Donor geo-map · City ranking

### Page 4 — City & Hospital Insights
City bubble map · State filled map · Hospital scatter (request vs donation) · Supply gap bar

**DAX Measures include:** Total Donors, Available Donors, Availability Rate %, Critical Requests %, Supply Demand Gap, Unique Active Donors, Average Donor Age.

**Slicers on every page:** Blood Group · City · State · Urgency Level · Year

---

## 💡 Key Insights

Based on the analysis of 5,000 donors, 2,000 requests, and 3,500 donations:

| Insight | Finding |
|---------|---------|
| 🔴 Most demanded blood group | **O+** (38% of all requests) |
| 🟡 Most critical shortage | **AB-** and **B-** (lowest supply, consistent demand) |
| 📍 Top donor cities | Tiruchirappalli, Mysore, Coimbatore |
| 🏥 Most active hospital | KEM Hospital (highest donations received) |
| 👥 Donor availability | **95.6%** of registered donors are available |
| 📅 Peak donation month | Highest volumes in mid-year (May–July) |
| 📉 Demand > Supply gap | Total deficit of **~4,296 units** across all groups |
| 🔁 Repeat donors | ~72% of active donors have donated more than once |
| 👴 Average donor age | **41.5 years** — middle-aged donors dominate |
| ⚠️ Critical requests | 19.6% of all hospital requests are **Critical urgency** |

---

## 🚀 How to Run

### Prerequisites
- Python 3.10+
- MySQL 8.0+
- Power BI Desktop (free from Microsoft)
- Git

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/blood-donation-analytics.git
cd blood-donation-analytics

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Generate raw data
python python/data_generation.py

# 4. Clean the data
python python/data_cleaning.py

# 5. Run EDA analysis
python python/eda_analysis.py

# 6. Set up MySQL database
mysql -u root -p < sql/schema.sql

# 7. Load cleaned CSVs into MySQL
#    (update absolute paths in schema.sql LOAD DATA section)
mysql -u root -p blood_donation_analytics < sql/schema.sql

# 8. Run analytical SQL queries
mysql -u root -p blood_donation_analytics < sql/analysis_queries.sql

# 9. Open Power BI Dashboard
#    → Follow dashboard/powerbi_guide.md step-by-step
```

### Jupyter Notebook
```bash
jupyter notebook notebooks/blood_donation_analysis.ipynb
```

---

## 📸 Screenshots

> Add screenshots of your Power BI dashboard pages here after setup.

| Page | Description |
|------|-------------|
| `screenshots/page1_executive_summary.png` | KPIs, blood group donut, monthly trend |
| `screenshots/page2_blood_demand.png` | Demand analysis, urgency breakdown |
| `screenshots/page3_donor_analytics.png` | Donor map, age groups, availability |
| `screenshots/page4_city_hospital.png` | City map, hospital scatter |

---

## 📄 Resume Description

> Copy-paste ready for your resume, LinkedIn, or portfolio:

---

**Blood Donation Analytics & Donor Intelligence Platform** | *Python · SQL · Power BI · Pandas · MySQL*

Designed and built an end-to-end data analytics platform simulating a real-world blood bank intelligence system. Generated and cleaned a dataset of 10,500+ records (5,000 donors, 2,000 hospital requests, 3,500 donations) across 50 Indian cities using Python and Pandas. Developed a three-stage pipeline: synthetic data generation with realistic distributions, automated data cleaning with validation logic, and comprehensive EDA with statistical summaries. Wrote 30 production-grade MySQL queries covering JOINs, correlated subqueries, and window functions (ROW_NUMBER, LAG, SUM OVER) to surface blood supply-demand gaps, donor availability patterns, and emergency request trends. Designed a 4-page interactive Power BI dashboard with DAX measures, slicers, KPI cards, geo-maps, and trend charts for executive and operational stakeholders. Key finding: a system-wide deficit of ~4,296 blood units, with AB- and B- groups most critically undersupplied.

---

<div align="center">
Made with ❤️ for the Data Analytics community
</div>
