"""
analyzer.py — Exploratory Data Analysis (EDA), filtering, and monthly summaries.
Uses Pandas and NumPy for all data operations.
"""

import pandas as pd
import numpy as np
from datetime import datetime


class ExpenseAnalyzer:
    def __init__(self, expenses: list):
        self.df = self._build_df(expenses)

    def _build_df(self, expenses):
        """Convert raw expense list to a clean Pandas DataFrame."""
        if not expenses:
            return pd.DataFrame()

        df = pd.DataFrame(expenses)

        # --- Data Cleaning ---
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        df.dropna(subset=["amount"], inplace=True)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df.dropna(subset=["date"], inplace=True)

        # --- Feature Engineering ---
        df["month"] = df["date"].dt.to_period("M").astype(str)
        df["week"] = df["date"].dt.to_period("W").astype(str)
        df["day_of_week"] = df["date"].dt.day_name()
        df["year"] = df["date"].dt.year
        df["day"] = df["date"].dt.date.astype(str)

        df.sort_values("date", inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    # ── FILTERS ──────────────────────────────────────────────────────────────

    def filter_by_category(self, category: str):
        result = self.df[self.df["category"] == category]
        return result.to_dict("records")

    def filter_by_month(self, month: str):
        result = self.df[self.df["month"] == month]
        return result.to_dict("records")

    def filter_by_date_range(self, start: str, end: str):
        result = self.df[
            (self.df["date"] >= pd.to_datetime(start)) &
            (self.df["date"] <= pd.to_datetime(end))
        ]
        return result.to_dict("records")

    def filter_by_method(self, method: str):
        result = self.df[self.df["payment_method"].str.lower() == method.lower()]
        return result.to_dict("records")

    # ── MONTHLY SUMMARY ───────────────────────────────────────────────────────

    def monthly_summary(self, month: str):
        df_m = self.df[self.df["month"] == month]

        if df_m.empty:
            print(f"\n  📭 No expenses found for {month}.")
            return

        total = df_m["amount"].sum()
        avg_daily = df_m.groupby("day")["amount"].sum().mean()
        max_expense = df_m.loc[df_m["amount"].idxmax()]
        by_category = df_m.groupby("category")["amount"].sum().sort_values(ascending=False)

        print(f"\n📅 MONTHLY SUMMARY — {month}")
        print("=" * 55)
        print(f"  Total Spending        : ₹{total:,.2f}")
        print(f"  Total Transactions    : {len(df_m)}")
        print(f"  Avg Daily Spending    : ₹{avg_daily:,.2f}")
        print(f"  Highest Single Expense: ₹{max_expense['amount']:,.2f} ({max_expense['category']}) on {str(max_expense['date'])[:10]}")
        print(f"  Unique Categories     : {df_m['category'].nunique()}")

        print(f"\n  {'Category':<25} {'Amount':>10}  {'% Share':>8}")
        print("  " + "-" * 47)
        for cat, amt in by_category.items():
            pct = (amt / total) * 100
            bar = "█" * int(pct / 5)
            print(f"  {cat:<25} ₹{amt:>9,.2f}  {pct:>6.1f}%  {bar}")

        print(f"\n  Payment Method Breakdown:")
        method_summary = df_m.groupby("payment_method")["amount"].sum().sort_values(ascending=False)
        for method, amt in method_summary.items():
            print(f"    {method:<20} ₹{amt:,.2f}")

        print(f"\n  Week-wise Spending:")
        week_summary = df_m.groupby("week")["amount"].sum()
        for week, amt in week_summary.items():
            print(f"    {week}  →  ₹{amt:,.2f}")

        # --- EDA Stats ---
        print(f"\n  📊 Statistical Summary (Amounts):")
        stats = df_m["amount"].describe()
        print(f"    Min    : ₹{stats['min']:,.2f}")
        print(f"    Max    : ₹{stats['max']:,.2f}")
        print(f"    Mean   : ₹{stats['mean']:,.2f}")
        print(f"    Median : ₹{df_m['amount'].median():,.2f}")
        print(f"    Std Dev: ₹{stats['std']:,.2f}")

    # ── FULL EDA ──────────────────────────────────────────────────────────────

    def full_eda(self):
        if self.df.empty:
            print("  No data available for EDA.")
            return

        print("\n🔬 FULL EDA REPORT")
        print("=" * 55)
        print(f"  Total Records     : {len(self.df)}")
        print(f"  Total Spending    : ₹{self.df['amount'].sum():,.2f}")
        print(f"  Date Range        : {self.df['date'].min().date()} → {self.df['date'].max().date()}")
        print(f"  Categories        : {self.df['category'].nunique()}")
        print(f"  Missing Values    : {self.df.isnull().sum().sum()}")
        print(f"  Duplicate Rows    : {self.df.duplicated().sum()}")

        print(f"\n  Top 3 Categories by Spend:")
        top3 = self.df.groupby("category")["amount"].sum().nlargest(3)
        for cat, amt in top3.items():
            print(f"    {cat}: ₹{amt:,.2f}")

        print(f"\n  Busiest Day of Week:")
        dow = self.df.groupby("day_of_week")["amount"].sum().idxmax()
        print(f"    {dow}")
