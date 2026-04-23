"""
visualizer.py — All Matplotlib & Seaborn visualizations for expense data.
Charts: Pie, Bar (category), Bar (monthly), Line (daily trend), Combined dashboard.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from datetime import datetime
import os

OUTPUT_DIR = "charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PALETTE = [
    "#1B4F8A", "#2E86C1", "#5DADE2", "#85C1E9", "#AED6F1",
    "#1ABC9C", "#2ECC71", "#F39C12", "#E74C3C", "#9B59B6"
]

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 120
})


class ExpenseVisualizer:
    def __init__(self, expenses: list):
        self.df = self._build_df(expenses)

    def _build_df(self, expenses):
        if not expenses:
            return pd.DataFrame()
        df = pd.DataFrame(expenses)
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df.dropna(subset=["amount", "date"], inplace=True)
        df["month"] = df["date"].dt.to_period("M").astype(str)
        df["day"] = df["date"].dt.date
        return df

    # ── PIE CHART ─────────────────────────────────────────────────────────────

    def pie_chart(self):
        by_cat = self.df.groupby("category")["amount"].sum().sort_values(ascending=False)
        total = by_cat.sum()

        fig, ax = plt.subplots(figsize=(9, 6))
        wedges, texts, autotexts = ax.pie(
            by_cat.values,
            labels=by_cat.index,
            autopct=lambda p: f"₹{p*total/100:,.0f}\n({p:.1f}%)",
            colors=PALETTE[:len(by_cat)],
            startangle=140,
            pctdistance=0.78,
            wedgeprops=dict(linewidth=1.5, edgecolor="white")
        )
        for t in autotexts:
            t.set_fontsize(8)

        ax.set_title("Category-wise Expense Distribution", fontsize=14, fontweight="bold", pad=20)
        plt.tight_layout()
        path = os.path.join(OUTPUT_DIR, "pie_chart.png")
        plt.savefig(path, bbox_inches="tight")
        print(f"\n  ✅ Pie chart saved → {path}")
        plt.show()

    # ── MONTHLY BAR ───────────────────────────────────────────────────────────

    def monthly_bar(self):
        by_month = self.df.groupby("month")["amount"].sum()

        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.bar(by_month.index, by_month.values, color=PALETTE[0], edgecolor="white", linewidth=0.8)

        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, h + 50, f"₹{h:,.0f}",
                    ha="center", va="bottom", fontsize=9, fontweight="bold", color="#333")

        ax.set_title("Monthly Total Spending", fontsize=14, fontweight="bold")
        ax.set_xlabel("Month", fontsize=11)
        ax.set_ylabel("Amount (₹)", fontsize=11)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        path = os.path.join(OUTPUT_DIR, "monthly_bar.png")
        plt.savefig(path, bbox_inches="tight")
        print(f"  ✅ Monthly bar chart saved → {path}")
        plt.show()

    # ── CATEGORY BAR ──────────────────────────────────────────────────────────

    def category_bar(self):
        by_cat = self.df.groupby("category")["amount"].sum().sort_values(ascending=True)

        fig, ax = plt.subplots(figsize=(10, 6))
        colors = PALETTE[:len(by_cat)]
        bars = ax.barh(by_cat.index, by_cat.values, color=colors[::-1], edgecolor="white")

        for bar in bars:
            w = bar.get_width()
            ax.text(w + 50, bar.get_y() + bar.get_height() / 2,
                    f"₹{w:,.0f}", va="center", fontsize=9, fontweight="bold")

        ax.set_title("Total Spending by Category", fontsize=14, fontweight="bold")
        ax.set_xlabel("Amount (₹)", fontsize=11)
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
        plt.tight_layout()
        path = os.path.join(OUTPUT_DIR, "category_bar.png")
        plt.savefig(path, bbox_inches="tight")
        print(f"  ✅ Category bar chart saved → {path}")
        plt.show()

    # ── DAILY TREND LINE ──────────────────────────────────────────────────────

    def daily_trend(self):
        daily = self.df.groupby("day")["amount"].sum().reset_index()
        daily["day"] = pd.to_datetime(daily["day"])
        daily = daily.sort_values("day")

        # 7-day rolling average
        daily["rolling_avg"] = daily["amount"].rolling(window=7, min_periods=1).mean()

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.fill_between(daily["day"], daily["amount"], alpha=0.25, color=PALETTE[1])
        ax.plot(daily["day"], daily["amount"], color=PALETTE[1], linewidth=1.5, label="Daily Spending", marker="o", markersize=3)
        ax.plot(daily["day"], daily["rolling_avg"], color=PALETTE[7], linewidth=2.2, linestyle="--", label="7-Day Avg")

        ax.set_title("Daily Spending Trend", fontsize=14, fontweight="bold")
        ax.set_xlabel("Date", fontsize=11)
        ax.set_ylabel("Amount (₹)", fontsize=11)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
        ax.legend(fontsize=10)
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        path = os.path.join(OUTPUT_DIR, "daily_trend.png")
        plt.savefig(path, bbox_inches="tight")
        print(f"  ✅ Daily trend chart saved → {path}")
        plt.show()

    # ── SEABORN HEATMAP ───────────────────────────────────────────────────────

    def category_month_heatmap(self):
        pivot = self.df.pivot_table(index="category", columns="month", values="amount", aggfunc="sum", fill_value=0)

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(pivot, annot=True, fmt=".0f", cmap="Blues", linewidths=0.5,
                    annot_kws={"size": 8}, ax=ax, cbar_kws={"label": "Amount (₹)"})
        ax.set_title("Category × Month Spending Heatmap", fontsize=14, fontweight="bold")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        path = os.path.join(OUTPUT_DIR, "heatmap.png")
        plt.savefig(path, bbox_inches="tight")
        print(f"  ✅ Heatmap saved → {path}")
        plt.show()

    # ── ALL CHARTS DASHBOARD ──────────────────────────────────────────────────

    def all_charts(self):
        fig = plt.figure(figsize=(16, 12))
        fig.suptitle("💰 Personal Finance Dashboard", fontsize=18, fontweight="bold", y=0.98)

        by_cat = self.df.groupby("category")["amount"].sum().sort_values(ascending=False)
        by_month = self.df.groupby("month")["amount"].sum()
        daily = self.df.groupby("day")["amount"].sum().reset_index()
        daily["day"] = pd.to_datetime(daily["day"])
        daily = daily.sort_values("day")
        daily["rolling_avg"] = daily["amount"].rolling(7, min_periods=1).mean()

        # Pie
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.pie(by_cat.values, labels=by_cat.index, autopct="%1.1f%%",
                colors=PALETTE[:len(by_cat)], startangle=140,
                wedgeprops=dict(linewidth=1, edgecolor="white"))
        ax1.set_title("Category Distribution", fontweight="bold")

        # Monthly bar
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.bar(by_month.index, by_month.values, color=PALETTE[0], edgecolor="white")
        ax2.set_title("Monthly Spending", fontweight="bold")
        ax2.set_ylabel("₹")
        ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=30, ha="right")

        # Category bar
        ax3 = fig.add_subplot(2, 2, 3)
        by_cat_sorted = by_cat.sort_values(ascending=True)
        ax3.barh(by_cat_sorted.index, by_cat_sorted.values, color=PALETTE[2])
        ax3.set_title("Spending by Category", fontweight="bold")
        ax3.set_xlabel("₹")

        # Daily trend
        ax4 = fig.add_subplot(2, 2, 4)
        ax4.fill_between(daily["day"], daily["amount"], alpha=0.2, color=PALETTE[1])
        ax4.plot(daily["day"], daily["amount"], color=PALETTE[1], linewidth=1.5, label="Daily")
        ax4.plot(daily["day"], daily["rolling_avg"], color=PALETTE[7], linestyle="--", linewidth=2, label="7-Day Avg")
        ax4.set_title("Daily Spending Trend", fontweight="bold")
        ax4.legend(fontsize=8)
        ax4.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
        plt.setp(ax4.xaxis.get_majorticklabels(), rotation=30, ha="right")

        plt.tight_layout()
        path = os.path.join(OUTPUT_DIR, "dashboard.png")
        plt.savefig(path, bbox_inches="tight")
        print(f"\n  ✅ Full dashboard saved → {path}")
        plt.show()
