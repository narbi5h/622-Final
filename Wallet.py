from classes import Account

#TESTING APPROVAL PROCESS IN GITHUB
# Testing approval - Jcllee99
#Testing pull and push - Jcllee99

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
        options = [Option("B", self.edit_balance), 
                   Option("I", self.add_income), 
                   Option("E", self.add_expense),
                   Option("VB", self.view_balance), 
                   Option("VI", self.view_incomes), 
                   Option("VE", self.view_expenses),

                    # mary added this line to add a new function as an option
                    Option("LA", self.list_all),          
                    Option("SA", self.switch_accounts),  
                    Option("CA", self.close_account),     
                    Option("OA", self.open_account),      
                    Option("TR", self.transfer),          
                    Option("UA", self.update_amount),    

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

    # Mary added this ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    def load_account(self, filename="data.txt"):
        file = open(filename, "a+")
        file.seek(0)
        first = file.readline()
        if not first:
            account_name = input("Enter account name: ")
            balance = getFloat("Enter initial balance: ")
            file.write(f"{account_name}:{balance}\\n")
        file.seek(0)
        self.account = Account(file)
        print(f"Loaded account '{self.account.name}'")

    def open_account(self):
        filename = input("Enter new account filename (e.g., account2.txt): ")
        account_name = input("Enter account name: ")
        balance = getFloat("Enter initial balance: ")
        with open(filename, "w") as f:
            f.write(f"{account_name}:{balance}\\n")
        self.load_account(filename)

    def close_account(self):
        if self.account:
            self.account.file.close()
            self.account = None
            print("Account closed.")

    def switch_accounts(self):
        self.close_account()
        filename = input("Enter filename of account to load: ")
        self.load_account(filename)

    def list_all(self):
        all_records = self.account.incomes + self.account.expenses
        all_records.sort(key=lambda x: x.datetime)
        for record in all_records:
            print(record)

    def transfer(self):
        target_file = input("Enter filename of account to transfer TO: ")
        amount = getFloat("Enter amount to transfer: ")
        if amount > self.account.balance():
            print("Not enough funds to transfer.")
            return
        note = input("Enter note for the transfer: ")
        self.account.add_expense(amount, category="Transfer", note=note)

        with open(target_file, "r+") as f:
            from classes import Account as TargetAccount
            target = TargetAccount(f)
            target.add_income(amount, category="Transfer", note=f"Received from {self.account.name}")
        print("Transfer complete.")

    def update_amount(self):
        all_records = self.account.incomes + self.account.expenses
        for idx, record in enumerate(all_records):
            print(f"{idx}: {record}")
        idx = int(input("Enter index of record to update: "))
        new_amount = getFloat("Enter new amount: ")
        if idx < len(self.account.incomes):
            self.account.incomes[idx].amount = abs(new_amount)
        else:
            self.account.expenses[idx - len(self.account.incomes)].amount = abs(new_amount)
        print("Record updated in memory. (Note: File update not implemented.)")

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
                  LA = List all transactions        
                  SA = Switch account              
                  OA = Open new account            
                  CA = Close current account       
                  TR = Transfer to another account 
                  UA = Update a transaction amount 
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