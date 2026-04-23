"""
seed_data.py — Generates realistic sample expense data for demonstration.
Run this before launching the main app to populate sample records.
"""

import csv
import random
from datetime import datetime, timedelta
import os

DATA_FILE = "expenses.csv"
FIELDNAMES = ["id", "date", "amount", "category", "description", "payment_method"]

CATEGORIES = {
    "Food & Dining":      [("Zomato order", 180, 650), ("Grocery store", 400, 1200), ("Restaurant dinner", 500, 1800), ("Tea & snacks", 30, 150)],
    "Transportation":     [("Ola/Uber ride", 80, 350), ("Petrol", 300, 800), ("Bus/Auto fare", 20, 100), ("Train ticket", 150, 600)],
    "Shopping":           [("Clothing", 500, 3000), ("Electronics accessory", 200, 2000), ("Amazon order", 300, 2500), ("Stationery", 50, 300)],
    "Entertainment":      [("Netflix subscription", 199, 499), ("Movie ticket", 150, 400), ("Gaming", 100, 500), ("Books", 150, 600)],
    "Health & Medical":   [("Pharmacy", 100, 800), ("Doctor consultation", 300, 800), ("Gym membership", 500, 1500), ("Vitamins", 200, 600)],
    "Utilities & Bills":  [("Electricity bill", 400, 1200), ("Internet bill", 499, 999), ("Mobile recharge", 199, 499), ("Water bill", 100, 300)],
    "Education":          [("Online course", 500, 3000), ("Books/Notes", 200, 800), ("Exam fee", 500, 2000), ("Coaching fee", 1000, 5000)],
    "Personal Care":      [("Haircut", 100, 300), ("Skincare", 200, 800), ("Laundry", 100, 300), ("Toiletries", 150, 500)],
    "Other":              [("Miscellaneous", 50, 500), ("Gift", 200, 1500), ("Donation", 100, 500)],
}

METHODS = ["UPI", "Cash", "UPI", "UPI", "Credit Card", "Debit Card", "Net Banking"]


def seed():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

    records = []
    expense_id = 1
    base_date = datetime(2025, 1, 1)

    for day_offset in range(270):  # ~9 months of data
        current_date = base_date + timedelta(days=day_offset)
        num_txns = random.choices([0, 1, 2, 3], weights=[20, 45, 25, 10])[0]

        for _ in range(num_txns):
            category = random.choice(list(CATEGORIES.keys()))
            desc, low, high = random.choice(CATEGORIES[category])
            amount = round(random.uniform(low, high), 2)
            method = random.choice(METHODS)

            records.append({
                "id": expense_id,
                "date": current_date.strftime("%Y-%m-%d"),
                "amount": amount,
                "category": category,
                "description": desc,
                "payment_method": method
            })
            expense_id += 1

    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(records)

    print(f"✅ Seeded {len(records)} sample expense records into '{DATA_FILE}'")
    print(f"   Date range: Jan 2025 → Sep 2025")
    print(f"   Categories: {len(CATEGORIES)}")
    print(f"\n   Now run:  python expense_tracker.py")


if __name__ == "__main__":
    seed()
