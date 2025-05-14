
from datetime import datetime
from zoneinfo import ZoneInfo

class Transaction:
    def __init__(self, incomes=None, expenses=None):
        self.incomes = incomes if incomes else []
        self.expenses = expenses if expenses else []

    def list_all(self):
        all_records = self.incomes + self.expenses
        all_records.sort(key=lambda x: x.datetime)
        return all_records

    def transfer(self, account, target_file, amount, note=""):
        if amount > account.balance():
            return "Not enough funds to transfer."

        account.add_expense(amount, category="Transfer", note=note)

        from Class_Account import Account as TargetAccount
        with open(target_file, "r+") as f:
            target = TargetAccount(f)
            target.add_income(amount, category="Transfer", note=f"Received from {account.name}")
        return "Transfer complete."

    def add_income(self, account, amount, category="Other", note=""):
        now = datetime.now(ZoneInfo("US/Pacific"))
        account.add_income(amount, now, category, note)

    def add_expense(self, account, amount, category="Other", note=""):
        if amount > account.balance():
            raise ValueError("Not enough funds.")
        now = datetime.now(ZoneInfo("US/Pacific"))
        account.add_expense(amount, now, category, note)

    def update_amount(self, account):
        all_records = account.incomes + account.expenses
        for idx, record in enumerate(all_records):
            print(f"{idx}: {record}")
        idx = int(input("Enter index of record to update: "))
        new_amount = float(input("Enter new amount: "))
        if idx < len(account.incomes):
            account.incomes[idx].amount = abs(new_amount)
        else:
            account.expenses[idx - len(account.incomes)].amount = abs(new_amount)
        print("Record updated in memory. (Note: File update not implemented.)")
