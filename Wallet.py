from classes import Account

#TESTING APPROVAL PROCESS IN GITHUB
import pandas as pd




def getFloat(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a number.")


class Menu:
    def __init__(self):
        file = open('data.txt', "a+")
        file.seek(0)
        first = file.readline()
        if not first:
            account_name = input("Enter account name: ")
            balance = getFloat("Enter initial balance: ")
            file.write(f"{account_name}:{balance}\n")
        file.seek(0)
        self.account = Account(file)
        self.quit = False
        options = [Option("B", self.edit_balance), Option("I", self.add_income), Option("E", self.add_expense),
                   Option("VB", self.view_balance), Option(
                       "VI", self.view_incomes)
                       , Option("VE", self.view_expenses),
                   Option("Q", self.exit)]
        # TODO: add new functions as options (no sub menu)
        self.options = {option.code: option for option in options}

    def edit_balance(self):
        amount = getFloat("Enter Balance:")
        self.account.edit_balance(amount)

    def add_income(self):
        amount = getFloat("Enter Income:")
        self.account.add_income(amount)

    def add_expense(self):
        success = False
        while not success:
            amount = getFloat("Enter Expense:")
            if amount > self.account.balance():
                print("Not enough funds.")
            else:
                success = True
        self.account.add_expense(amount)

    def view_balance(self):
        print(f"Current balance of Account '{self.account.name}': {self.account.balance()}")

    def view_incomes(self):
        for income in self.account.incomes:
            print(f"{income}")
        Total_income = sum(income.amount for income in self.account.incomes)
        print(f"Total income: {Total_income}")

    def view_expenses(self):
        for expense in self.account.expenses:
            print(f"{expense}")
        Total_expense = sum(expense.amount for expense in self.account.expenses)
        print(f"Current Expense: {Total_expense}")

    def exit(self):
        self.quit = True

    def loop(self):
        self.quit = False
        while not self.quit:
            print("""Please choose from the following actions:
                  B = Edit balance
                  I = Add income
                  E = Add expenditure
                  VB = View balance
                  VI = View incomes
                  VE = View expenditures
                  Q = Quit program
                """)
            try:
                self.options[input("Option: ")].execute()
            except KeyError:
                print("Please enter a valid option.")


class Option:
    def __init__(self, code: str, func):
        self.code = code
        self.execute = func


Menu().loop()