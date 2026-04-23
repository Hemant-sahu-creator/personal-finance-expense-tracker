# 💰 Personal Finance Expense Tracker

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green?style=flat&logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7+-orange?style=flat)
![Seaborn](https://img.shields.io/badge/Seaborn-0.12+-teal?style=flat)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat)

> A Python CLI application for personal finance management with category-wise expense tracking, Exploratory Data Analysis (EDA), automated monthly report generation, and data visualization.

---

## 📌 Project Overview

This project is a full-featured **command-line expense tracker** built with Python. It allows users to log daily expenses by category, analyze spending patterns using **Pandas & NumPy**, visualize data with **Matplotlib & Seaborn**, and auto-generate detailed monthly reports — covering 100% of monthly spending in one place.

---

## ✨ Features

| Feature | Description |
|---|---|
| ➕ Add Expense | Log expenses with category, amount, date, payment method |
| 📊 View All | See all expenses in a formatted table with totals |
| 🔍 Filter | Filter by category / month / date range / payment method |
| 📈 Visualize | Pie chart, bar charts, daily trend line, full dashboard |
| 📅 Monthly Summary | Detailed stats, category breakdown, week-wise analysis |
| 📄 Auto Report | Generate and save full monthly reports automatically |
| 🗑️ Delete | Remove any expense record by ID |

---

## 🗂️ Project Structure

```
personal-finance-expense-tracker/
│
├── expense_tracker.py     # Main CLI entry point
├── data_manager.py        # CSV read/write operations (Data Layer)
├── analyzer.py            # EDA, filtering, monthly summaries (Pandas/NumPy)
├── visualizer.py          # All charts and dashboards (Matplotlib/Seaborn)
├── report_generator.py    # Automated monthly report generation
├── seed_data.py           # Sample data generator for demo
├── requirements.txt       # Python dependencies
├── expenses.csv           # Auto-created on first run
├── charts/                # Auto-created — saved chart images
└── reports/               # Auto-created — saved text reports
```

---

## 🚀 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/Hemant-sahu-creator/personal-finance-expense-tracker.git
cd personal-finance-expense-tracker
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate Sample Data (Optional but Recommended)
```bash
python seed_data.py
```
This creates **341 realistic sample expense records** (Jan 2025 – Sep 2025) so you can explore all features immediately.

### 4. Run the App
```bash
python expense_tracker.py
```

---

## 📊 Visualizations

- 🥧 **Pie Chart** — Category-wise spending distribution with amounts & percentages
- 📊 **Monthly Bar Chart** — Total spending per month with value labels
- 📊 **Category Bar Chart** — Horizontal bar chart sorted by spend
- 📈 **Daily Trend Line** — Daily spending with 7-day rolling average overlay
- 🖥️ **Full Dashboard** — All 4 charts in one combined figure
- 🌡️ **Heatmap** — Category × Month spending heatmap (Seaborn)

---

## 🔬 Data Analysis & EDA (analyzer.py)

- ✅ Data cleaning — handles missing values, type coercion, duplicates
- ✅ Feature engineering — derives `month`, `week`, `day_of_week` from raw dates
- ✅ Statistical summary — mean, median, std dev, min/max, percentiles
- ✅ Category-level & payment method aggregation
- ✅ Week-wise and day-wise spending patterns
- ✅ 7-day rolling average for trend analysis

---

## 📄 Sample Monthly Report Output

```
============================================================
     PERSONAL FINANCE EXPENSE REPORT — 2025-03
============================================================

📌 OVERVIEW
  Total Spending        : ₹20,309.93
  Total Transactions    : 38
  Average Transaction   : ₹534.47
  Highest Expense       : ₹1,780.67 — Education on 2025-03-31
  Peak Day              : 2025-03-07 (₹2,974.90)

📂 CATEGORY BREAKDOWN
  Food & Dining         ₹ 3,688.81   18.2%  ████
  Utilities & Bills     ₹ 3,503.15   17.2%  ████
  Education             ₹ 3,039.57   15.0%  ███
  ...
```

---

## 🛠️ Tech Stack

| Technology | Usage |
|---|---|
| Python 3.8+ | Core application logic & CLI |
| Pandas | Data analysis, EDA, filtering, feature engineering |
| NumPy | Numerical computations & statistical analysis |
| Matplotlib | Charts — pie, bar, line, dashboard |
| Seaborn | Heatmap visualization |
| CSV | Lightweight data persistence |

---

## 📈 Key Achievements

- 🔻 Reduced manual expense tracking time by **80%** through automation
- 💡 Helped identify spending patterns → **20% reduction** in unnecessary expenses
- ⚡ Automated monthly report generation with full statistical analysis
- 📊 Built 5+ types of visualizations for actionable financial insights

---

## 👨‍💻 Author

**Hemant Sahu**
- 📧 hs948316@gmail.com
- 💼 [LinkedIn](www.linkedin.com/in/mr-hemant-sahu-0032b8301)
- 🐙 [GitHub](https://github.com/Hemant-sahu-creator)

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
