from Class_Account_type import AccountType
from Class_User import User
from Class_Account import Class_Account  
from Export_Logs import exportLogs
from Class_Transaction import Transaction  
from TRANSACTION_TYPE import TRANSACTION_TYPE
from Categories import Categories
from classes import Record, Income, Expense, Account
from datetime import datetime

def getFloat(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a number.")

class Menu:
    def __init__(self):
        self.quit = False
        self.user = User()
        self.account_type = AccountType()
        self.categories = Categories()
        self.transaction = Transaction()
        self.export_logs = exportLogs()
        self.transaction_type = TRANSACTION_TYPE()

        # User login or creation
        while True:
            choice = input("Are you an existing user? (Y/N): ").strip().upper()
            if choice == "N":
                self.create_user()
            elif choice == "Y":
                if self.login_user():
                    break
                else:
                    print("Login failed. Please try again.")
            else:
                print("Invalid input. Please enter 'Y' or 'N'.")

        # Select an account
        print(f"Welcome, {self.current_user['name']}!")

        self.user_id = self.current_user["user_id"]
        self.account_manager = Class_Account()
        accounts = self.account_manager.list_accounts(self.user_id)
        if not accounts:
            print("No accounts found. Let's create one.")
            name = input("Enter account type name (e.g. 'Checking'): ")
            balance = getFloat("Enter starting balance: ")
            self.account_id = self.account_manager.open_account(self.user_id, name, balance)
        else:
            self.account_id = self.account_manager.switch_accounts(self.user_id)

    def edit_balance(self):
        amount = getFloat("Enter Balance:")
        self.account_manager.edit_balance(self.account_id, amount)

    def add_income(self):
        amount = getFloat("Enter Income:")
        self.transaction.add_income(self.account_id, amount)

    def add_expense(self):
        amount = getFloat("Enter Expense:")
        category = input("Enter category (default is 'Other'): ") or "Other"
        try:
            self.transaction.add_expense(self.account_id, amount, category)
        except ValueError as e:
            print(e)

    def update_amount(self):
        self.transaction.update_amount(self.account_id)

    def view_balance(self):
        acc = self.account_manager.get_account(self.account_id)
        if acc:
            print(f"Current balance: {acc['balance']}")
        else:
            print("Account not found.")

    def view_incomes(self):
        for income in self.transaction.list_all(self.account_id):
            if income[2] == 1:
                print(income)
        Total_income = sum(t[0] for t in self.transaction.list_all(self.account_id) if t[2] == 1)
        print(f"Total income: {Total_income}")

    def view_expenses(self):
        for expense in self.transaction.list_all(self.account_id):
            if expense[2] == 2:
                print(expense)
        Total_expense = sum(t[0] for t in self.transaction.list_all(self.account_id) if t[2] == 2)
        print(f"Current Expense: {Total_expense}")

    def list_all(self):
        for record in self.transaction.list_all(self.account_id):
            print(record)

    def transfer(self):
        to_id = input("Enter destination account ID: ").strip()
        amount = getFloat("Enter amount to transfer: ")
        note = input("Enter note for the transfer: ")
        result = self.transaction.transfer(self.account_id, to_id, amount, note)
        print(result)


    def switch_accounts(self):
        self.account_id = self.account_manager.switch_accounts(self.user_id)

    def add_account_for_user(self):
        name = input("Account Type Name: ")
        balance = getFloat("Starting Balance: ")
        self.account_id = self.account_manager.open_account(self.user_id, name, balance)

    def close_user_account(self):
        account_id = input("Account ID to close: ")
        self.account_manager.close_account(account_id)

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
        self.user.create(username, name, email, password)
        print("User created.")

    def login_user(self):
        username = input("Username: ")
        password = input("Password: ")
        if self.user.authenticate(username, password):
            print("Login successful.")
            self.current_user = self.user.get_by_username(username)
            return True
        else:
            return False

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
        for t in self.account_type.list_all():
            print(t)

    def change_account_type_name(self):
        type_id = (input("Account Type ID: "))
        new_name = input("New Name: ")
        self.account_type.change_account_type_name(type_id, new_name)
        print("Account type name updated.")

    def disable_account_type(self):
        type_id = input("Account Type ID to disable: ")
        self.account_type.disable_account(type_id)
        print("Account type disabled.")

    def enable_account_type(self):
        type_id = (input("Account Type ID to enable: "))
        self.account_type.enable_account(type_id)
        print("Account type enabled.")

    def get_account_type_details(self):
        type_id = (input("Account Type ID: "))
        print(self.account_type.get_account_details(type_id))

    def add_category(self):
        name = input("Category name: ")
        print(self.categories.add(name))

    def update_category(self):
        category_id = (input("Category ID: "))
        new_name = input("New Name: ")
        print(self.categories.update(category_id, new_name))

    def delete_category(self):
        category_id = (input("Category ID to delete: "))
        print(self.categories.delete(category_id))

    def list_categories(self):
        for row in self.categories.view():
            print(row)

    def sort_categories(self):
        for row in self.categories.sort():
            print(row)

    def list_transaction_types(self):
        for ttype in self.transaction_type.LIST_ALL():
            print(ttype)

    def add_transaction_type(self):
        type_id = (input("Transaction Type ID: "))
        name = input("Category Name: ")
        print(self.transaction_type.ADD(type_id, name))

    def update_transaction_type_name(self):
        type_id = (input("Transaction Type ID: "))
        new_name = input("New Name: ")
        print(self.transaction_type.UPDATE_NAME(type_id, new_name))

    def delete_transaction_type(self):
        type_id = (input("Transaction Type ID to delete: "))
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
            B = Edit balance       I = Add income         E = Add expenditure
            VB = View balance      VI = View incomes      VE = View expenditures
            LA = List transactions TR = Transfer funds    UA = Update transaction
            OA = Open account      SA = Switch account    CA = Close account

            Export Logs:
            XL = Logs by index     XT = Logs by timestamp
            XF = Find log by ID    XB = Find logs by balance

            User Management:
            CU = Create user       LU = Login user        FPW = Forgot password
            ADA = Add user account CLA = Close user acct

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
                cmd = input("Option: ").upper()
                if cmd == "B": self.edit_balance()
                elif cmd == "I": self.add_income()
                elif cmd == "E": self.add_expense()
                elif cmd == "VB": self.view_balance()
                elif cmd == "VI": self.view_incomes()
                elif cmd == "VE": self.view_expenses()
                elif cmd == "UA": self.update_amount()
                elif cmd == "LA": self.list_all()
                elif cmd == "TR": self.transfer()
                elif cmd == "SA": self.switch_accounts()
                elif cmd == "CA": self.close_user_account()
                elif cmd == "OA": self.add_account_for_user()

                elif cmd == "XL": self.view_logs_by_index()
                elif cmd == "XT": self.view_logs_by_timestamp()
                elif cmd == "XF": self.find_log_by_id()
                elif cmd == "XB": self.find_log_by_balance()

                elif cmd == "CU": self.create_user()
                elif cmd == "LU": self.login_user()
                elif cmd == "FPW": self.forgot_password()

                elif cmd == "ADA": self.add_account_for_user()
                elif cmd == "CLA": self.close_user_account()

                elif cmd == "AAT": self.add_account_type()
                elif cmd == "LAT": self.list_account_types()
                elif cmd == "CNAT": self.change_account_type_name()
                elif cmd == "DACT": self.disable_account_type()
                elif cmd == "ENACT": self.enable_account_type()
                elif cmd == "GAT": self.get_account_type_details()

                elif cmd == "AC": self.add_category()
                elif cmd == "UC": self.update_category()
                elif cmd == "DC": self.delete_category()
                elif cmd == "LC": self.list_categories()
                elif cmd == "SC": self.sort_categories()

                elif cmd == "LTT": self.list_transaction_types()
                elif cmd == "ATT": self.add_transaction_type()
                elif cmd == "UTT": self.update_transaction_type_name()
                elif cmd == "DTT": self.delete_transaction_type()
                elif cmd == "STT": self.search_transaction_type()
                elif cmd == "GTT": self.group_transaction_types()

                elif cmd == "Q": self.exit()
                else: print("Invalid option.")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    Menu().loop()
