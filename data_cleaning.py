"""
Blood Donation Analytics & Donor Intelligence Platform
=======================================================
data_cleaning.py  —  Cleans & standardises all raw datasets
Author: Data Analytics Team
"""

import pandas as pd
import numpy as np
import os

RAW_DIR     = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw")
CLEANED_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "cleaned")
os.makedirs(CLEANED_DIR, exist_ok=True)

VALID_BLOOD_GROUPS = {"A+","A-","B+","B-","AB+","AB-","O+","O-"}
VALID_GENDERS      = {"Male","Female","Other"}
VALID_URGENCY      = {"Critical","High","Medium","Low"}
VALID_AVAIL        = {"Available","Unavailable"}


# ─────────────────────────────────────────────
# UTILITY
# ─────────────────────────────────────────────
def report(label, before, after):
    print(f"  [{label}]  rows: {before:,} → {after:,}  (dropped {before-after:,})")


def print_section(title):
    print(f"\n{'='*55}")
    print(f"  {title}")
    print(f"{'='*55}")


# ─────────────────────────────────────────────
# DONORS
# ─────────────────────────────────────────────
def clean_donors(path):
    print_section("Cleaning: donors.csv")
    df = pd.read_csv(path)
    n0 = len(df)
    print(f"  Raw rows: {n0:,}")
    print(f"  Columns : {list(df.columns)}")

    # --- Missing values summary ---
    mv = df.isnull().sum()
    print("\n  Missing values (before cleaning):")
    print(mv[mv > 0].to_string())

    # Drop full duplicates
    df.drop_duplicates(inplace=True)
    report("Drop duplicates", n0, len(df))

    # Drop rows where donor_id is null (primary key)
    df.dropna(subset=["donor_id"], inplace=True)

    # Age: fill missing with median; clip 18–65
    median_age = df["age"].median()
    df["age"] = df["age"].fillna(median_age).clip(18, 65).astype(int)

    # Gender: fill missing with 'Unknown'
    df["gender"] = df["gender"].fillna("Unknown").str.strip().str.title()
    df.loc[~df["gender"].isin(VALID_GENDERS | {"Unknown"}), "gender"] = "Unknown"

    # Blood group: standardise format (e.g. "a+" -> "A+")
    df["blood_group"] = df["blood_group"].str.strip().str.upper()
    invalid_bg = ~df["blood_group"].isin(VALID_BLOOD_GROUPS)
    print(f"\n  Invalid blood groups found: {invalid_bg.sum()}")
    df = df[~invalid_bg]

    # City / State: title-case strip
    df["city"]  = df["city"].str.strip().str.title()
    df["state"] = df["state"].str.strip().str.title()

    # last_donation_date: parse; fill NaT with a sentinel "Never"
    df["last_donation_date"] = pd.to_datetime(df["last_donation_date"], errors="coerce")
    # Remove dates in the future
    today = pd.Timestamp("2025-01-01")
    future_mask = df["last_donation_date"] > today
    print(f"  Future donation dates removed: {future_mask.sum()}")
    df.loc[future_mask, "last_donation_date"] = pd.NaT

    # availability_status: standardise
    df["availability_status"] = df["availability_status"].fillna("Available")
    df.loc[~df["availability_status"].isin(VALID_AVAIL), "availability_status"] = "Available"

    # Coordinates: drop rows where lat/lon are missing or clearly wrong
    df.dropna(subset=["latitude","longitude"], inplace=True)
    df = df[(df["latitude"].between(8, 37)) & (df["longitude"].between(68, 97))]

    # Format last_donation_date back to string for export
    df["last_donation_date"] = df["last_donation_date"].dt.strftime("%Y-%m-%d")

    # Reset index
    df.reset_index(drop=True, inplace=True)

    print(f"\n  Final clean rows: {len(df):,}")
    print(f"  Missing values (after cleaning):\n{df.isnull().sum()[df.isnull().sum()>0].to_string()}")
    return df


# ─────────────────────────────────────────────
# BLOOD REQUESTS
# ─────────────────────────────────────────────
def clean_requests(path):
    print_section("Cleaning: blood_requests.csv")
    df = pd.read_csv(path)
    n0 = len(df)
    print(f"  Raw rows: {n0:,}")

    df.drop_duplicates(inplace=True)
    df.dropna(subset=["request_id"], inplace=True)

    df["blood_group"] = df["blood_group"].str.strip().str.upper()
    df = df[df["blood_group"].isin(VALID_BLOOD_GROUPS)]

    df["units_required"] = pd.to_numeric(df["units_required"], errors="coerce")
    df.dropna(subset=["units_required"], inplace=True)
    df = df[df["units_required"].between(1, 20)]
    df["units_required"] = df["units_required"].astype(int)

    df["urgency_level"] = df["urgency_level"].str.strip().str.title()
    df.loc[~df["urgency_level"].isin(VALID_URGENCY), "urgency_level"] = "Medium"

    df["city"] = df["city"].str.strip().str.title()
    df["hospital_name"] = df["hospital_name"].str.strip()

    df["request_date"] = pd.to_datetime(df["request_date"], errors="coerce")
    df.dropna(subset=["request_date"], inplace=True)
    df["request_date"] = df["request_date"].dt.strftime("%Y-%m-%d")

    df.reset_index(drop=True, inplace=True)
    report("Final", n0, len(df))
    return df


# ─────────────────────────────────────────────
# DONATION RECORDS
# ─────────────────────────────────────────────
def clean_donations(path):
    print_section("Cleaning: donation_records.csv")
    df = pd.read_csv(path)
    n0 = len(df)
    print(f"  Raw rows: {n0:,}")

    df.drop_duplicates(inplace=True)
    df.dropna(subset=["donation_id","donor_id"], inplace=True)

    df["blood_group"] = df["blood_group"].str.strip().str.upper()
    df = df[df["blood_group"].isin(VALID_BLOOD_GROUPS)]

    df["units_donated"] = pd.to_numeric(df["units_donated"], errors="coerce")
    df.dropna(subset=["units_donated"], inplace=True)
    df = df[df["units_donated"].between(1, 5)]
    df["units_donated"] = df["units_donated"].astype(int)

    df["donation_date"] = pd.to_datetime(df["donation_date"], errors="coerce")
    df.dropna(subset=["donation_date"], inplace=True)
    df["donation_date"] = df["donation_date"].dt.strftime("%Y-%m-%d")

    df["hospital_name"] = df["hospital_name"].str.strip()
    df.reset_index(drop=True, inplace=True)
    report("Final", n0, len(df))
    return df


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print("\n" + "=" * 55)
    print("  Blood Donation Analytics — Data Cleaning Pipeline")
    print("=" * 55)

    donors    = clean_donors(   os.path.join(RAW_DIR, "donors.csv"))
    requests  = clean_requests( os.path.join(RAW_DIR, "blood_requests.csv"))
    donations = clean_donations(os.path.join(RAW_DIR, "donation_records.csv"))

    donors.to_csv(   os.path.join(CLEANED_DIR, "donors_clean.csv"),           index=False)
    requests.to_csv( os.path.join(CLEANED_DIR, "blood_requests_clean.csv"),   index=False)
    donations.to_csv(os.path.join(CLEANED_DIR, "donation_records_clean.csv"), index=False)

    print(f"\n[SUCCESS] Cleaned files saved to: {CLEANED_DIR}")
    print(f"  donors_clean.csv            -> {len(donors):,} rows")
    print(f"  blood_requests_clean.csv    -> {len(requests):,} rows")
    print(f"  donation_records_clean.csv  -> {len(donations):,} rows")


if __name__ == "__main__":
    main()
