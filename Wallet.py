from Class_Account_type import AccountType
from Class_User import User
from Class_Account import Class_Account  
from Export_Logs import exportLogs
from Class_Transaction import Transaction  
from TRANSACTION_TYPE import TRANSACTION_TYPE
from Categories import Categories
from classes import Record, Income, Expense, Account
import pandas as pd
from datetime import datetime

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
        self.account = Class_Account(file)
        self.transaction = Transaction()
        self.export_logs = exportLogs()
        self.quit = False
        self.user = User()
        self.account_type = AccountType()
        self.categories = Categories()
        self.transaction_type = TRANSACTION_TYPE()
        options = [
            Option("B", self.edit_balance), 
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
            # adding new functions as options (no sub menu)
            Option("XL", self.view_logs_by_index),
            Option("XT", self.view_logs_by_timestamp),
            Option("XF", self.find_log_by_id),
            Option("XB", self.find_log_by_balance), 
            Option("CU", self.create_user),
            Option("LU", self.login_user),
            Option("FPW", self.forgot_password),
            Option("AAT", self.add_account_type),
            Option("LAT", self.list_account_types),
            Option("CNAT", self.change_account_type_name),
            Option("DACT", self.disable_account_type),
            Option("ENACT", self.enable_account_type),
            Option("GAT", self.get_account_type_details),
            Option("AC", self.add_category),
            Option("UC", self.update_category),
            Option("DC", self.delete_category),
            Option("LC", self.list_categories),
            Option("SC", self.sort_categories),
            Option("LTT", self.list_transaction_types),
            Option("ATT", self.add_transaction_type),
            Option("UTT", self.update_transaction_type_name),
            Option("DTT", self.delete_transaction_type),
            Option("STT", self.search_transaction_type),
            Option("GTT", self.group_transaction_types),
            Option("ADA", self.add_account_for_user),
            Option("CLA", self.close_user_account),
            Option("FZA", self.freeze_account),
            # Q to exit
            Option("Q", self.exit)
            ]
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

    def view_logs_by_index(self):
        for log in self.export_logs.sortByIndex():
            print(log)

    def view_logs_by_timestamp(self):
        for log in self.export_logs.sortByTimestamp():
            print(log)

    def find_log_by_id(self):
        try:
            log_id = int(input("Enter Export Log ID: "))
            print(self.export_logs.findByIndex(log_id))
        except ValueError:
            print("Please enter a valid integer.")

    def find_log_by_balance(self):
        try:
            balance = float(input("Enter Balance to search for: "))
            for log in self.export_logs.findByAmount(balance):
                print(log)
        except ValueError:
            print("Please enter a valid number.")
    
    def create_user(self):
        name = input("Name: ")
        email = input("Email: ")
        username = input("Username: ")
        password = input("Password: ")
        self.user.create(name, email, username, password)
        print("User created.")

    def login_user(self):
        username = input("Username: ")
        password = input("Password: ")
        if self.user.authenticate(username, password):
            print("Login successful.")
        else:
            print("Login failed.")

    def forgot_password(self):
        username = input("Username: ")
        new_password = input("New password: ")
        self.user.forgot_password(username, new_password)
        print("Password has been reset.")

    def add_account_type(self):
        name = input("Account Type Name: ")
        description = input("Description: ")
        self.account_type.add_account_type(name, description)
        print("Account type added.")

    def list_account_types(self):
        types = self.account_type.list_all()
        for t in types:
            print(t)

    def list_transaction_types(self):
        for ttype in self.transaction_type.LIST_ALL():
            print(ttype)

    def add_category(self):
        name = input("Category name: ")
        print(self.categories.add(name))

    def list_categories(self):
        categories = self.categories.view()
        for c in categories:
            print(c)


    def add_account_for_user(self):
        user_id = int(input("User ID: "))
        name = input("Account Name: ")
        balance = getFloat("Initial Balance: ")
        self.user.add_account(user_id, name, balance)
        print("Account added.")

    def close_user_account(self):
        account_id = int(input("Account ID to close: "))
        self.user.close_account(account_id)
        print("Account closed.")

    def freeze_account(self):
        account_id = int(input("Account ID to freeze: "))
        self.user.freeze_account(account_id)
        print("Account frozen.")

    def change_account_type_name(self):
        type_id = int(input("Account Type ID: "))
        new_name = input("New Name: ")
        self.account_type.change_account_type_name(type_id, new_name)
        print("Account type name updated.")

    def disable_account_type(self):
        type_id = int(input("Account Type ID to disable: "))
        self.account_type.disable_account(type_id)
        print("Account type disabled.")

    def enable_account_type(self):
        type_id = int(input("Account Type ID to enable: "))
        self.account_type.enable_account(type_id)
        print("Account type enabled.")

    def get_account_type_details(self):
        type_id = int(input("Account Type ID: "))
        print(self.account_type.get_account_details(type_id))

    def update_category(self):
        category_id = int(input("Category ID: "))
        new_name = input("New Name: ")
        print(self.categories.update(category_id, new_name))

    def delete_category(self):
        category_id = int(input("Category ID to delete: "))
        print(self.categories.delete(category_id))

    def sort_categories(self):
        for row in self.categories.sort():
            print(row)

    def add_transaction_type(self):
        type_id = int(input("Transaction Type ID: "))
        name = input("Category Name: ")
        print(self.transaction_type.ADD(type_id, name))

    def update_transaction_type_name(self):
        type_id = int(input("Transaction Type ID: "))
        new_name = input("New Name: ")
        print(self.transaction_type.UPDATE_NAME(type_id, new_name))

    def delete_transaction_type(self):
        type_id = int(input("Transaction Type ID to delete: "))
        print(self.transaction_type.DELETE_TYPE(type_id))

    def search_transaction_type(self):
        keyword = input("Keyword to search: ")
        for result in self.transaction_type.SEARCH(keyword):
            print(result)

    def group_transaction_types(self):
        grouped = self.transaction_type.GROUP()
        for letter, types in grouped.items():
            print(f"{letter}:")
            for t in types:
                print(f"  {t}")

    def exit(self):
        self.quit = True

    def loop(self):
        self.quit = False
        while not self.quit:
            print("""
            Please choose from the following actions:

            Account Operations:
            B = Edit balance       I = Add income         E = Add expenditure
            VB = View balance      VI = View incomes      VE = View expenditures
            LA = List transactions TR = Transfer funds    UA = Update transaction
            OA = Open account      SA = Switch account    CA = Close account

            Export Logs:
            XL = Logs by index     XT = Logs by timestamp
            XF = Find log by ID    XB = Find logs by balance

            User Management:
            CU = Create user       LU = Login user        FPW = Forgot password
            ADA = Add user account CLA = Close user acct  FZA = Freeze account

            Account Types:
            AAT = Add type         LAT = List types       CNAT = Change type name
            DACT = Disable type    ENACT = Enable type    GAT = Get type details

            Categories:
            AC = Add category      UC = Update category   DC = Delete category
            LC = List categories   SC = Sort categories

            Transaction Types:
            LTT = List types       ATT = Add type         UTT = Update type
            DTT = Delete type      STT = Search types     GTT = Group types

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