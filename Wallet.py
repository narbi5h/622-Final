from Class_Account import Account  
from Class_Transaction import Transaction  

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
        self.transaction = Transaction()
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
        self.transaction.add_income(self.account, amount)

    def add_expense(self):
        amount = getFloat("Enter Expense:")
        try:
            self.transaction.add_expense(self.account, amount)
        except ValueError as e:
            print(e)

    def open_account(self):
        self.account = self.account.open_account()

    def close_account(self):
        self.account.close_account()

    def switch_accounts(self):
        self.account = self.account.switch_accounts()

    def list_all(self):
        for record in self.transaction.list_all():
            print(record)

    def transfer(self):
        target_file = input("Enter filename of account to transfer TO: ")
        amount = getFloat("Enter amount to transfer: ")
        note = input("Enter note for the transfer: ")
        result = self.transaction.transfer(self.account, target_file, amount, note)
        print(result)

    def update_amount(self):
        self.transaction.update_amount(self.account)


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