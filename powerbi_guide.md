# Power BI Dashboard Guide
## Blood Donation Analytics & Donor Intelligence Platform

---

## Step 1 — Import Data

Open Power BI Desktop → **Get Data → Text/CSV** and import all three files from `data/cleaned/`:
- `donors_clean.csv`
- `blood_requests_clean.csv`
- `donation_records_clean.csv`

---

## Step 2 — Data Model (Relationships)

In the **Model** view, create relationships:

| From Table       | Column     | To Table         | Column     | Cardinality |
|------------------|------------|------------------|------------|-------------|
| donation_records | donor_id   | donors           | donor_id   | Many-to-One |

---

## Step 3 — DAX Measures

Create a dedicated **Measures** table and add the following:

```dax
-- KPI: Total Donors
Total Donors = COUNTROWS(donors)

-- KPI: Available Donors
Available Donors = CALCULATE(COUNTROWS(donors), donors[availability_status] = "Available")

-- KPI: Availability Rate %
Availability Rate % = DIVIDE([Available Donors], [Total Donors], 0) * 100

-- KPI: Total Blood Requests
Total Requests = COUNTROWS(blood_requests)

-- KPI: Total Units Requested
Total Units Requested = SUM(blood_requests[units_required])

-- KPI: Critical Requests
Critical Requests = CALCULATE(COUNTROWS(blood_requests), blood_requests[urgency_level] = "Critical")

-- KPI: Critical Request %
Critical Request % = DIVIDE([Critical Requests], [Total Requests], 0) * 100

-- KPI: Total Donations
Total Donations = COUNTROWS(donation_records)

-- KPI: Total Units Donated
Total Units Donated = SUM(donation_records[units_donated])

-- KPI: Average Donor Age
Avg Donor Age = AVERAGE(donors[age])

-- KPI: Supply vs Demand Gap
Supply Demand Gap = [Total Units Requested] - [Total Units Donated]

-- KPI: Unique Active Donors
Unique Active Donors = DISTINCTCOUNT(donation_records[donor_id])
```

---

## Step 4 — Calculated Columns

Add these calculated columns in the **donors** table:

```dax
-- Age Group
Age Group =
SWITCH(TRUE(),
    donors[age] <= 25, "18-25",
    donors[age] <= 35, "26-35",
    donors[age] <= 45, "36-45",
    donors[age] <= 55, "46-55",
    "56-65"
)

-- Days Since Last Donation
Days Since Donation =
IF(
    ISBLANK(donors[last_donation_date]),
    BLANK(),
    DATEDIFF(donors[last_donation_date], TODAY(), DAY)
)
```

Add in **blood_requests** table:

```dax
-- Request Year
Request Year = YEAR(blood_requests[request_date])

-- Request Month Name
Request Month = FORMAT(blood_requests[request_date], "MMM YYYY")
```

Add in **donation_records** table:

```dax
-- Donation Year
Donation Year = YEAR(donation_records[donation_date])

-- Donation Month
Donation Month = FORMAT(donation_records[donation_date], "MMM YYYY")
```

---

## Step 5 — Dashboard Pages

### Page 1: Executive Summary

**Layout:** Full-width KPI row → Charts below

| Visual | Type | Fields |
|--------|------|--------|
| Total Donors | Card | `[Total Donors]` |
| Available Donors | Card | `[Available Donors]` |
| Total Requests | Card | `[Total Requests]` |
| Critical Requests | Card | `[Critical Requests]` |
| Units Donated | Card | `[Total Units Donated]` |
| Units Requested | Card | `[Total Units Requested]` |
| Blood Group Donors | Donut Chart | Legend: blood_group, Values: [Total Donors] |
| Urgency Breakdown | Donut Chart | Legend: urgency_level, Values: [Total Requests] |
| Monthly Requests Trend | Line Chart | X: request_date (month), Y: [Total Requests] |
| Supply vs Demand | Clustered Bar | Axis: blood_group, Values: [Total Units Donated] + [Total Units Requested] |

**Slicers (top of page):**  
- Blood Group (donors[blood_group])  
- City (donors[city])  
- Year (blood_requests[Request Year])

---

### Page 2: Blood Demand Analysis

| Visual | Type | Fields |
|--------|------|--------|
| Most Demanded Blood Group | Bar Chart | Axis: blood_group, Values: [Total Units Requested] |
| Urgency by Blood Group | Stacked Bar | Axis: blood_group, Legend: urgency_level, Values: [Total Requests] |
| Monthly Request Trend | Area Chart | X: request_date, Y: [Total Requests] |
| Critical Requests by City | Map | Location: city, Size: [Critical Requests] |
| Top Requesting Hospitals | Horizontal Bar | Axis: hospital_name, Values: [Total Requests] |
| Requests by Urgency | Treemap | Group: urgency_level, Values: [Total Units Requested] |

**Slicers:** Blood Group · Urgency Level · City · Year

---

### Page 3: Donor Analytics

| Visual | Type | Fields |
|--------|------|--------|
| Availability Rate % | Gauge | Value: [Availability Rate %], Max: 100 |
| Gender Distribution | Donut | Legend: gender, Values: [Total Donors] |
| Age Group Distribution | Column Chart | Axis: Age Group, Values: [Total Donors] |
| Average Donor Age | Card | `[Avg Donor Age]` |
| Never Donated Donors | Card | Filter donors where last_donation_date is blank |
| Donors by Blood Group & Gender | Clustered Bar | Axis: blood_group, Legend: gender |
| Top 15 Donor Cities | Horizontal Bar | Axis: city, Values: [Total Donors] |
| Donor Map | Filled Map / Bubble Map | Lat: latitude, Long: longitude, Size: [Total Donors] |

**Slicers:** Blood Group · Gender · State · Availability Status

---

### Page 4: City & Hospital Insights

| Visual | Type | Fields |
|--------|------|--------|
| City Donor Distribution | Map | Location: city, Size: [Total Donors] |
| Top 10 Cities by Requests | Bar | Axis: city, Values: [Total Units Requested] |
| Hospital Blood Received | Horizontal Bar | Axis: hospital_name, Values: [Total Units Donated] |
| Hospital Requests vs Donations | Scatter | X: [Total Requests], Y: [Total Units Donated], Details: hospital_name |
| State-wise Donors | Filled Map | Location: state, Color Saturation: [Total Donors] |
| City Supply Gap | Bar (conditional format) | Axis: city, Values: [Supply Demand Gap] |

**Slicers:** City · State · Hospital · Blood Group

---

## Step 6 — Design Tips

- **Theme:** Apply a custom red/white theme (matches blood donation branding)
- **Conditional Formatting:** Apply red formatting on Supply Demand Gap visuals when gap > 0
- **Bookmarks:** Create bookmarks for "Critical Only" and "Available Donors Only" filter states
- **Tooltips:** Add custom tooltip pages showing full donor or hospital details
- **Mobile Layout:** Enable and configure the mobile view for each page
- **Page Navigation:** Add navigation buttons between pages for a polished feel

---

## Step 7 — Publish

1. **File → Publish → Power BI Service**
2. Set scheduled refresh if connecting to a live database
3. Share the dashboard link with stakeholders or embed in a portal

