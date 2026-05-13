"""
🩸 Blood Donation Analytics & Donor Intelligence Platform
=========================================================
Professional Streamlit Dashboard — Resume Edition
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date

# ──────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Blood Donation Analytics",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────
# GLOBAL CSS
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a0a0a 0%, #2d1515 50%, #1a0a0a 100%);
    border-right: 1px solid #3d1a1a;
}
section[data-testid="stSidebar"] * { color: #f0d0d0 !important; }
section[data-testid="stSidebar"] .stRadio label { 
    color: #f0d0d0 !important; font-size: 14px; 
}
section[data-testid="stSidebar"] hr { border-color: #3d1a1a !important; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #8B0000 0%, #c0392b 40%, #e74c3c 100%);
    padding: 28px 36px; border-radius: 16px; margin-bottom: 28px;
    box-shadow: 0 8px 32px rgba(192,57,43,0.35);
    position: relative; overflow: hidden;
}
.hero::before {
    content: '🩸'; font-size: 140px; position: absolute;
    right: 20px; top: -20px; opacity: 0.12;
}
.hero h1 { color: white; font-size: 26px; font-weight: 700; margin: 0 0 6px 0; letter-spacing: -0.3px; }
.hero p  { color: rgba(255,255,255,0.85); font-size: 13px; margin: 0; }
.hero-badges { display: flex; gap: 8px; margin-top: 14px; flex-wrap: wrap; }
.hero-badge {
    background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25);
    color: white; padding: 3px 12px; border-radius: 20px; font-size: 11px; font-weight: 500;
}

/* ── KPI Cards ── */
.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px,1fr)); gap: 14px; margin-bottom: 24px; }
.kpi-card {
    background: white; border-radius: 14px; padding: 18px 16px;
    border: 1px solid #f0e8e8; text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    transition: transform 0.2s, box-shadow 0.2s;
    position: relative; overflow: hidden;
}
.kpi-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
}
.kpi-card.red::before   { background: linear-gradient(90deg,#c0392b,#e74c3c); }
.kpi-card.green::before { background: linear-gradient(90deg,#27ae60,#2ecc71); }
.kpi-card.blue::before  { background: linear-gradient(90deg,#2980b9,#3498db); }
.kpi-card.orange::before{ background: linear-gradient(90deg,#d35400,#e67e22); }
.kpi-card.purple::before{ background: linear-gradient(90deg,#6c3483,#8e44ad); }
.kpi-card.teal::before  { background: linear-gradient(90deg,#148f77,#1abc9c); }
.kpi-icon  { font-size: 26px; margin-bottom: 6px; }
.kpi-value { font-size: 26px; font-weight: 700; color: #1a1a1a; line-height: 1; margin-bottom: 4px; }
.kpi-label { font-size: 11px; color: #888; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500; }
.kpi-delta { font-size: 11px; margin-top: 4px; font-weight: 500; }
.kpi-delta.up   { color: #27ae60; }
.kpi-delta.down { color: #c0392b; }

/* ── Section headers ── */
.sec-header {
    display: flex; align-items: center; gap: 10px;
    margin: 24px 0 14px 0; padding-bottom: 10px;
    border-bottom: 2px solid #f5e8e8;
}
.sec-header .icon { font-size: 18px; }
.sec-header h3 { font-size: 15px; font-weight: 600; color: #2c2c2c; margin: 0; }
.sec-header .badge {
    background: #fef0f0; color: #c0392b; font-size: 10px;
    padding: 2px 8px; border-radius: 10px; font-weight: 600; margin-left: auto;
}

/* ── Chart cards ── */
.chart-card {
    background: white; border-radius: 14px; padding: 18px 20px;
    border: 1px solid #f0e8e8; box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    margin-bottom: 16px;
}
.chart-title { font-size: 13px; font-weight: 600; color: #444; margin-bottom: 12px; }

/* ── Insight boxes ── */
.insight-row { display: grid; grid-template-columns: repeat(auto-fit,minmax(220px,1fr)); gap: 12px; margin: 16px 0; }
.insight-box {
    background: white; border-radius: 12px; padding: 14px 16px;
    border-left: 4px solid #c0392b; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.insight-box.green { border-left-color: #27ae60; }
.insight-box.blue  { border-left-color: #2980b9; }
.insight-box.orange{ border-left-color: #e67e22; }
.insight-icon  { font-size: 20px; margin-bottom: 6px; }
.insight-title { font-size: 11px; color: #999; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; }
.insight-text  { font-size: 13px; color: #333; margin-top: 3px; font-weight: 500; }

/* ── Alert boxes ── */
.alert { padding: 12px 16px; border-radius: 10px; font-size: 13px; margin: 8px 0; display: flex; align-items: flex-start; gap: 10px; }
.alert.critical { background: #fef0f0; border: 1px solid #fac5c5; color: #7b1515; }
.alert.warning  { background: #fef8ec; border: 1px solid #f9d98a; color: #7a4f00; }
.alert.success  { background: #edfaf1; border: 1px solid #a8e6be; color: #155724; }
.alert.info     { background: #eef6ff; border: 1px solid #93c5fd; color: #1e3a5f; }

/* ── Tables ── */
.styled-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.styled-table th { background: #fef0f0; color: #c0392b; font-weight: 600; padding: 10px 12px; text-align: left; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; }
.styled-table td { padding: 9px 12px; border-bottom: 1px solid #f5f5f5; color: #333; }
.styled-table tr:last-child td { border-bottom: none; }
.styled-table tr:hover td { background: #fef9f9; }

/* ── Tags/badges ── */
.tag { display: inline-block; padding: 2px 8px; border-radius: 6px; font-size: 11px; font-weight: 600; }
.tag.critical { background: #fef0f0; color: #c0392b; }
.tag.high     { background: #fef5ec; color: #d35400; }
.tag.medium   { background: #eef6ff; color: #2980b9; }
.tag.low      { background: #edfaf1; color: #27ae60; }
.tag.available   { background: #edfaf1; color: #27ae60; }
.tag.unavailable { background: #fef0f0; color: #c0392b; }
.tag.deficit  { background: #fef0f0; color: #c0392b; }
.tag.surplus  { background: #edfaf1; color: #27ae60; }

/* ── Progress bars ── */
.prog-wrap { margin: 6px 0; }
.prog-label { display: flex; justify-content: space-between; font-size: 12px; color: #555; margin-bottom: 4px; }
.prog-track { background: #f5e8e8; border-radius: 6px; height: 10px; overflow: hidden; }
.prog-fill  { height: 100%; border-radius: 6px; background: linear-gradient(90deg,#c0392b,#e74c3c); transition: width 0.5s; }
.prog-fill.green  { background: linear-gradient(90deg,#27ae60,#2ecc71); }
.prog-fill.blue   { background: linear-gradient(90deg,#2980b9,#3498db); }
.prog-fill.orange { background: linear-gradient(90deg,#d35400,#e67e22); }

/* ── Donor finder ── */
.donor-card {
    background: white; border-radius: 12px; padding: 14px 16px;
    border: 1px solid #f0e8e8; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;
}
.donor-name  { font-weight: 600; font-size: 14px; color: #1a1a1a; }
.donor-meta  { font-size: 12px; color: #888; margin-top: 2px; }
.blood-badge {
    width: 44px; height: 44px; border-radius: 50%;
    background: linear-gradient(135deg,#c0392b,#e74c3c);
    color: white; font-weight: 700; font-size: 13px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}

/* ── Footer ── */
.footer {
    text-align: center; padding: 20px; margin-top: 32px;
    border-top: 1px solid #f5e8e8; color: #bbb; font-size: 12px;
}

/* ── Streamlit overrides ── */
div[data-testid="metric-container"] {
    background: white; border-radius: 12px; padding: 14px 16px;
    border: 1px solid #f0e8e8; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
div[data-testid="stMetricValue"] > div { font-size: 22px !important; font-weight: 700 !important; }
.stDataFrame { border-radius: 10px; overflow: hidden; }
div[data-testid="stExpander"] { border-radius: 10px; border: 1px solid #f0e8e8; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# DATA LOADING
# ──────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    donors    = pd.read_csv("data/cleaned/donors_clean.csv",           parse_dates=["last_donation_date"])
    requests  = pd.read_csv("data/cleaned/blood_requests_clean.csv",   parse_dates=["request_date"])
    donations = pd.read_csv("data/cleaned/donation_records_clean.csv", parse_dates=["donation_date"])

    # Feature engineering
    today = pd.Timestamp("2025-01-01")
    donors["days_since_donation"] = (today - donors["last_donation_date"]).dt.days
    donors["age_group"] = pd.cut(donors["age"], bins=[17,25,35,45,55,65],
                                  labels=["18-25","26-35","36-45","46-55","56-65"])
    donations["year"]  = donations["donation_date"].dt.year
    donations["month"] = donations["donation_date"].dt.to_period("M")
    requests["year"]   = requests["request_date"].dt.year
    requests["month"]  = requests["request_date"].dt.to_period("M")
    requests["quarter"]= requests["request_date"].dt.to_period("Q")
    return donors, requests, donations

with st.spinner("Loading analytics platform..."):
    donors, requests, donations = load_data()

BLOOD_GROUPS   = ["A+","A-","B+","B-","AB+","AB-","O+","O-"]
URGENCY_LEVELS = ["Critical","High","Medium","Low"]
URGENCY_COLORS = {"Critical":"#c0392b","High":"#e67e22","Medium":"#3498db","Low":"#27ae60"}
BG_COLORS      = {"O+":"#e74c3c","A+":"#e67e22","B+":"#f39c12","AB+":"#9b59b6",
                   "O-":"#c0392b","A-":"#d35400","B-":"#e74c3c","AB-":"#6c3483"}


# ──────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:16px 0 8px 0'>
      <div style='font-size:40px'>🩸</div>
      <div style='font-size:14px;font-weight:700;color:#ff6b6b;margin-top:4px'>Blood Analytics</div>
      <div style='font-size:10px;color:#cc8888;margin-top:2px'>Donor Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    page = st.radio("", [
        "🏠  Executive Dashboard",
        "🩸  Blood Demand Analysis",
        "👥  Donor Intelligence",
        "🔍  Donor Finder",
        "🏙️  City & Regional Insights",
        "⚠️  Shortage Alert Center",
        "📊  Data Explorer",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("<div style='font-size:12px;color:#cc8888;font-weight:600'>GLOBAL FILTERS</div>", unsafe_allow_html=True)

    sel_bg = st.multiselect("Blood Groups", BLOOD_GROUPS, default=BLOOD_GROUPS)
    sel_urgency = st.multiselect("Urgency Levels", URGENCY_LEVELS, default=URGENCY_LEVELS)
    sel_year = st.multiselect("Year", [2020,2021,2022,2023,2024], default=[2020,2021,2022,2023,2024])

    st.markdown("---")
    total_donors    = len(donors)
    avail_donors    = (donors["availability_status"]=="Available").sum()
    total_units_gap = requests["units_required"].sum() - donations["units_donated"].sum()
    st.markdown(f"""
    <div style='font-size:11px;color:#cc8888;line-height:2'>
    📋 <b style='color:#ff9999'>{total_donors:,}</b> total donors<br>
    ✅ <b style='color:#88cc88'>{avail_donors:,}</b> available now<br>
    ⚠️ <b style='color:#ffaa88'>{total_units_gap:,}</b> units deficit
    </div>
    """, unsafe_allow_html=True)


# ── Filtered data ─────────────────────────────────────────────
fd = donors[donors["blood_group"].isin(sel_bg)]
fr = requests[requests["blood_group"].isin(sel_bg) &
              requests["urgency_level"].isin(sel_urgency) &
              requests["year"].isin(sel_year)]
fdon = donations[donations["blood_group"].isin(sel_bg) &
                 donations["year"].isin(sel_year)]


# ──────────────────────────────────────────────────────────────
# HERO BANNER (all pages)
# ──────────────────────────────────────────────────────────────
page_name = page.split("  ")[1] if "  " in page else page
st.markdown(f"""
<div class="hero">
  <h1>🩸 Blood Donation Analytics & Donor Intelligence Platform</h1>
  <p>Real-time analytics across 5,000+ donors · 2,000+ hospital requests · 3,500+ donation events · 50 Indian cities</p>
  <div class="hero-badges">
    <span class="hero-badge">📍 50 Cities</span>
    <span class="hero-badge">🏥 25 Hospitals</span>
    <span class="hero-badge">🩸 8 Blood Groups</span>
    <span class="hero-badge">📅 2020–2024</span>
    <span class="hero-badge">⚡ Live Filters</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 1: EXECUTIVE DASHBOARD
# ══════════════════════════════════════════════════════════════
if "Executive" in page:

    # ── KPI Row 1 ─────────────────────────────────────────────
    k1,k2,k3,k4,k5,k6 = st.columns(6)
    avail_pct = (fd["availability_status"]=="Available").sum()/max(len(fd),1)*100
    crit_pct  = (fr["urgency_level"]=="Critical").sum()/max(len(fr),1)*100
    deficit   = max(0, fr["units_required"].sum() - fdon["units_donated"].sum())

    with k1:
        st.markdown(f"""<div class="kpi-card red">
        <div class="kpi-icon">👥</div>
        <div class="kpi-value">{len(fd):,}</div>
        <div class="kpi-label">Total Donors</div>
        <div class="kpi-delta up">↑ Registered</div></div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class="kpi-card green">
        <div class="kpi-icon">✅</div>
        <div class="kpi-value">{(fd["availability_status"]=="Available").sum():,}</div>
        <div class="kpi-label">Available Now</div>
        <div class="kpi-delta up">↑ {avail_pct:.1f}% rate</div></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class="kpi-card blue">
        <div class="kpi-icon">🏥</div>
        <div class="kpi-value">{len(fr):,}</div>
        <div class="kpi-label">Blood Requests</div>
        <div class="kpi-delta down">⚠️ {crit_pct:.1f}% critical</div></div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class="kpi-card orange">
        <div class="kpi-icon">📦</div>
        <div class="kpi-value">{fr["units_required"].sum():,}</div>
        <div class="kpi-label">Units Demanded</div>
        <div class="kpi-delta down">↑ Total need</div></div>""", unsafe_allow_html=True)
    with k5:
        st.markdown(f"""<div class="kpi-card purple">
        <div class="kpi-icon">💉</div>
        <div class="kpi-value">{fdon["units_donated"].sum():,}</div>
        <div class="kpi-label">Units Donated</div>
        <div class="kpi-delta up">↑ Total supply</div></div>""", unsafe_allow_html=True)
    with k6:
        st.markdown(f"""<div class="kpi-card teal">
        <div class="kpi-icon">⚠️</div>
        <div class="kpi-value" style="color:#c0392b">{deficit:,}</div>
        <div class="kpi-label">Units Deficit</div>
        <div class="kpi-delta down">↓ Gap to fill</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 2: Charts ─────────────────────────────────────────
    col1, col2, col3 = st.columns([2,2,1.5])

    with col1:
        st.markdown('<div class="sec-header"><span class="icon">📊</span><h3>Supply vs Demand by Blood Group</h3><span class="badge">Key Insight</span></div>', unsafe_allow_html=True)
        supply = fdon.groupby("blood_group")["units_donated"].sum().rename("Supply")
        demand = fr.groupby("blood_group")["units_required"].sum().rename("Demand")
        svd    = pd.concat([supply,demand],axis=1).fillna(0).astype(int)
        svd    = svd.reindex(BLOOD_GROUPS).fillna(0)
        st.bar_chart(svd, color=["#27ae60","#c0392b"], height=280)

    with col2:
        st.markdown('<div class="sec-header"><span class="icon">📈</span><h3>Monthly Donation Trend</h3><span class="badge">2020–2024</span></div>', unsafe_allow_html=True)
        monthly = fdon.groupby("month")["units_donated"].sum().reset_index()
        monthly["month"] = monthly["month"].astype(str)
        monthly = monthly.set_index("month")
        st.area_chart(monthly, color="#c0392b", height=280)

    with col3:
        st.markdown('<div class="sec-header"><span class="icon">🚨</span><h3>Urgency Split</h3></div>', unsafe_allow_html=True)
        urg = fr["urgency_level"].value_counts()
        for level in URGENCY_LEVELS:
            count = urg.get(level,0)
            pct   = count/max(len(fr),1)*100
            st.markdown(f"""
            <div class="prog-wrap">
              <div class="prog-label"><span>{level}</span><span>{count:,} ({pct:.0f}%)</span></div>
              <div class="prog-track"><div class="prog-fill {'green' if level=='Low' else 'blue' if level=='Medium' else 'orange' if level=='High' else ''}" style="width:{pct}%"></div></div>
            </div>""", unsafe_allow_html=True)

    # ── Row 3: Insights ───────────────────────────────────────
    st.markdown('<div class="sec-header"><span class="icon">💡</span><h3>Key Insights</h3></div>', unsafe_allow_html=True)

    most_demanded = fr.groupby("blood_group")["units_required"].sum().idxmax() if len(fr)>0 else "N/A"
    top_city      = fd["city"].value_counts().idxmax() if len(fd)>0 else "N/A"
    repeat_donors = (fdon["donor_id"].value_counts()>1).sum()
    never_donated = fd["last_donation_date"].isna().sum()

    i1,i2,i3,i4 = st.columns(4)
    with i1:
        st.markdown(f"""<div class="insight-box">
        <div class="insight-icon">🔴</div>
        <div class="insight-title">Most Demanded</div>
        <div class="insight-text"><b>{most_demanded}</b> blood group — highest units requested across all hospitals</div>
        </div>""", unsafe_allow_html=True)
    with i2:
        st.markdown(f"""<div class="insight-box green">
        <div class="insight-icon">✅</div>
        <div class="insight-title">Availability Rate</div>
        <div class="insight-text"><b>{avail_pct:.1f}%</b> of donors currently available — strong donor base</div>
        </div>""", unsafe_allow_html=True)
    with i3:
        st.markdown(f"""<div class="insight-box blue">
        <div class="insight-icon">🔁</div>
        <div class="insight-title">Repeat Donors</div>
        <div class="insight-text"><b>{repeat_donors:,}</b> donors have donated more than once — high retention</div>
        </div>""", unsafe_allow_html=True)
    with i4:
        st.markdown(f"""<div class="insight-box orange">
        <div class="insight-icon">📍</div>
        <div class="insight-title">Top Donor City</div>
        <div class="insight-text"><b>{top_city}</b> leads in donor registrations across India</div>
        </div>""", unsafe_allow_html=True)

    # ── Row 4: Blood group distribution ──────────────────────
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="sec-header"><span class="icon">🩸</span><h3>Donor Distribution by Blood Group</h3></div>', unsafe_allow_html=True)
        bg_donors = fd["blood_group"].value_counts().reindex(BLOOD_GROUPS,fill_value=0)
        total_bg  = bg_donors.sum()
        html = '<table class="styled-table"><tr><th>Blood Group</th><th>Donors</th><th>Share</th><th>Availability</th></tr>'
        for bg, cnt in bg_donors.items():
            avail_cnt = fd[(fd["blood_group"]==bg)&(fd["availability_status"]=="Available")].shape[0]
            pct = cnt/max(total_bg,1)*100
            html += f'<tr><td><b>{bg}</b></td><td>{cnt:,}</td><td>{pct:.1f}%</td><td><span class="tag available">{avail_cnt} avail</span></td></tr>'
        html += '</table>'
        st.markdown(html, unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="sec-header"><span class="icon">📅</span><h3>Yearly Donation Summary</h3></div>', unsafe_allow_html=True)
        yearly = fdon.groupby("year").agg(
            Donations=("donation_id","count"),
            Units=("units_donated","sum"),
            Donors=("donor_id","nunique")
        )
        st.dataframe(yearly, use_container_width=True, height=250)


# ══════════════════════════════════════════════════════════════
# PAGE 2: BLOOD DEMAND ANALYSIS
# ══════════════════════════════════════════════════════════════
elif "Blood Demand" in page:

    k1,k2,k3,k4,k5 = st.columns(5)
    with k1:
        st.markdown(f"""<div class="kpi-card red"><div class="kpi-icon">📋</div>
        <div class="kpi-value">{len(fr):,}</div><div class="kpi-label">Total Requests</div></div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class="kpi-card orange"><div class="kpi-icon">📦</div>
        <div class="kpi-value">{fr["units_required"].sum():,}</div><div class="kpi-label">Units Needed</div></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class="kpi-card red"><div class="kpi-icon">🚨</div>
        <div class="kpi-value">{(fr["urgency_level"]=="Critical").sum():,}</div><div class="kpi-label">Critical</div></div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class="kpi-card blue"><div class="kpi-icon">🏥</div>
        <div class="kpi-value">{fr["hospital_name"].nunique():,}</div><div class="kpi-label">Hospitals</div></div>""", unsafe_allow_html=True)
    with k5:
        avg_u = fr["units_required"].mean()
        st.markdown(f"""<div class="kpi-card green"><div class="kpi-icon">📊</div>
        <div class="kpi-value">{avg_u:.1f}</div><div class="kpi-label">Avg Units/Req</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="sec-header"><span class="icon">🩸</span><h3>Units Demanded by Blood Group</h3><span class="badge">Ranked</span></div>', unsafe_allow_html=True)
        bg_d = fr.groupby("blood_group")["units_required"].sum().sort_values(ascending=False)
        max_d = bg_d.max()
        for bg, val in bg_d.items():
            pct = val/max(max_d,1)*100
            st.markdown(f"""<div class="prog-wrap">
            <div class="prog-label"><span><b>{bg}</b></span><span>{val:,} units</span></div>
            <div class="prog-track"><div class="prog-fill" style="width:{pct}%"></div></div>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="sec-header"><span class="icon">🚨</span><h3>Urgency by Blood Group</h3></div>', unsafe_allow_html=True)
        urg_bg = fr.groupby(["blood_group","urgency_level"]).size().unstack(fill_value=0)
        urg_bg = urg_bg.reindex(columns=[c for c in URGENCY_LEVELS if c in urg_bg.columns])
        st.bar_chart(urg_bg, height=300)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="sec-header"><span class="icon">📈</span><h3>Monthly Request Trend</h3></div>', unsafe_allow_html=True)
        monthly_r = fr.groupby("month").agg(Requests=("request_id","count"), Units=("units_required","sum")).reset_index()
        monthly_r["month"] = monthly_r["month"].astype(str)
        st.line_chart(monthly_r.set_index("month"), height=250)

    with col4:
        st.markdown('<div class="sec-header"><span class="icon">🏥</span><h3>Top 10 Requesting Hospitals</h3></div>', unsafe_allow_html=True)
        top_h = fr.groupby("hospital_name").agg(
            Requests=("request_id","count"),
            Units=("units_required","sum"),
            Critical=("urgency_level", lambda x:(x=="Critical").sum())
        ).sort_values("Units",ascending=False).head(10)
        st.dataframe(top_h, use_container_width=True, height=280)

    st.markdown('<div class="sec-header"><span class="icon">🏙️</span><h3>Top 20 Cities by Blood Demand</h3></div>', unsafe_allow_html=True)
    city_d = fr.groupby("city")["units_required"].sum().sort_values(ascending=False).head(20)
    st.bar_chart(city_d, color="#c0392b", height=280)


# ══════════════════════════════════════════════════════════════
# PAGE 3: DONOR INTELLIGENCE
# ══════════════════════════════════════════════════════════════
elif "Donor Intelligence" in page:

    k1,k2,k3,k4,k5 = st.columns(5)
    never_don = fd["last_donation_date"].isna().sum()
    avg_age   = fd["age"].mean()
    repeat_d  = (fdon["donor_id"].value_counts()>1).sum()

    with k1:
        st.markdown(f"""<div class="kpi-card red"><div class="kpi-icon">👥</div>
        <div class="kpi-value">{len(fd):,}</div><div class="kpi-label">Total Donors</div></div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class="kpi-card green"><div class="kpi-icon">✅</div>
        <div class="kpi-value">{(fd["availability_status"]=="Available").sum():,}</div><div class="kpi-label">Available</div></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class="kpi-card blue"><div class="kpi-icon">🎂</div>
        <div class="kpi-value">{avg_age:.1f}</div><div class="kpi-label">Avg Age</div></div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class="kpi-card purple"><div class="kpi-icon">🔁</div>
        <div class="kpi-value">{repeat_d:,}</div><div class="kpi-label">Repeat Donors</div></div>""", unsafe_allow_html=True)
    with k5:
        st.markdown(f"""<div class="kpi-card orange"><div class="kpi-icon">😴</div>
        <div class="kpi-value">{never_don:,}</div><div class="kpi-label">Never Donated</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="sec-header"><span class="icon">🎂</span><h3>Age Group Distribution</h3></div>', unsafe_allow_html=True)
        age_g = fd["age_group"].value_counts().sort_index()
        st.bar_chart(age_g, color="#8e44ad", height=220)

    with col2:
        st.markdown('<div class="sec-header"><span class="icon">⚧</span><h3>Gender Distribution</h3></div>', unsafe_allow_html=True)
        gen = fd["gender"].value_counts()
        st.bar_chart(gen, color="#2980b9", height=220)

    with col3:
        st.markdown('<div class="sec-header"><span class="icon">✅</span><h3>Availability by Blood Group</h3></div>', unsafe_allow_html=True)
        avail_bg = fd.groupby("blood_group")["availability_status"].apply(
            lambda x: round((x=="Available").sum()/max(len(x),1)*100,1)
        ).sort_values(ascending=False)
        for bg, pct in avail_bg.items():
            color = "green" if pct>95 else "blue" if pct>90 else "orange"
            st.markdown(f"""<div class="prog-wrap">
            <div class="prog-label"><span><b>{bg}</b></span><span>{pct}%</span></div>
            <div class="prog-track"><div class="prog-fill {color}" style="width:{pct}%"></div></div>
            </div>""", unsafe_allow_html=True)

    col4, col5 = st.columns(2)

    with col4:
        st.markdown('<div class="sec-header"><span class="icon">💉</span><h3>Monthly Donations Trend</h3></div>', unsafe_allow_html=True)
        monthly_don = fdon.groupby("month")["units_donated"].sum().reset_index()
        monthly_don["month"] = monthly_don["month"].astype(str)
        st.area_chart(monthly_don.set_index("month"), color="#27ae60", height=250)

    with col5:
        st.markdown('<div class="sec-header"><span class="icon">🏆</span><h3>Top 15 Most Active Donors</h3></div>', unsafe_allow_html=True)
        top_don = fdon.groupby("donor_id").agg(
            Donations=("donation_id","count"),
            Units=("units_donated","sum")
        ).sort_values("Donations",ascending=False).head(15)
        top_don = top_don.merge(donors[["donor_id","name","blood_group","city"]], on="donor_id", how="left")
        st.dataframe(top_don[["name","blood_group","city","Donations","Units"]], use_container_width=True, height=280)

    # Geo map
    st.markdown('<div class="sec-header"><span class="icon">🗺️</span><h3>Donor Geographic Distribution</h3></div>', unsafe_allow_html=True)
    map_df = fd[["latitude","longitude"]].dropna().rename(columns={"latitude":"lat","longitude":"lon"})
    if len(map_df)>0:
        st.map(map_df, zoom=4)


# ══════════════════════════════════════════════════════════════
# PAGE 4: DONOR FINDER (Most Useful Feature)
# ══════════════════════════════════════════════════════════════
elif "Donor Finder" in page:

    st.markdown("""
    <div class="alert info">
    <span>🔍</span>
    <span>Use the Donor Finder to instantly locate available blood donors by blood group, city, gender and age range. Perfect for emergency matching.</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-header"><span class="icon">🔍</span><h3>Search Criteria</h3></div>', unsafe_allow_html=True)

    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        find_bg   = st.selectbox("Blood Group Required", ["Any"] + BLOOD_GROUPS)
    with fc2:
        find_city = st.selectbox("City", ["Any"] + sorted(donors["city"].unique().tolist()))
    with fc3:
        find_gender = st.selectbox("Gender", ["Any","Male","Female","Other"])
    with fc4:
        age_range = st.slider("Age Range", 18, 65, (18, 65))

    find_avail = st.checkbox("Show only AVAILABLE donors", value=True)

    # Apply search
    result = donors.copy()
    if find_bg    != "Any": result = result[result["blood_group"]        == find_bg]
    if find_city  != "Any": result = result[result["city"]               == find_city]
    if find_gender!= "Any": result = result[result["gender"]             == find_gender]
    if find_avail:           result = result[result["availability_status"]== "Available"]
    result = result[(result["age"] >= age_range[0]) & (result["age"] <= age_range[1])]
    result = result.sort_values("last_donation_date", ascending=True, na_position="last")

    # Results
    col_r, col_s = st.columns([3,1])
    with col_r:
        st.markdown(f'<div class="sec-header"><span class="icon">👥</span><h3>Search Results</h3><span class="badge">{len(result):,} donors found</span></div>', unsafe_allow_html=True)

    with col_s:
        if len(result) > 0:
            st.download_button(
                "⬇ Download Results",
                result.to_csv(index=False),
                "donor_search_results.csv", "text/csv",
                use_container_width=True
            )

    if len(result) == 0:
        st.markdown("""<div class="alert warning"><span>⚠️</span>
        <span>No donors found matching your criteria. Try adjusting the filters.</span></div>""", unsafe_allow_html=True)
    else:
        # Show first 20 as cards
        display_count = min(20, len(result))
        for _, row in result.head(display_count).iterrows():
            last_don = row["last_donation_date"]
            last_don_str = last_don.strftime("%d %b %Y") if pd.notna(last_don) else "Never donated"
            days_ago = row.get("days_since_donation", None)
            days_str = f"{int(days_ago)} days ago" if pd.notna(days_ago) else "—"
            avail_tag = "available" if row["availability_status"]=="Available" else "unavailable"
            st.markdown(f"""
            <div class="donor-card">
              <div class="blood-badge">{row['blood_group']}</div>
              <div style="flex:1;padding:0 14px">
                <div class="donor-name">{row['name']}</div>
                <div class="donor-meta">🎂 Age {int(row['age'])} &nbsp;|&nbsp; ⚧ {row['gender']} &nbsp;|&nbsp; 📍 {row['city']}, {row['state']}</div>
                <div class="donor-meta">💉 Last donation: {last_don_str} ({days_str})</div>
              </div>
              <span class="tag {avail_tag}">{row['availability_status']}</span>
            </div>
            """, unsafe_allow_html=True)

        if len(result) > 20:
            st.info(f"Showing top 20 of {len(result):,} results. Download CSV to see all.")

        # Stats for search results
        st.markdown('<div class="sec-header"><span class="icon">📊</span><h3>Search Result Summary</h3></div>', unsafe_allow_html=True)
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Found",     f"{len(result):,}")
        s2.metric("Available", f"{(result['availability_status']=='Available').sum():,}")
        s3.metric("Avg Age",   f"{result['age'].mean():.1f}")
        s4.metric("Cities",    f"{result['city'].nunique():,}")


# ══════════════════════════════════════════════════════════════
# PAGE 5: CITY & REGIONAL INSIGHTS
# ══════════════════════════════════════════════════════════════
elif "City" in page:

    k1,k2,k3,k4 = st.columns(4)
    with k1:
        st.markdown(f"""<div class="kpi-card blue"><div class="kpi-icon">🏙️</div>
        <div class="kpi-value">{fd["city"].nunique()}</div><div class="kpi-label">Cities</div></div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class="kpi-card red"><div class="kpi-icon">🗺️</div>
        <div class="kpi-value">{fd["state"].nunique()}</div><div class="kpi-label">States</div></div>""", unsafe_allow_html=True)
    with k3:
        top_c = fd["city"].value_counts().idxmax()
        st.markdown(f"""<div class="kpi-card green"><div class="kpi-icon">🏆</div>
        <div class="kpi-value" style="font-size:16px">{top_c}</div><div class="kpi-label">Top Donor City</div></div>""", unsafe_allow_html=True)
    with k4:
        top_r = fr["city"].value_counts().idxmax() if len(fr)>0 else "N/A"
        st.markdown(f"""<div class="kpi-card orange"><div class="kpi-icon">🏥</div>
        <div class="kpi-value" style="font-size:16px">{top_r}</div><div class="kpi-label">Top Request City</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="sec-header"><span class="icon">👥</span><h3>Top 15 Cities — Donor Count</h3></div>', unsafe_allow_html=True)
        st.bar_chart(fd["city"].value_counts().head(15), color="#2980b9", height=300)

    with col2:
        st.markdown('<div class="sec-header"><span class="icon">📦</span><h3>Top 15 Cities — Units Demanded</h3></div>', unsafe_allow_html=True)
        st.bar_chart(fr.groupby("city")["units_required"].sum().sort_values(ascending=False).head(15), color="#c0392b", height=300)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="sec-header"><span class="icon">🚨</span><h3>Critical Requests by City (Top 10)</h3></div>', unsafe_allow_html=True)
        crit_c = fr[fr["urgency_level"]=="Critical"]["city"].value_counts().head(10)
        st.bar_chart(crit_c, color="#e74c3c", height=260)

    with col4:
        st.markdown('<div class="sec-header"><span class="icon">🗺️</span><h3>Top 10 States by Donor Count</h3></div>', unsafe_allow_html=True)
        state_d = fd["state"].value_counts().head(10)
        st.bar_chart(state_d, color="#8e44ad", height=260)

    # Full city table
    st.markdown('<div class="sec-header"><span class="icon">📋</span><h3>Complete City Analysis Table</h3></div>', unsafe_allow_html=True)
    city_table = fd.groupby(["city","state"]).agg(
        Total_Donors=("donor_id","count"),
        Available=("availability_status", lambda x:(x=="Available").sum()),
        Avg_Age=("age","mean")
    ).round(1).sort_values("Total_Donors",ascending=False)
    city_table["Availability_%"] = (city_table["Available"]/city_table["Total_Donors"]*100).round(1)
    demand_by_city = fr.groupby("city")["units_required"].sum().rename("Units_Demanded")
    city_table = city_table.join(demand_by_city, how="left").fillna(0)
    city_table["Units_Demanded"] = city_table["Units_Demanded"].astype(int)
    st.dataframe(city_table, use_container_width=True, height=400)
    st.download_button("⬇ Download City Analysis", city_table.to_csv(), "city_analysis.csv","text/csv")


# ══════════════════════════════════════════════════════════════
# PAGE 6: SHORTAGE ALERT CENTER
# ══════════════════════════════════════════════════════════════
elif "Shortage" in page:

    st.markdown("""
    <div class="alert critical">
    <span>🚨</span>
    <span><b>Shortage Alert Center</b> — This page identifies critical blood supply gaps that need immediate attention from blood banks and hospital administrators.</span>
    </div>
    """, unsafe_allow_html=True)

    supply = fdon.groupby("blood_group")["units_donated"].sum().rename("Supplied")
    demand = fr.groupby("blood_group")["units_required"].sum().rename("Demanded")
    svd    = pd.concat([supply,demand],axis=1).fillna(0).astype(int)
    svd["Gap"]        = svd["Demanded"] - svd["Supplied"]
    svd["Coverage_%"] = (svd["Supplied"]/svd["Demanded"].replace(0,1)*100).round(1)
    svd["Status"]     = svd["Gap"].apply(lambda x: "🔴 DEFICIT" if x>0 else "🟢 SURPLUS")
    svd["Severity"]   = svd["Gap"].apply(
        lambda x: "Critical" if x>1000 else "High" if x>500 else "Medium" if x>0 else "OK"
    )
    svd = svd.sort_values("Gap", ascending=False)

    # KPIs
    deficit_groups  = (svd["Gap"]>0).sum()
    total_deficit   = svd[svd["Gap"]>0]["Gap"].sum()
    worst_bg        = svd["Gap"].idxmax() if len(svd)>0 else "N/A"
    coverage_avg    = svd["Coverage_%"].mean()

    k1,k2,k3,k4 = st.columns(4)
    with k1:
        st.markdown(f"""<div class="kpi-card red"><div class="kpi-icon">🔴</div>
        <div class="kpi-value">{deficit_groups}</div><div class="kpi-label">Groups in Deficit</div></div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class="kpi-card orange"><div class="kpi-icon">📉</div>
        <div class="kpi-value">{total_deficit:,}</div><div class="kpi-label">Total Units Deficit</div></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class="kpi-card red"><div class="kpi-icon">⚠️</div>
        <div class="kpi-value">{worst_bg}</div><div class="kpi-label">Worst Shortage</div></div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class="kpi-card blue"><div class="kpi-icon">📊</div>
        <div class="kpi-value">{coverage_avg:.1f}%</div><div class="kpi-label">Avg Coverage</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Alert cards per blood group
    st.markdown('<div class="sec-header"><span class="icon">🚨</span><h3>Blood Group Alert Status</h3></div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, (bg, row) in enumerate(svd.iterrows()):
        with cols[i % 4]:
            gap    = int(row["Gap"])
            sev    = row["Severity"]
            cov    = row["Coverage_%"]
            color  = "#c0392b" if gap>0 else "#27ae60"
            bg_col = "#fef0f0" if gap>0 else "#edfaf1"
            border = "#fac5c5" if gap>0 else "#a8e6be"
            icon   = "🔴" if sev=="Critical" else "🟠" if sev=="High" else "🟡" if sev=="Medium" else "🟢"
            st.markdown(f"""
            <div style="background:{bg_col};border:1px solid {border};border-radius:12px;padding:14px;margin-bottom:10px;text-align:center">
              <div style="font-size:24px;font-weight:800;color:{color}">{bg}</div>
              <div style="font-size:11px;color:#888;margin:4px 0">Coverage: <b>{cov}%</b></div>
              <div style="font-size:12px;color:{color};font-weight:600">{icon} {abs(gap):,} {'deficit' if gap>0 else 'surplus'}</div>
              <div style="font-size:10px;color:#aaa;margin-top:4px">{sev} severity</div>
            </div>""", unsafe_allow_html=True)

    # Shortage table
    st.markdown('<div class="sec-header"><span class="icon">📋</span><h3>Full Shortage Analysis Table</h3></div>', unsafe_allow_html=True)
    st.dataframe(svd, use_container_width=True)

    # Critical city-level shortages
    st.markdown('<div class="sec-header"><span class="icon">🏙️</span><h3>Cities with Most Critical Requests Unmatched</h3></div>', unsafe_allow_html=True)
    crit_city = fr[fr["urgency_level"]=="Critical"].groupby("city").agg(
        Critical_Requests=("request_id","count"),
        Units_Needed=("units_required","sum")
    ).sort_values("Critical_Requests",ascending=False).head(15)
    st.dataframe(crit_city, use_container_width=True)
    st.download_button("⬇ Download Shortage Report", svd.to_csv(), "shortage_report.csv","text/csv")


# ══════════════════════════════════════════════════════════════
# PAGE 7: DATA EXPLORER
# ══════════════════════════════════════════════════════════════
elif "Data Explorer" in page:

    tab1, tab2, tab3 = st.tabs(["🧑 Donors Database", "🏥 Blood Requests", "💉 Donation Records"])

    with tab1:
        st.markdown(f"**{len(fd):,} donor records** — search, filter and download")
        c1,c2,c3 = st.columns(3)
        with c1: search   = st.text_input("🔍 Search name / city")
        with c2: avf      = st.selectbox("Availability",["All","Available","Unavailable"])
        with c3: gender_f = st.selectbox("Gender",["All","Male","Female","Other"])

        disp = fd.copy()
        if search:   disp = disp[disp["name"].str.contains(search,case=False,na=False)|disp["city"].str.contains(search,case=False,na=False)]
        if avf  !="All": disp = disp[disp["availability_status"]==avf]
        if gender_f!="All": disp = disp[disp["gender"]==gender_f]

        st.markdown(f"*Showing {len(disp):,} records*")
        st.dataframe(disp.drop(columns=["age_group","days_since_donation"],errors="ignore").reset_index(drop=True), use_container_width=True, height=420)
        st.download_button("⬇ Download Filtered Data", disp.to_csv(index=False), "donors_filtered.csv","text/csv")

    with tab2:
        c1,c2 = st.columns(2)
        with c1: uf = st.selectbox("Urgency",["All"]+URGENCY_LEVELS)
        with c2: hf = st.selectbox("Hospital",["All"]+sorted(fr["hospital_name"].unique().tolist()))

        rd = fr.copy()
        if uf!="All": rd = rd[rd["urgency_level"]==uf]
        if hf!="All": rd = rd[rd["hospital_name"]==hf]
        rd = rd.sort_values("request_date",ascending=False)
        st.markdown(f"*Showing {len(rd):,} records*")
        st.dataframe(rd.drop(columns=["month","year","quarter"],errors="ignore").reset_index(drop=True), use_container_width=True, height=420)
        st.download_button("⬇ Download Filtered Data", rd.to_csv(index=False), "requests_filtered.csv","text/csv")

    with tab3:
        dd = fdon.sort_values("donation_date",ascending=False)
        st.markdown(f"*Showing {len(dd):,} records*")
        st.dataframe(dd.drop(columns=["month","year"],errors="ignore").reset_index(drop=True), use_container_width=True, height=420)
        st.download_button("⬇ Download Data", dd.to_csv(index=False), "donations.csv","text/csv")


# ── Footer ────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  🩸 <b>Blood Donation Analytics & Donor Intelligence Platform</b><br>
  Built with Python · Pandas · Streamlit &nbsp;|&nbsp; Data: 2020–2024 &nbsp;|&nbsp; 50 Indian Cities
</div>
""", unsafe_allow_html=True)
