# 💰 Wallet App – Personal Finance Tracker

A lightweight, console-based personal finance tracker built with Python and SQLite. Designed for simplicity and modularity, this app helps users manage income, expenses, transfers, and account summaries all from the command line.

## 🚀 Features

- Create and manage multiple user accounts
- Add and categorize income and expenses
- Transfer funds between accounts
- View account balance and transaction history
- Export and view logs by index, timestamp, or balance
- Manage categories and transaction types
- Supports account types like checking and savings
- Modular object-oriented structure for scalability

## 🏗️ Project Structure

| Component         | Description                                         |
|------------------|-----------------------------------------------------|
| `Wallet.py`       | Main entry point; handles menu and user input      |
| `Class_Account.py`| Account logic (create, switch, close, balance)     |
| `Class_User.py`   | User creation, login, authentication, password reset |
| `Class_Transaction.py` | Transaction logic for income, expense, transfer |
| `Export_Logs.py`  | Export logs sorted/searched by index, time, balance |
| `TRANSACTION_TYPE.py` | Manage transaction type       |
| `Categories.py`   | Manage income/expense categories                   |
| `Class_Account_type.py` | Dictionary for account types            |

## 🧱 Technologies Used

- **Python 3**
- **SQLite3**
- Object-Oriented Programming
- Database Normalization (3NF)

## 📦 Installation

1. **Clone the repo**:
   ```bash
   git clone https://github.com/yourusername/wallet-app.git
   cd wallet-app
   ```

2. **Run the app**:
   ```bash
   python Wallet.py
   ```

## 🧑‍💻 How to Use

Once the app starts:

1. Create or log into a user account.
2. Open or switch between financial accounts.
3. Use menu options to:
   - `I`: Add income
   - `E`: Add expense
   - `VB`: View balance
   - `TR`: Transfer between accounts
   - `LA`: List all transactions
   - And many more...

Use the full text-based menu to navigate all available features.

## 📊 Sample Functionalities

- **Add Income/Expense**
- **View Sorted Logs**
- **Search by Balance or Transaction Type**
- **Group Transaction Types Alphabetically**

## 📚 Learning & Reflection

This project emphasized:
- Efficient use of object-oriented principles
- Parallel development with modular classes
- Hands-on application of ERD to real database schema
- Functional CLI tools mimicking real-world banking operations

## 🤝 Contributors

- Mary Reynosa  
- Ameya Patil  
- Julian Amberg  
- Gio Villasenor  
- Jeffrey Lee  
- Jeffrey Brown

Instructor: Dr. Pouyan Eslami  
Course: BANA 620

## 📄 License

This project is for educational purposes. You can adapt or expand it for personal use.
