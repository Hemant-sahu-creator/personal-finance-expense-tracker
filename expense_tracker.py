"""
Personal Finance Expense Tracker
Author: Hemant Sahu
Description: A Python CLI app for category-wise expense logging,
             EDA, visualization, and automated monthly report generation.
"""

import os
import csv
import json
from datetime import datetime
from data_manager import DataManager
from analyzer import ExpenseAnalyzer
from visualizer import ExpenseVisualizer
from report_generator import ReportGenerator


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    print("=" * 60)
    print("       💰 Personal Finance Expense Tracker")
    print("          By Hemant Sahu | Python Project")
    print("=" * 60)


def main_menu():
    print("\n📋 MAIN MENU")
    print("-" * 40)
    print("  1. ➕ Add New Expense")
    print("  2. 📊 View All Expenses")
    print("  3. 🔍 Filter Expenses")
    print("  4. 📈 Visualize Spending")
    print("  5. 📅 Monthly Summary")
    print("  6. 📄 Generate Full Report")
    print("  7. 🗑️  Delete an Expense")
    print("  8. ❌ Exit")
    print("-" * 40)
    return input("  Enter choice (1-8): ").strip()


CATEGORIES = [
    "Food & Dining",
    "Transportation",
    "Shopping",
    "Entertainment",
    "Health & Medical",
    "Utilities & Bills",
    "Education",
    "Travel",
    "Personal Care",
    "Other"
]


def add_expense(dm):
    print("\n➕ ADD NEW EXPENSE")
    print("-" * 40)

    # Amount
    while True:
        try:
            amount = float(input("  Enter amount (₹): ").strip())
            if amount <= 0:
                print("  ⚠️  Amount must be positive.")
                continue
            break
        except ValueError:
            print("  ⚠️  Please enter a valid number.")

    # Category
    print("\n  Select Category:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"    {i:2}. {cat}")
    while True:
        try:
            cat_choice = int(input("  Enter category number: ").strip())
            if 1 <= cat_choice <= len(CATEGORIES):
                category = CATEGORIES[cat_choice - 1]
                break
            print(f"  ⚠️  Enter a number between 1 and {len(CATEGORIES)}.")
        except ValueError:
            print("  ⚠️  Please enter a valid number.")

    # Description
    description = input("  Description (optional): ").strip() or "N/A"

    # Date
    date_input = input("  Date (YYYY-MM-DD) [leave blank for today]: ").strip()
    if not date_input:
        date = datetime.today().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            date = date_input
        except ValueError:
            print("  ⚠️  Invalid date format. Using today's date.")
            date = datetime.today().strftime("%Y-%m-%d")

    # Payment method
    methods = ["Cash", "UPI", "Credit Card", "Debit Card", "Net Banking", "Other"]
    print("\n  Payment Method:")
    for i, m in enumerate(methods, 1):
        print(f"    {i}. {m}")
    while True:
        try:
            m_choice = int(input("  Enter method number: ").strip())
            if 1 <= m_choice <= len(methods):
                method = methods[m_choice - 1]
                break
            print(f"  ⚠️  Enter between 1 and {len(methods)}.")
        except ValueError:
            print("  ⚠️  Please enter a valid number.")

    expense = {
        "id": dm.get_next_id(),
        "date": date,
        "amount": amount,
        "category": category,
        "description": description,
        "payment_method": method
    }

    dm.add_expense(expense)
    print(f"\n  ✅ Expense of ₹{amount:.2f} added under '{category}' on {date}.")


def view_expenses(dm):
    expenses = dm.load_expenses()
    if not expenses:
        print("\n  📭 No expenses found.")
        return

    print(f"\n📊 ALL EXPENSES ({len(expenses)} records)")
    print("-" * 80)
    print(f"  {'ID':<5} {'Date':<12} {'Category':<20} {'Amount':>10}  {'Method':<14} {'Description'}")
    print("-" * 80)
    total = 0
    for e in expenses:
        print(f"  {e['id']:<5} {e['date']:<12} {e['category']:<20} ₹{float(e['amount']):>9.2f}  {e['payment_method']:<14} {e['description']}")
        total += float(e['amount'])
    print("-" * 80)
    print(f"  {'TOTAL':<38} ₹{total:>9.2f}")
    print("-" * 80)


def filter_expenses(dm):
    print("\n🔍 FILTER EXPENSES")
    print("  1. By Category")
    print("  2. By Month")
    print("  3. By Date Range")
    print("  4. By Payment Method")
    choice = input("  Choose filter: ").strip()

    analyzer = ExpenseAnalyzer(dm.load_expenses())

    if choice == "1":
        print("\n  Categories:")
        for i, c in enumerate(CATEGORIES, 1):
            print(f"    {i}. {c}")
        cat_num = int(input("  Choose category: ").strip())
        cat = CATEGORIES[cat_num - 1]
        results = analyzer.filter_by_category(cat)
        _print_filtered(results, f"Category: {cat}")

    elif choice == "2":
        month = input("  Enter month (YYYY-MM): ").strip()
        results = analyzer.filter_by_month(month)
        _print_filtered(results, f"Month: {month}")

    elif choice == "3":
        start = input("  Start date (YYYY-MM-DD): ").strip()
        end = input("  End date (YYYY-MM-DD): ").strip()
        results = analyzer.filter_by_date_range(start, end)
        _print_filtered(results, f"Range: {start} to {end}")

    elif choice == "4":
        method = input("  Payment method: ").strip()
        results = analyzer.filter_by_method(method)
        _print_filtered(results, f"Method: {method}")


def _print_filtered(results, label):
    if not results:
        print(f"\n  📭 No results for {label}.")
        return
    total = sum(float(e['amount']) for e in results)
    print(f"\n  Results for {label} ({len(results)} records)  —  Total: ₹{total:.2f}")
    print(f"  {'ID':<5} {'Date':<12} {'Category':<20} {'Amount':>10}  {'Description'}")
    print("  " + "-" * 65)
    for e in results:
        print(f"  {e['id']:<5} {e['date']:<12} {e['category']:<20} ₹{float(e['amount']):>9.2f}  {e['description']}")


def visualize(dm):
    expenses = dm.load_expenses()
    if not expenses:
        print("\n  📭 No expenses to visualize.")
        return

    viz = ExpenseVisualizer(expenses)
    print("\n📈 VISUALIZE SPENDING")
    print("  1. Pie Chart — Category-wise distribution")
    print("  2. Bar Chart — Monthly spending")
    print("  3. Bar Chart — Category totals")
    print("  4. Line Chart — Daily spending trend")
    print("  5. All Charts")
    choice = input("  Choose (1-5): ").strip()

    if choice == "1":
        viz.pie_chart()
    elif choice == "2":
        viz.monthly_bar()
    elif choice == "3":
        viz.category_bar()
    elif choice == "4":
        viz.daily_trend()
    elif choice == "5":
        viz.all_charts()
    else:
        print("  ⚠️  Invalid choice.")


def monthly_summary(dm):
    analyzer = ExpenseAnalyzer(dm.load_expenses())
    month = input("\n  Enter month (YYYY-MM) [blank for current]: ").strip()
    if not month:
        month = datetime.today().strftime("%Y-%m")
    analyzer.monthly_summary(month)


def generate_report(dm):
    expenses = dm.load_expenses()
    if not expenses:
        print("\n  📭 No expenses to report.")
        return
    rg = ReportGenerator(expenses)
    month = input("  Enter month (YYYY-MM) [blank for current]: ").strip()
    if not month:
        month = datetime.today().strftime("%Y-%m")
    rg.generate(month)


def delete_expense(dm):
    view_expenses(dm)
    try:
        eid = int(input("\n  Enter ID to delete: ").strip())
        dm.delete_expense(eid)
        print(f"  ✅ Expense ID {eid} deleted.")
    except ValueError:
        print("  ⚠️  Invalid ID.")


def main():
    dm = DataManager()
    while True:
        clear()
        print_banner()
        choice = main_menu()

        if choice == "1":
            add_expense(dm)
        elif choice == "2":
            view_expenses(dm)
        elif choice == "3":
            filter_expenses(dm)
        elif choice == "4":
            visualize(dm)
        elif choice == "5":
            monthly_summary(dm)
        elif choice == "6":
            generate_report(dm)
        elif choice == "7":
            delete_expense(dm)
        elif choice == "8":
            print("\n  👋 Goodbye! Keep tracking your finances.\n")
            break
        else:
            print("\n  ⚠️  Invalid choice. Please try again.")

        input("\n  Press Enter to continue...")


if __name__ == "__main__":
    main()
