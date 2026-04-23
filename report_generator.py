"""
report_generator.py — Automated monthly report generation.
Saves a detailed text report to the reports/ folder.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)


class ReportGenerator:
    def __init__(self, expenses: list):
        self.df = self._build_df(expenses)

    def _build_df(self, expenses):
        df = pd.DataFrame(expenses)
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df.dropna(subset=["amount", "date"], inplace=True)
        df["month"] = df["date"].dt.to_period("M").astype(str)
        df["day"] = df["date"].dt.date.astype(str)
        df["week"] = df["date"].dt.to_period("W").astype(str)
        df["day_of_week"] = df["date"].dt.day_name()
        return df

    def generate(self, month: str):
        df_m = self.df[self.df["month"] == month]

        if df_m.empty:
            print(f"\n  📭 No data found for {month}. Cannot generate report.")
            return

        lines = []
        sep = "=" * 60
        div = "-" * 60

        total = df_m["amount"].sum()
        count = len(df_m)
        avg_txn = df_m["amount"].mean()
        median_txn = df_m["amount"].median()
        max_row = df_m.loc[df_m["amount"].idxmax()]
        min_row = df_m.loc[df_m["amount"].idxmin()]
        by_cat = df_m.groupby("category")["amount"].sum().sort_values(ascending=False)
        by_method = df_m.groupby("payment_method")["amount"].sum().sort_values(ascending=False)
        daily = df_m.groupby("day")["amount"].sum()
        weekly = df_m.groupby("week")["amount"].sum()

        lines.append(sep)
        lines.append(f"     PERSONAL FINANCE EXPENSE REPORT — {month}")
        lines.append(f"     Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(sep)

        lines.append("\n📌 OVERVIEW")
        lines.append(div)
        lines.append(f"  Total Spending        : ₹{total:,.2f}")
        lines.append(f"  Total Transactions    : {count}")
        lines.append(f"  Average Transaction   : ₹{avg_txn:,.2f}")
        lines.append(f"  Median Transaction    : ₹{median_txn:,.2f}")
        lines.append(f"  Highest Expense       : ₹{max_row['amount']:,.2f} — {max_row['category']} on {max_row['day']}")
        lines.append(f"  Lowest Expense        : ₹{min_row['amount']:,.2f} — {min_row['category']} on {min_row['day']}")
        lines.append(f"  Avg Daily Spending    : ₹{daily.mean():,.2f}")
        lines.append(f"  Peak Day              : {daily.idxmax()} (₹{daily.max():,.2f})")

        lines.append("\n📂 CATEGORY BREAKDOWN")
        lines.append(div)
        lines.append(f"  {'Category':<25} {'Amount':>10}  {'%':>6}  {'Bar'}")
        lines.append("  " + "-" * 55)
        for cat, amt in by_cat.items():
            pct = (amt / total) * 100
            bar = "█" * int(pct / 4)
            lines.append(f"  {cat:<25} ₹{amt:>9,.2f}  {pct:>5.1f}%  {bar}")
        lines.append(f"\n  {'TOTAL':<25} ₹{total:>9,.2f}")

        lines.append("\n💳 PAYMENT METHOD BREAKDOWN")
        lines.append(div)
        for method, amt in by_method.items():
            pct = (amt / total) * 100
            lines.append(f"  {method:<20} ₹{amt:>9,.2f}  ({pct:.1f}%)")

        lines.append("\n📅 WEEK-WISE SUMMARY")
        lines.append(div)
        for week, amt in weekly.items():
            lines.append(f"  {week}  →  ₹{amt:,.2f}")

        lines.append("\n📆 DAILY SPENDING LOG")
        lines.append(div)
        lines.append(f"  {'Date':<14} {'Amount':>10}  {'Transactions':>14}")
        lines.append("  " + "-" * 42)
        daily_counts = df_m.groupby("day")["amount"].count()
        for day in sorted(daily.index):
            lines.append(f"  {day:<14} ₹{daily[day]:>9,.2f}  {daily_counts[day]:>14}")

        lines.append("\n📊 STATISTICAL ANALYSIS (EDA)")
        lines.append(div)
        stats = df_m["amount"].describe()
        lines.append(f"  Count   : {int(stats['count'])}")
        lines.append(f"  Mean    : ₹{stats['mean']:,.2f}")
        lines.append(f"  Std Dev : ₹{stats['std']:,.2f}")
        lines.append(f"  Min     : ₹{stats['min']:,.2f}")
        lines.append(f"  25%     : ₹{stats['25%']:,.2f}")
        lines.append(f"  Median  : ₹{stats['50%']:,.2f}")
        lines.append(f"  75%     : ₹{stats['75%']:,.2f}")
        lines.append(f"  Max     : ₹{stats['max']:,.2f}")

        lines.append("\n🔍 ALL TRANSACTIONS")
        lines.append(div)
        lines.append(f"  {'ID':<5} {'Date':<12} {'Category':<22} {'Amount':>10}  {'Method':<14} Description")
        lines.append("  " + "-" * 78)
        for _, row in df_m.iterrows():
            lines.append(f"  {row['id']:<5} {row['day']:<12} {row['category']:<22} ₹{row['amount']:>9,.2f}  {row['payment_method']:<14} {row['description']}")

        lines.append("\n" + sep)
        lines.append("  End of Report — Personal Finance Expense Tracker")
        lines.append(f"  Author: Hemant Sahu  |  Generated: {datetime.now().strftime('%Y-%m-%d')}")
        lines.append(sep)

        report_text = "\n".join(lines)
        filename = os.path.join(REPORT_DIR, f"report_{month}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report_text)

        print(report_text)
        print(f"\n  ✅ Report saved → {filename}")
