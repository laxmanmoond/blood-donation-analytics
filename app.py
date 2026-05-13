"""
Blood Donation Analytics & Donor Intelligence Platform
======================================================
app.py  —  Streamlit Web Application
Author: Data Analytics Team
"""

import streamlit as st
import pandas as pd
import numpy as np

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Blood Donation Analytics",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #c0392b, #96281b);
        padding: 20px 28px;
        border-radius: 12px;
        margin-bottom: 24px;
        color: white;
    }
    .main-header h1 { font-size: 28px; margin: 0 0 6px 0; }
    .main-header p  { font-size: 14px; margin: 0; opacity: 0.85; }

    .kpi-card {
        background: #fff;
        border: 1px solid #e8e8e8;
        border-radius: 10px;
        padding: 16px 18px;
        text-align: center;
        height: 100%;
    }
    .kpi-label { font-size: 12px; color: #888; margin-bottom: 4px; }
    .kpi-value { font-size: 28px; font-weight: 700; color: #1a1a1a; }
    .kpi-sub   { font-size: 11px; color: #aaa; margin-top: 2px; }
    .kpi-red   .kpi-value { color: #c0392b; }
    .kpi-green .kpi-value { color: #27ae60; }
    .kpi-blue  .kpi-value { color: #2980b9; }

    .section-title {
        font-size: 15px;
        font-weight: 600;
        color: #333;
        margin: 20px 0 10px 0;
        padding-bottom: 6px;
        border-bottom: 2px solid #c0392b;
        display: inline-block;
    }
    .insight-box {
        background: #fef9f9;
        border-left: 4px solid #c0392b;
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        margin: 8px 0;
        font-size: 14px;
        color: #333;
    }
    div[data-testid="stMetricValue"] { font-size: 24px !important; }
</style>
""", unsafe_allow_html=True)


# ── Data loading ──────────────────────────────────────────────
@st.cache_data
def load_data():
    donors    = pd.read_csv("data/cleaned/donors_clean.csv",
                            parse_dates=["last_donation_date"])
    requests  = pd.read_csv("data/cleaned/blood_requests_clean.csv",
                            parse_dates=["request_date"])
    donations = pd.read_csv("data/cleaned/donation_records_clean.csv",
                            parse_dates=["donation_date"])
    return donors, requests, donations


donors, requests, donations = load_data()

BLOOD_GROUPS   = sorted(donors["blood_group"].unique().tolist())
CITIES         = sorted(donors["city"].unique().tolist())
URGENCY_LEVELS = ["Critical", "High", "Medium", "Low"]


# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🩸 Navigation")
    page = st.radio(
        "Select page",
        ["Executive Summary", "Blood Demand Analysis",
         "Donor Analytics", "City & Hospital Insights",
         "Raw Data Explorer"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("## 🔍 Filters")

    sel_bg = st.multiselect(
        "Blood Group", BLOOD_GROUPS, default=BLOOD_GROUPS,
        help="Filter all charts by blood group"
    )
    sel_city = st.multiselect(
        "City (top 20)", CITIES[:20], default=CITIES[:20],
    )
    sel_urgency = st.multiselect(
        "Urgency Level", URGENCY_LEVELS, default=URGENCY_LEVELS,
    )

    st.markdown("---")
    st.caption("Blood Donation Analytics Platform\nv1.0 · Data: 2020–2024")


# ── Apply filters ─────────────────────────────────────────────
f_donors    = donors[donors["blood_group"].isin(sel_bg)]
f_requests  = requests[
    requests["blood_group"].isin(sel_bg) &
    requests["urgency_level"].isin(sel_urgency)
]
f_donations = donations[donations["blood_group"].isin(sel_bg)]


# ── Header ────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>🩸 Blood Donation Analytics & Donor Intelligence Platform</h1>
  <p>5,000 donors · 2,000 hospital requests · 3,500 donation events · 50 Indian cities · 2020–2024</p>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 1: EXECUTIVE SUMMARY
# ══════════════════════════════════════════════════════════════
if page == "Executive Summary":

    # ── KPI Row ───────────────────────────────────────────────
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Total Donors",      f"{len(f_donors):,}")
    c2.metric("Available Donors",  f"{(f_donors['availability_status']=='Available').sum():,}",
              delta=f"{(f_donors['availability_status']=='Available').sum()/max(len(f_donors),1)*100:.1f}%")
    c3.metric("Avg Donor Age",     f"{f_donors['age'].mean():.1f} yrs")
    c4.metric("Total Requests",    f"{len(f_requests):,}")
    c5.metric("Critical Requests", f"{(f_requests['urgency_level']=='Critical').sum():,}",
              delta=f"{(f_requests['urgency_level']=='Critical').sum()/max(len(f_requests),1)*100:.1f}%",
              delta_color="inverse")
    c6.metric("Units Donated",     f"{f_donations['units_donated'].sum():,}")

    st.markdown("---")

    col_l, col_r = st.columns(2)

    # Supply vs Demand
    with col_l:
        st.markdown('<div class="section-title">Supply vs Demand by Blood Group</div>',
                    unsafe_allow_html=True)
        supply = f_donations.groupby("blood_group")["units_donated"].sum().rename("Supply")
        demand = f_requests.groupby("blood_group")["units_required"].sum().rename("Demand")
        svd    = pd.concat([supply, demand], axis=1).fillna(0).astype(int)
        svd["Gap"] = svd["Demand"] - svd["Supply"]
        svd = svd.sort_values("Demand", ascending=False)
        st.bar_chart(svd[["Supply", "Demand"]])

    # Urgency breakdown
    with col_r:
        st.markdown('<div class="section-title">Requests by Urgency Level</div>',
                    unsafe_allow_html=True)
        urg = f_requests["urgency_level"].value_counts().reindex(
            URGENCY_LEVELS, fill_value=0
        ).reset_index()
        urg.columns = ["Urgency", "Count"]
        st.bar_chart(urg.set_index("Urgency"))

    # Monthly trend
    st.markdown('<div class="section-title">Monthly Donation Trend (Units)</div>',
                unsafe_allow_html=True)
    f_donations["month"] = f_donations["donation_date"].dt.to_period("M")
    monthly = f_donations.groupby("month")["units_donated"].sum().reset_index()
    monthly["month"] = monthly["month"].astype(str)
    monthly = monthly.set_index("month")
    st.line_chart(monthly)

    # Key Insights
    st.markdown('<div class="section-title">Key Insights</div>', unsafe_allow_html=True)
    most_demanded = f_requests.groupby("blood_group")["units_required"].sum().idxmax() \
        if len(f_requests) > 0 else "N/A"
    avail_pct = (f_donors["availability_status"] == "Available").sum() / max(len(f_donors), 1) * 100
    total_deficit = max(0, f_requests["units_required"].sum() - f_donations["units_donated"].sum())

    i1, i2, i3 = st.columns(3)
    with i1:
        st.markdown(f'<div class="insight-box">🔴 Most demanded blood group is <b>{most_demanded}</b> — highest units requested across all hospitals</div>', unsafe_allow_html=True)
    with i2:
        st.markdown(f'<div class="insight-box">✅ <b>{avail_pct:.1f}%</b> of registered donors are currently available for donation</div>', unsafe_allow_html=True)
    with i3:
        st.markdown(f'<div class="insight-box">⚠️ Total blood deficit of <b>{total_deficit:,} units</b> — demand exceeds current supply</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 2: BLOOD DEMAND ANALYSIS
# ══════════════════════════════════════════════════════════════
elif page == "Blood Demand Analysis":

    st.markdown('<div class="section-title">Blood Demand KPIs</div>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Requests",    f"{len(f_requests):,}")
    k2.metric("Total Units Needed", f"{f_requests['units_required'].sum():,}")
    k3.metric("Critical Requests", f"{(f_requests['urgency_level']=='Critical').sum():,}")
    k4.metric("Avg Units/Request",  f"{f_requests['units_required'].mean():.1f}")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">Total Units Demanded by Blood Group</div>',
                    unsafe_allow_html=True)
        bg_demand = f_requests.groupby("blood_group")["units_required"].sum() \
                              .sort_values(ascending=False)
        st.bar_chart(bg_demand)

    with col2:
        st.markdown('<div class="section-title">Request Count by Blood Group</div>',
                    unsafe_allow_html=True)
        bg_count = f_requests["blood_group"].value_counts()
        st.bar_chart(bg_count)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-title">Monthly Request Trend</div>',
                    unsafe_allow_html=True)
        f_requests["month"] = f_requests["request_date"].dt.to_period("M")
        monthly_req = f_requests.groupby("month").agg(
            Requests=("request_id","count"),
            Units=("units_required","sum")
        ).reset_index()
        monthly_req["month"] = monthly_req["month"].astype(str)
        monthly_req = monthly_req.set_index("month")
        st.line_chart(monthly_req)

    with col4:
        st.markdown('<div class="section-title">Urgency Level Breakdown</div>',
                    unsafe_allow_html=True)
        urg_bg = f_requests.groupby(["blood_group","urgency_level"]).size().unstack(fill_value=0)
        urg_bg = urg_bg.reindex(columns=[c for c in URGENCY_LEVELS if c in urg_bg.columns])
        st.bar_chart(urg_bg)

    st.markdown('<div class="section-title">Top 15 Requesting Hospitals</div>',
                unsafe_allow_html=True)
    top_hosp = f_requests.groupby("hospital_name").agg(
        Requests=("request_id","count"),
        Total_Units=("units_required","sum"),
        Critical=("urgency_level", lambda x: (x=="Critical").sum())
    ).sort_values("Total_Units", ascending=False).head(15)
    st.dataframe(top_hosp, use_container_width=True)

    st.markdown('<div class="section-title">Top 15 Cities by Blood Demand</div>',
                unsafe_allow_html=True)
    city_demand = f_requests.groupby("city")["units_required"].sum() \
                             .sort_values(ascending=False).head(15)
    st.bar_chart(city_demand)


# ══════════════════════════════════════════════════════════════
# PAGE 3: DONOR ANALYTICS
# ══════════════════════════════════════════════════════════════
elif page == "Donor Analytics":

    st.markdown('<div class="section-title">Donor KPIs</div>', unsafe_allow_html=True)
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Total Donors",     f"{len(f_donors):,}")
    k2.metric("Available",        f"{(f_donors['availability_status']=='Available').sum():,}")
    k3.metric("Unavailable",      f"{(f_donors['availability_status']=='Unavailable').sum():,}")
    k4.metric("Avg Age",          f"{f_donors['age'].mean():.1f}")
    k5.metric("Never Donated",    f"{f_donors['last_donation_date'].isna().sum():,}")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">Donor Count by Blood Group</div>',
                    unsafe_allow_html=True)
        bg_donors = f_donors["blood_group"].value_counts().sort_index()
        st.bar_chart(bg_donors)

    with col2:
        st.markdown('<div class="section-title">Availability by Blood Group</div>',
                    unsafe_allow_html=True)
        avail = f_donors.groupby(["blood_group","availability_status"]).size().unstack(fill_value=0)
        if "Available" not in avail.columns:
            avail["Available"] = 0
        if "Unavailable" not in avail.columns:
            avail["Unavailable"] = 0
        st.bar_chart(avail[["Available","Unavailable"]])

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-title">Donor Age Distribution</div>',
                    unsafe_allow_html=True)
        bins   = [17,25,35,45,55,65]
        labels = ["18-25","26-35","36-45","46-55","56-65"]
        f_donors["age_group"] = pd.cut(f_donors["age"], bins=bins, labels=labels)
        age_grp = f_donors["age_group"].value_counts().sort_index()
        st.bar_chart(age_grp)

    with col4:
        st.markdown('<div class="section-title">Gender Distribution</div>',
                    unsafe_allow_html=True)
        gender = f_donors["gender"].value_counts()
        st.bar_chart(gender)

    # Donor activity
    st.markdown('<div class="section-title">Most Active Donors (Top 20)</div>',
                unsafe_allow_html=True)
    donor_activity = f_donations.groupby("donor_id").agg(
        Donations=("donation_id","count"),
        Units_Donated=("units_donated","sum"),
        Last_Donation=("donation_date","max")
    ).sort_values("Donations", ascending=False).head(20)
    donor_activity = donor_activity.merge(
        donors[["donor_id","name","blood_group","city"]],
        on="donor_id", how="left"
    )
    st.dataframe(
        donor_activity[["donor_id","name","blood_group","city","Donations","Units_Donated","Last_Donation"]],
        use_container_width=True
    )

    # Geo map
    st.markdown('<div class="section-title">Donor Locations Map</div>',
                unsafe_allow_html=True)
    map_data = f_donors[["latitude","longitude"]].dropna().rename(
        columns={"latitude":"lat","longitude":"lon"}
    )
    if len(map_data) > 0:
        st.map(map_data, zoom=4)


# ══════════════════════════════════════════════════════════════
# PAGE 4: CITY & HOSPITAL INSIGHTS
# ══════════════════════════════════════════════════════════════
elif page == "City & Hospital Insights":

    st.markdown('<div class="section-title">City & Hospital KPIs</div>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Cities Covered",   f"{f_donors['city'].nunique():,}")
    k2.metric("States Covered",   f"{f_donors['state'].nunique():,}")
    k3.metric("Hospitals (Requests)", f"{f_requests['hospital_name'].nunique():,}")
    k4.metric("Hospitals (Donations)",f"{f_donations['hospital_name'].nunique():,}")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">Top 15 Cities — Donor Count</div>',
                    unsafe_allow_html=True)
        top_donor_cities = f_donors["city"].value_counts().head(15)
        st.bar_chart(top_donor_cities)

    with col2:
        st.markdown('<div class="section-title">Top 15 Cities — Blood Demand (Units)</div>',
                    unsafe_allow_html=True)
        top_req_cities = f_requests.groupby("city")["units_required"].sum() \
                                    .sort_values(ascending=False).head(15)
        st.bar_chart(top_req_cities)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-title">Top 10 Hospitals — Units Received</div>',
                    unsafe_allow_html=True)
        top_hosp_don = f_donations.groupby("hospital_name")["units_donated"].sum() \
                                   .sort_values(ascending=False).head(10)
        st.bar_chart(top_hosp_don)

    with col4:
        st.markdown('<div class="section-title">Critical Requests by City</div>',
                    unsafe_allow_html=True)
        crit_city = f_requests[f_requests["urgency_level"]=="Critical"]["city"] \
                               .value_counts().head(10)
        st.bar_chart(crit_city)

    # Supply vs demand deficit table
    st.markdown('<div class="section-title">Blood Group Supply vs Demand — Full Analysis</div>',
                unsafe_allow_html=True)
    supply = f_donations.groupby("blood_group")["units_donated"].sum().rename("Units Supplied")
    demand = f_requests.groupby("blood_group")["units_required"].sum().rename("Units Demanded")
    svd    = pd.concat([supply, demand], axis=1).fillna(0).astype(int)
    svd["Surplus / Deficit"] = svd["Units Supplied"] - svd["Units Demanded"]
    svd["Coverage %"]        = (svd["Units Supplied"] / svd["Units Demanded"].replace(0,1) * 100).round(1)
    svd["Status"]            = svd["Surplus / Deficit"].apply(
        lambda x: "✅ Surplus" if x >= 0 else "🔴 Deficit"
    )
    svd = svd.sort_values("Surplus / Deficit")
    st.dataframe(svd, use_container_width=True)

    # State-wise donor summary
    st.markdown('<div class="section-title">State-wise Donor Summary</div>',
                unsafe_allow_html=True)
    state_summary = f_donors.groupby("state").agg(
        Total_Donors=("donor_id","count"),
        Available=("availability_status", lambda x: (x=="Available").sum()),
        Avg_Age=("age","mean")
    ).round(1).sort_values("Total_Donors", ascending=False)
    st.dataframe(state_summary, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# PAGE 5: RAW DATA EXPLORER
# ══════════════════════════════════════════════════════════════
elif page == "Raw Data Explorer":

    tab1, tab2, tab3 = st.tabs(["🧑 Donors", "🏥 Blood Requests", "💉 Donation Records"])

    with tab1:
        st.markdown(f"**{len(f_donors):,} donor records** (filtered)")
        st.markdown("**Search & filter:**")
        search = st.text_input("Search by name or city", key="donor_search")
        avail_filter = st.selectbox("Availability", ["All","Available","Unavailable"], key="avail_f")

        display = f_donors.copy()
        if search:
            display = display[
                display["name"].str.contains(search, case=False, na=False) |
                display["city"].str.contains(search, case=False, na=False)
            ]
        if avail_filter != "All":
            display = display[display["availability_status"] == avail_filter]

        st.dataframe(display.reset_index(drop=True), use_container_width=True, height=450)
        st.download_button(
            "⬇ Download filtered donors CSV",
            display.to_csv(index=False),
            "donors_filtered.csv", "text/csv"
        )

    with tab2:
        st.markdown(f"**{len(f_requests):,} request records** (filtered)")
        urg_f = st.selectbox("Urgency", ["All"] + URGENCY_LEVELS, key="urg_f")
        req_display = f_requests.copy()
        if urg_f != "All":
            req_display = req_display[req_display["urgency_level"] == urg_f]
        req_display = req_display.sort_values("request_date", ascending=False)
        st.dataframe(req_display.reset_index(drop=True), use_container_width=True, height=450)
        st.download_button(
            "⬇ Download filtered requests CSV",
            req_display.to_csv(index=False),
            "requests_filtered.csv", "text/csv"
        )

    with tab3:
        st.markdown(f"**{len(f_donations):,} donation records** (filtered)")
        don_display = f_donations.sort_values("donation_date", ascending=False)
        st.dataframe(don_display.reset_index(drop=True), use_container_width=True, height=450)
        st.download_button(
            "⬇ Download filtered donations CSV",
            don_display.to_csv(index=False),
            "donations_filtered.csv", "text/csv"
        )


# ── Footer ────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#aaa;font-size:12px'>"
    "🩸 Blood Donation Analytics Platform · Built with Python & Streamlit · Data: 2020–2024"
    "</div>",
    unsafe_allow_html=True
)
