"""
Blood Donation Analytics & Donor Intelligence Platform
=======================================================
eda_analysis.py  —  Exploratory Data Analysis & Insights
Author: Data Analytics Team
"""

import pandas as pd
import numpy as np
import os

CLEANED_DIR  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "cleaned")
REPORTS_DIR  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


def sep(title=""):
    print(f"\n{'─'*55}")
    if title:
        print(f"  {title}")
        print(f"{'─'*55}")


def load_data():
    donors    = pd.read_csv(os.path.join(CLEANED_DIR, "donors_clean.csv"),           parse_dates=["last_donation_date"])
    requests  = pd.read_csv(os.path.join(CLEANED_DIR, "blood_requests_clean.csv"),   parse_dates=["request_date"])
    donations = pd.read_csv(os.path.join(CLEANED_DIR, "donation_records_clean.csv"), parse_dates=["donation_date"])
    print(f"[INFO] Loaded  donors={len(donors):,}  requests={len(requests):,}  donations={len(donations):,}")
    return donors, requests, donations


# ─────────────────────────────────────────────
# 1. BASIC STATISTICAL SUMMARIES
# ─────────────────────────────────────────────
def statistical_summary(donors, requests, donations):
    sep("1. Statistical Summaries")

    print("\n--- Donors: Numeric Summary ---")
    print(donors[["age"]].describe().round(2).to_string())

    print("\n--- Blood Requests: Units Summary ---")
    print(requests[["units_required"]].describe().round(2).to_string())

    print("\n--- Donation Records: Units Summary ---")
    print(donations[["units_donated"]].describe().round(2).to_string())

    print(f"\n  Total unique donors     : {donors['donor_id'].nunique():,}")
    print(f"  Total unique cities     : {donors['city'].nunique():,}")
    print(f"  Total units donated     : {donations['units_donated'].sum():,}")
    print(f"  Total units requested   : {requests['units_required'].sum():,}")
    print(f"  Average donor age       : {donors['age'].mean():.1f} years")
    print(f"  Median donor age        : {donors['age'].median():.1f} years")


# ─────────────────────────────────────────────
# 2. BLOOD GROUP ANALYSIS
# ─────────────────────────────────────────────
def blood_group_analysis(donors, requests, donations):
    sep("2. Blood Group Analysis")

    # Supply side
    supply = (donors.groupby("blood_group")
              .agg(total_donors=("donor_id","count"),
                   available_donors=("availability_status", lambda x:(x=="Available").sum()))
              .assign(availability_rate=lambda df: (df["available_donors"]/df["total_donors"]*100).round(1))
              .sort_values("total_donors", ascending=False))

    # Demand side
    demand = (requests.groupby("blood_group")
              .agg(total_requests=("request_id","count"),
                   total_units_needed=("units_required","sum"))
              .sort_values("total_requests", ascending=False))

    # Actual donations
    donated = (donations.groupby("blood_group")
               .agg(total_donations=("donation_id","count"),
                    total_units_donated=("units_donated","sum")))

    combined = supply.join(demand).join(donated)
    combined["demand_supply_ratio"] = (
        combined["total_requests"] / combined["total_donors"] * 100
    ).round(2)

    print("\n--- Blood Group Supply vs Demand ---")
    print(combined.to_string())

    print("\n  Most demanded blood group :", demand["total_requests"].idxmax())
    print("  Most available blood group:", supply["total_donors"].idxmax())
    print("  Scarcest blood group      :", supply["total_donors"].idxmin())
    return combined


# ─────────────────────────────────────────────
# 3. CITY-WISE ANALYSIS
# ─────────────────────────────────────────────
def city_analysis(donors, requests):
    sep("3. City-wise Analysis")

    city_donors = (donors.groupby("city")
                   .agg(total_donors=("donor_id","count"),
                        available_donors=("availability_status", lambda x:(x=="Available").sum()),
                        avg_age=("age","mean"))
                   .round(1)
                   .sort_values("total_donors", ascending=False))

    city_requests = (requests.groupby("city")
                     .agg(total_requests=("request_id","count"),
                          total_units_needed=("units_required","sum"))
                     .sort_values("total_requests", ascending=False))

    print("\n--- Top 15 Cities by Donor Count ---")
    print(city_donors.head(15).to_string())

    print("\n--- Top 15 Cities by Blood Requests ---")
    print(city_requests.head(15).to_string())

    # Blood shortage index: cities where requests > available donors
    merged = city_donors.join(city_requests, how="outer").fillna(0)
    merged["shortage_index"] = (
        merged["total_requests"] - merged["available_donors"]
    ).clip(lower=0).astype(int)

    shortage = merged[merged["shortage_index"] > 0].sort_values("shortage_index", ascending=False)
    print("\n--- Top 10 Cities With Blood Shortage Risk ---")
    print(shortage[["available_donors","total_requests","shortage_index"]].head(10).to_string())

    return city_donors, city_requests


# ─────────────────────────────────────────────
# 4. MONTHLY DONATION TRENDS
# ─────────────────────────────────────────────
def monthly_trends(donations, requests):
    sep("4. Monthly Donation & Request Trends")

    donations["year_month"]  = donations["donation_date"].dt.to_period("M")
    requests["year_month"]   = requests["request_date"].dt.to_period("M")

    monthly_don = (donations.groupby("year_month")
                   .agg(donations_count=("donation_id","count"),
                        units_donated=("units_donated","sum"))
                   .sort_index())

    monthly_req = (requests.groupby("year_month")
                   .agg(requests_count=("request_id","count"),
                        units_requested=("units_required","sum"))
                   .sort_index())

    print("\n--- Monthly Donation Summary (last 12 months) ---")
    print(monthly_don.tail(12).to_string())

    print("\n--- Monthly Request Summary (last 12 months) ---")
    print(monthly_req.tail(12).to_string())

    peak_don_month = monthly_don["donations_count"].idxmax()
    peak_req_month = monthly_req["requests_count"].idxmax()
    print(f"\n  Peak donation month : {peak_don_month}")
    print(f"  Peak request month  : {peak_req_month}")

    return monthly_don, monthly_req


# ─────────────────────────────────────────────
# 5. DONOR ACTIVITY ANALYSIS
# ─────────────────────────────────────────────
def donor_activity(donors, donations):
    sep("5. Donor Activity Analysis")

    # Availability breakdown
    avail = donors["availability_status"].value_counts()
    avail_pct = (avail / len(donors) * 100).round(1)
    print("\n--- Donor Availability ---")
    for status, cnt in avail.items():
        print(f"  {status:15s}: {cnt:,}  ({avail_pct[status]}%)")

    # Donation frequency per donor
    freq = (donations.groupby("donor_id")["donation_id"]
            .count()
            .reset_index(name="donation_count"))
    print("\n--- Donation Frequency Distribution ---")
    print(freq["donation_count"].describe().round(2).to_string())

    # Top 10 most active donors
    top_donors = freq.nlargest(10, "donation_count")
    top_donors = top_donors.merge(
        donors[["donor_id","name","city","blood_group"]],
        on="donor_id", how="left"
    )
    print("\n--- Top 10 Most Active Donors ---")
    print(top_donors.to_string(index=False))

    # Gender distribution
    gender_dist = donors["gender"].value_counts()
    print("\n--- Gender Distribution ---")
    print(gender_dist.to_string())

    # Age group segmentation
    bins   = [18, 25, 35, 45, 55, 65]
    labels = ["18-24","25-34","35-44","45-54","55-65"]
    donors["age_group"] = pd.cut(donors["age"], bins=bins, labels=labels, right=False)
    age_grp = donors["age_group"].value_counts().sort_index()
    print("\n--- Donor Age Group Distribution ---")
    print(age_grp.to_string())

    return freq


# ─────────────────────────────────────────────
# 6. URGENCY / EMERGENCY ANALYSIS
# ─────────────────────────────────────────────
def urgency_analysis(requests):
    sep("6. Emergency Demand Analysis")

    urgency = (requests.groupby("urgency_level")
               .agg(count=("request_id","count"),
                    total_units=("units_required","sum"),
                    avg_units=("units_required","mean"))
               .round(2)
               .sort_values("count", ascending=False))
    print("\n--- Requests by Urgency Level ---")
    print(urgency.to_string())

    # Critical blood group demand
    critical = requests[requests["urgency_level"] == "Critical"]
    crit_bg  = critical["blood_group"].value_counts()
    print("\n--- Critical Requests by Blood Group ---")
    print(crit_bg.to_string())

    # Urgency trend over time
    requests["year_month"] = requests["request_date"].dt.to_period("M")
    crit_trend = (requests[requests["urgency_level"]=="Critical"]
                  .groupby("year_month")["request_id"].count())
    print("\n--- Monthly Critical Request Trend (last 6 months) ---")
    print(crit_trend.tail(6).to_string())


# ─────────────────────────────────────────────
# 7. HOSPITAL ANALYSIS
# ─────────────────────────────────────────────
def hospital_analysis(requests, donations):
    sep("7. Hospital Analysis")

    hosp_req = (requests.groupby("hospital_name")
                .agg(total_requests=("request_id","count"),
                     total_units_needed=("units_required","sum"))
                .sort_values("total_requests", ascending=False))

    hosp_don = (donations.groupby("hospital_name")
                .agg(total_donations=("donation_id","count"),
                     total_units_donated=("units_donated","sum"))
                .sort_values("total_donations", ascending=False))

    print("\n--- Top 10 Hospitals by Requests ---")
    print(hosp_req.head(10).to_string())

    print("\n--- Top 10 Hospitals by Donations Received ---")
    print(hosp_don.head(10).to_string())


# ─────────────────────────────────────────────
# 8. EXPORT SUMMARY REPORT
# ─────────────────────────────────────────────
def export_summary(donors, requests, donations, bg_combined, city_donors, monthly_don):
    sep("8. Exporting Summary Tables")

    bg_combined.to_csv(os.path.join(REPORTS_DIR, "blood_group_analysis.csv"))
    city_donors.head(30).to_csv(os.path.join(REPORTS_DIR, "city_donor_analysis.csv"))
    monthly_don.to_csv(os.path.join(REPORTS_DIR, "monthly_donation_trends.csv"))

    # Key KPIs
    kpis = {
        "Total Donors":               len(donors),
        "Available Donors":           (donors["availability_status"]=="Available").sum(),
        "Total Blood Requests":       len(requests),
        "Total Donations":            len(donations),
        "Total Units Donated":        int(donations["units_donated"].sum()),
        "Total Units Requested":      int(requests["units_required"].sum()),
        "Average Donor Age":          round(donors["age"].mean(), 1),
        "Most Demanded Blood Group":  requests["blood_group"].value_counts().idxmax(),
        "Most Available Blood Group": donors["blood_group"].value_counts().idxmax(),
        "Top Donor City":             donors["city"].value_counts().idxmax(),
        "Top Request City":           requests["city"].value_counts().idxmax(),
        "Critical Requests":          int((requests["urgency_level"]=="Critical").sum()),
    }
    kpi_df = pd.DataFrame(list(kpis.items()), columns=["KPI","Value"])
    kpi_df.to_csv(os.path.join(REPORTS_DIR, "kpi_summary.csv"), index=False)

    print(f"\n  Reports saved to: {REPORTS_DIR}")
    print("\n--- KEY KPIs ---")
    for k, v in kpis.items():
        print(f"  {k:35s}: {v}")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print("\n" + "="*55)
    print("  Blood Donation Analytics — EDA Pipeline")
    print("="*55)

    donors, requests, donations = load_data()

    statistical_summary(donors, requests, donations)
    bg_combined                = blood_group_analysis(donors, requests, donations)
    city_donors, city_requests = city_analysis(donors, requests)
    monthly_don, monthly_req   = monthly_trends(donations, requests)
    donor_activity(donors, donations)
    urgency_analysis(requests)
    hospital_analysis(requests, donations)
    export_summary(donors, requests, donations, bg_combined, city_donors, monthly_don)

    print("\n[DONE] EDA complete.\n")


if __name__ == "__main__":
    main()
