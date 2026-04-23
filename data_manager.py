"""
data_manager.py — Handles all CSV read/write operations for expenses.
"""

import csv
import os

DATA_FILE = "expenses.csv"
FIELDNAMES = ["id", "date", "amount", "category", "description", "payment_method"]


class DataManager:
    def __init__(self, filepath=DATA_FILE):
        self.filepath = filepath
        self._init_file()

    def _init_file(self):
        """Create CSV with headers if it doesn't exist."""
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
                writer.writeheader()

    def load_expenses(self):
        """Load all expenses from CSV and return as list of dicts."""
        expenses = []
        with open(self.filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                expenses.append(row)
        return expenses

    def add_expense(self, expense: dict):
        """Append a new expense record to the CSV."""
        with open(self.filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writerow(expense)

    def save_all(self, expenses: list):
        """Overwrite the CSV with the given list of expenses."""
        with open(self.filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(expenses)

    def delete_expense(self, expense_id: int):
        """Delete an expense by its ID."""
        expenses = self.load_expenses()
        updated = [e for e in expenses if int(e["id"]) != expense_id]
        if len(updated) == len(expenses):
            print(f"  ⚠️  No expense found with ID {expense_id}.")
        else:
            self.save_all(updated)

    def get_next_id(self):
        """Return the next available integer ID."""
        expenses = self.load_expenses()
        if not expenses:
            return 1
        return max(int(e["id"]) for e in expenses) + 1
