"""
Blood Donation Analytics & Donor Intelligence Platform
=======================================================
data_generation.py  —  Generates realistic synthetic datasets
Author: Data Analytics Team
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# ─────────────────────────────────────────────
SEED = 42
np.random.seed(SEED)
random.seed(SEED)

NUM_DONORS    = 5000
NUM_REQUESTS  = 2000
NUM_DONATIONS = 3500

RAW_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

# ─────────────────────────────────────────────
BLOOD_GROUPS        = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
BLOOD_GROUP_WEIGHTS = [0.229, 0.049, 0.238, 0.016, 0.074, 0.025, 0.311, 0.058]

CITIES = [
    "Mumbai","Delhi","Bangalore","Hyderabad","Chennai","Kolkata","Pune","Ahmedabad",
    "Jaipur","Surat","Lucknow","Kanpur","Nagpur","Indore","Thane","Bhopal",
    "Visakhapatnam","Pimpri","Patna","Vadodara","Ludhiana","Agra","Nashik",
    "Faridabad","Meerut","Rajkot","Varanasi","Srinagar","Aurangabad","Dhanbad",
    "Amritsar","Allahabad","Ranchi","Howrah","Coimbatore","Jabalpur","Gwalior",
    "Vijayawada","Jodhpur","Madurai","Raipur","Kota","Guwahati","Chandigarh",
    "Solapur","Hubballi","Tiruchirappalli","Bareilly","Mysore","Aligarh"
]

STATES = {
    "Mumbai":"Maharashtra","Delhi":"Delhi","Bangalore":"Karnataka",
    "Hyderabad":"Telangana","Chennai":"Tamil Nadu","Kolkata":"West Bengal",
    "Pune":"Maharashtra","Ahmedabad":"Gujarat","Jaipur":"Rajasthan",
    "Surat":"Gujarat","Lucknow":"Uttar Pradesh","Kanpur":"Uttar Pradesh",
    "Nagpur":"Maharashtra","Indore":"Madhya Pradesh","Thane":"Maharashtra",
    "Bhopal":"Madhya Pradesh","Visakhapatnam":"Andhra Pradesh",
    "Pimpri":"Maharashtra","Patna":"Bihar","Vadodara":"Gujarat",
    "Ludhiana":"Punjab","Agra":"Uttar Pradesh","Nashik":"Maharashtra",
    "Faridabad":"Haryana","Meerut":"Uttar Pradesh","Rajkot":"Gujarat",
    "Varanasi":"Uttar Pradesh","Srinagar":"Jammu & Kashmir",
    "Aurangabad":"Maharashtra","Dhanbad":"Jharkhand","Amritsar":"Punjab",
    "Allahabad":"Uttar Pradesh","Ranchi":"Jharkhand","Howrah":"West Bengal",
    "Coimbatore":"Tamil Nadu","Jabalpur":"Madhya Pradesh",
    "Gwalior":"Madhya Pradesh","Vijayawada":"Andhra Pradesh",
    "Jodhpur":"Rajasthan","Madurai":"Tamil Nadu","Raipur":"Chhattisgarh",
    "Kota":"Rajasthan","Guwahati":"Assam","Chandigarh":"Punjab",
    "Solapur":"Maharashtra","Hubballi":"Karnataka",
    "Tiruchirappalli":"Tamil Nadu","Bareilly":"Uttar Pradesh",
    "Mysore":"Karnataka","Aligarh":"Uttar Pradesh"
}

CITY_COORDS = {
    "Mumbai":(19.0760,72.8777),"Delhi":(28.6139,77.2090),
    "Bangalore":(12.9716,77.5946),"Hyderabad":(17.3850,78.4867),
    "Chennai":(13.0827,80.2707),"Kolkata":(22.5726,88.3639),
    "Pune":(18.5204,73.8567),"Ahmedabad":(23.0225,72.5714),
    "Jaipur":(26.9124,75.7873),"Surat":(21.1702,72.8311),
    "Lucknow":(26.8467,80.9462),"Kanpur":(26.4499,80.3319),
    "Nagpur":(21.1458,79.0882),"Indore":(22.7196,75.8577),
    "Thane":(19.2183,72.9781),"Bhopal":(23.2599,77.4126),
    "Visakhapatnam":(17.6868,83.2185),"Pimpri":(18.6279,73.8009),
    "Patna":(25.5941,85.1376),"Vadodara":(22.3072,73.1812),
    "Ludhiana":(30.9010,75.8573),"Agra":(27.1767,78.0081),
    "Nashik":(19.9975,73.7898),"Faridabad":(28.4089,77.3178),
    "Meerut":(28.9845,77.7064),"Rajkot":(22.3039,70.8022),
    "Varanasi":(25.3176,82.9739),"Srinagar":(34.0837,74.7973),
    "Aurangabad":(19.8762,75.3433),"Dhanbad":(23.7957,86.4304),
    "Amritsar":(31.6340,74.8723),"Allahabad":(25.4358,81.8463),
    "Ranchi":(23.3441,85.3096),"Howrah":(22.5958,88.2636),
    "Coimbatore":(11.0168,76.9558),"Jabalpur":(23.1815,79.9864),
    "Gwalior":(26.2183,78.1828),"Vijayawada":(16.5062,80.6480),
    "Jodhpur":(26.2389,73.0243),"Madurai":(9.9252,78.1198),
    "Raipur":(21.2514,81.6296),"Kota":(25.2138,75.8648),
    "Guwahati":(26.1445,91.7362),"Chandigarh":(30.7333,76.7794),
    "Solapur":(17.6599,75.9064),"Hubballi":(15.3647,75.1240),
    "Tiruchirappalli":(10.7905,78.7047),"Bareilly":(28.3670,79.4304),
    "Mysore":(12.2958,76.6394),"Aligarh":(27.8974,78.0880)
}

FIRST_NAMES = [
    "Aarav","Vivaan","Aditya","Vihaan","Arjun","Sai","Ayaan","Reyansh",
    "Ananya","Priya","Diya","Riya","Sneha","Kavya","Pooja","Neha",
    "Rahul","Rohit","Kiran","Suresh","Ramesh","Rajesh","Amit","Ajay",
    "Sunita","Geeta","Meena","Savita","Rekha","Nisha","Anjali","Divya",
    "Vikram","Varun","Nikhil","Gaurav","Manish","Deepak","Sachin",
    "Lakshmi","Parvati","Durga","Saraswati","Uma","Sita","Radha"
]

LAST_NAMES = [
    "Sharma","Verma","Singh","Kumar","Gupta","Patel","Shah","Mehta",
    "Joshi","Nair","Pillai","Reddy","Rao","Iyer","Menon","Chatterjee",
    "Banerjee","Das","Bose","Sen","Mishra","Shukla","Tiwari","Pandey",
    "Yadav","Jha","Thakur","Chauhan","Rajput","Bhat","Kaur","Gill",
    "Malhotra","Kapoor","Bhatia","Khanna","Chopra","Arora","Sinha"
]

HOSPITALS = [
    "AIIMS Hospital","Apollo Hospitals","Fortis Healthcare",
    "Max Super Speciality Hospital","Medanta - The Medicity",
    "Narayana Health","Columbia Asia Hospital","Manipal Hospitals",
    "Lilavati Hospital","Kokilaben Dhirubhai Ambani Hospital",
    "Christian Medical College","Amrita Institute of Medical Sciences",
    "Safdarjung Hospital","Ram Manohar Lohia Hospital",
    "Sir Gangaram Hospital","Hinduja Hospital","Breach Candy Hospital",
    "Bombay Hospital","KEM Hospital","Sassoon General Hospital",
    "Government General Hospital","ESI Hospital","District Hospital",
    "Civil Hospital","Primary Health Centre"
]

URGENCY_LEVELS   = ["Critical","High","Medium","Low"]
URGENCY_WEIGHTS  = [0.20, 0.30, 0.35, 0.15]


# ─────────────────────────────────────────────
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))


def add_noise(lat, lon, r=0.3):
    return (round(lat + np.random.uniform(-r, r), 6),
            round(lon + np.random.uniform(-r, r), 6))


# ─────────────────────────────────────────────
def generate_donors(n=NUM_DONORS):
    print(f"[INFO] Generating {n} donor records ...")
    cities = np.random.choice(CITIES, size=n)
    lats, lons = zip(*[add_noise(*CITY_COORDS[c]) for c in cities])

    s, e = datetime(2020,1,1), datetime(2024,12,31)
    last_dates = [
        random_date(s, e).strftime("%Y-%m-%d") if random.random() > 0.15 else None
        for _ in range(n)
    ]
    today = datetime(2025, 1, 1)
    avail = [
        "Available" if d is None or (today - datetime.strptime(d,"%Y-%m-%d")).days >= 90
        else "Unavailable"
        for d in last_dates
    ]

    df = pd.DataFrame({
        "donor_id":           [f"D{str(i).zfill(5)}" for i in range(1, n+1)],
        "name":               [f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}" for _ in range(n)],
        "age":                np.random.randint(18, 66, n).astype(float),
        "gender":             np.random.choice(["Male","Female","Other"], n, p=[0.58,0.40,0.02]),
        "blood_group":        np.random.choice(BLOOD_GROUPS, n, p=BLOOD_GROUP_WEIGHTS),
        "city":               cities,
        "state":              [STATES[c] for c in cities],
        "last_donation_date": last_dates,
        "availability_status":avail,
        "latitude":           list(lats),
        "longitude":          list(lons),
    })
    for col in ["last_donation_date","age","gender"]:
        df.loc[np.random.random(n) < 0.03, col] = np.nan
    return df


def generate_requests(n=NUM_REQUESTS):
    print(f"[INFO] Generating {n} blood request records ...")
    s, e = datetime(2023,1,1), datetime(2024,12,31)
    return pd.DataFrame({
        "request_id":    [f"R{str(i).zfill(5)}" for i in range(1, n+1)],
        "hospital_name": np.random.choice(HOSPITALS, n),
        "blood_group":   np.random.choice(BLOOD_GROUPS, n, p=BLOOD_GROUP_WEIGHTS),
        "units_required":np.random.randint(1, 11, n),
        "urgency_level": np.random.choice(URGENCY_LEVELS, n, p=URGENCY_WEIGHTS),
        "city":          np.random.choice(CITIES, n),
        "request_date":  [random_date(s, e).strftime("%Y-%m-%d") for _ in range(n)],
    })


def generate_donations(donors_df, n=NUM_DONATIONS):
    print(f"[INFO] Generating {n} donation records ...")
    eligible = donors_df[donors_df["last_donation_date"].notna()]
    sampled  = eligible.sample(n=n, replace=True, random_state=SEED)
    s, e = datetime(2020,1,1), datetime(2024,12,31)
    return pd.DataFrame({
        "donation_id":   [f"DON{str(i).zfill(6)}" for i in range(1, n+1)],
        "donor_id":      sampled["donor_id"].values,
        "hospital_name": np.random.choice(HOSPITALS, n),
        "blood_group":   sampled["blood_group"].values,
        "donation_date": [random_date(s, e).strftime("%Y-%m-%d") for _ in range(n)],
        "units_donated": np.random.randint(1, 4, n),
    })


def main():
    donors    = generate_donors()
    requests  = generate_requests()
    donations = generate_donations(donors)

    donors.to_csv(os.path.join(RAW_DIR,"donors.csv"),            index=False)
    requests.to_csv(os.path.join(RAW_DIR,"blood_requests.csv"),  index=False)
    donations.to_csv(os.path.join(RAW_DIR,"donation_records.csv"),index=False)

    print(f"\n[SUCCESS] Datasets saved to: {RAW_DIR}")
    print(f"  donors.csv            -> {len(donors):,} rows")
    print(f"  blood_requests.csv    -> {len(requests):,} rows")
    print(f"  donation_records.csv  -> {len(donations):,} rows")


if __name__ == "__main__":
    main()
