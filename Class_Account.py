
from datetime import datetime
from zoneinfo import ZoneInfo

class Class_Account:
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
        self.incomes = [a for a in records if a[0] > 0]
        self.expenses = [-a[0] for a in records if a[0] < 0]

    def balance(self) -> float:
        return self.initialBalance + sum(i[0] for i in self.incomes) - sum(self.expenses)

    def edit_balance(self, balance: float):
        oldBalance = self.initialBalance
        self.initialBalance = abs(balance)
        self.logs.append((datetime.now(ZoneInfo("US/Pacific")), f"Edited balance from {oldBalance} to {self.initialBalance}"))

    def load_account(self, filename="data.txt"):
        file = open(filename, "a+")
        file.seek(0)
        first = file.readline()
        if not first:
            account_name = input("Enter account name: ")
            balance = float(input("Enter initial balance: "))
            file.write(f"{account_name}:{balance}\n")
        file.seek(0)
        return Class_Account(file)

    def open_account(self):
        filename = input("Enter new account filename (e.g., account2.txt): ")
        account_name = input("Enter account name: ")
        balance = float(input("Enter initial balance: "))
        with open(filename, "w") as f:
            f.write(f"{account_name}:{balance}\n")
        return self.load_account(filename)

    def close_account(self):
        if self.file:
            self.file.close()
            print("Account closed.")

    def switch_accounts(self):
        self.close_account()
        filename = input("Enter filename of account to load: ")
        return self.load_account(filename)
