from datetime import datetime
from zoneinfo import ZoneInfo
import math

class Record:
    def __init__(self, amount: float, datetime: datetime, category: str, note: str):
        self.amount = abs(amount)
        self.datetime = datetime
        self.category = category
        self.note = note

    def __str__(self):
        return f"${self.amount} at {self.datetime} in category {self.category} with note {self.note}"


class Income(Record):
    def __init__(self, amount: float, datetime: datetime, category: str, note: str):
        super().__init__(amount, datetime, category, note)

    def __str__(self):
        return f"Income of ${self.amount} at {self.datetime} in category {self.category} with note {self.note}"

class Expense(Record):
    def __init__(self, amount: float, datetime: datetime, category: str, note: str):
        super().__init__(amount, datetime, category, note)

    def __str__(self):
        return f"Expense of ${self.amount} at {self.datetime} in category {self.category} with note {self.note}"

class Account:
    def __init__(self, file):
        self.file = file
        lines = file.readlines()
        name, initialBalance = lines[0].split(":")
        self.name = name
        self.read_records(lines[1:])
        self.initialBalance = float(initialBalance)
        self.logs: list[tuple[datetime, str]] = []

    def read_records(self, lines: list[str]):
        records = [line.split(",") for line in lines]
        records = [(float(a), datetime.fromisoformat(d), c, n) for a, d, c, n in records]
        self.incomes = [Income(a, d, c, n) for a, d, c, n in records if a > 0]
        self.expenses = [Expense(-a, d, c, n) for a, d, c, n in records if a < 0]

    def balance(self) -> float:
        return self.initialBalance + sum(i.amount for i in self.incomes) - sum(e.amount for e in self.expenses)

    def edit_balance(self, balance: float):
        oldBalance = self.initialBalance
        self.initialBalance = abs(balance)
        self.logs.append((datetime.now(ZoneInfo("US/Pacific")), f"Edited balance from {oldBalance} to {self.initialBalance}"))


    def add_income(self, amount: float, datetime: datetime = datetime.now(ZoneInfo("US/Pacific")), category: str = "Other", note: str = ""):
        self.incomes.append(Income(amount, datetime, category, note))
        self.file.write(f"+{abs(amount)},{datetime},{category},{note}\n")
        self.logs.append((datetime.now(ZoneInfo("US/Pacific")), f"Added {self.incomes[-1]}"))

    def add_expense(self, amount: float, datetime: datetime = datetime.now(ZoneInfo("US/Pacific")), category: str = "Other", note: str = ""):
        self.expenses.append(Expense(amount, datetime, category, note))
        self.file.write(f"-{abs(amount)},{datetime},{category},{note}\n")
        self.logs.append((datetime.now(ZoneInfo("US/Pacific")), f"Added {self.expenses[-1]}"))