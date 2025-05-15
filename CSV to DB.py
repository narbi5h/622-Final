import sqlite3
import pandas as pd
import os
from DATA_DICTIONARY import dataDictionary

# Optional: Change working directory if needed
# os.chdir()

# === Step 1: Remove existing database ===
db_path = "walletApp.db"
if os.path.exists(db_path):
    os.remove(db_path)

# === Step 2: Load CSVs ===
user_df = pd.read_csv("Flat Files for DB/USER.csv")
account_type_df = pd.read_csv("Flat Files for DB/ACCOUNT_TYPE.csv")
account_df = pd.read_csv("Flat Files for DB/ACCOUNT.csv")
transaction_type_df = pd.read_csv("Flat Files for DB/TRANSACTION_TYPE.csv")
categories_df = pd.read_csv("Flat Files for DB/CATEGORIES.csv")
transaction_df = pd.read_csv("Flat Files for DB/TRANSACTION.csv")
export_logs_df = pd.read_csv("Flat Files for DB/EXPORT_LOGS.csv")

# === Step 3: Clean and transform data ===

## USERS
user_df.rename(columns={"pw": "password"}, inplace=True)
user_df = user_df.dropna(subset=["user_id", "username", "password"])
user_df["user_id"] = user_df["user_id"].astype(str).str.strip()
user_df["username"] = user_df["username"].astype(str).str.strip()
user_df["name"] = user_df["name"].astype(str).str.strip()
user_df["email"] = user_df["email"].astype(str).str.strip()
user_df["password"] = user_df["password"].astype(str).str.strip()

## ACCOUNT_TYPE
account_type_df = account_type_df.rename(columns={"account_type": "type_name", "type_name": "account_type"})
account_type_df["account_type"] = pd.factorize(account_type_df["account_type"])[0] + 1
# account_type_df["account_type"] = account_type_df["account_type"].astype(str).str.strip()
account_type_df["type_name"] = account_type_df["type_name"].astype(str).str.strip()
account_type_df["is_enabled"] = 1

## ACCOUNT
account_df = account_df.dropna(subset=["account_id", "user_id", "account_type", "balance"])
account_df["account_id"] = account_df["account_id"].astype(str).str.strip()
account_df["user_id"] = account_df["user_id"].astype(str).str.strip()
account_df["balance"] = account_df["balance"].astype(str).str.replace(",", "").astype(float)
account_df["account_type"] = account_df["account_type"].astype(str).str.strip()
type_map = dict(zip(account_type_df["type_name"], account_type_df["account_type"]))
account_df["account_type"] = account_df["account_type"].map(type_map)

## TRANSACTION_TYPE
transaction_type_df = transaction_type_df.dropna()
transaction_type_df["transaction_type_id"] = transaction_type_df["transaction_type_id"].astype(int)
transaction_type_df["category_name"] = transaction_type_df["category_name"].astype(str).str.strip()

## CATEGORIES
categories_df = categories_df.dropna()
categories_df["sub_category_id"] = categories_df["sub_category_id"].astype(str).str.strip()
categories_df["name"] = categories_df["name"].astype(str).str.strip()
categories_df["transaction_type_id"] = categories_df["transaction_type_id"].astype(int)

## TRANSACTIONS
transaction_df = transaction_df.dropna()
transaction_df["transaction_id"] = transaction_df["transaction_id"].astype(str).str.strip()
transaction_df["account_id"] = transaction_df["account_id"].astype(str).str.strip()
transaction_df["sub_category_id"] = transaction_df["sub_category_id"].astype(str).str.strip()
transaction_df["amount"] = transaction_df["amount"].astype(str).str.replace(",", "").astype(float)
transaction_df["timestamp"] = transaction_df["timestamp"].astype(str).str.strip()

# Merge with CATEGORIES to get type_id
transaction_df = transaction_df.merge(
    categories_df[["sub_category_id", "transaction_type_id"]],
    on="sub_category_id",
    how="left"
)
transaction_df.rename(columns={"transaction_type_id": "type_id"}, inplace=True)
# transaction_df = transaction_df.drop(columns=["sub_category_id"])
transaction_df["type_id"] = transaction_df["type_id"].astype(int)

## EXPORT_LOGS
export_logs_df = export_logs_df.dropna()
export_logs_df["export_id"] = export_logs_df["export_id"].astype(str).str.strip()
export_logs_df["account_id"] = export_logs_df["account_id"].astype(str).str.strip()
export_logs_df["timestamp"] = export_logs_df["timestamp"].astype(str).str.strip()
export_logs_df["file_path"] = export_logs_df["file_path"].astype(str).str.strip()

# === Step 4: Create SQLite database with correct schema ===
conn = sqlite3.connect(db_path)
conn.execute("PRAGMA foreign_keys = ON;")
cursor = conn.cursor()

cursor.executescript("""                     
CREATE TABLE IF NOT EXISTS ACCOUNT_TYPE (
    account_type INTEGER PRIMARY KEY,
    type_name TEXT NOT NULL,
    is_enabled INTEGER NOT NULL DEFAULT 1
);
                         
CREATE TABLE IF NOT EXISTS USERS (
    user_id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ACCOUNT (
    account_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    account_type INTEGER NOT NULL,
    balance REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES USERS(user_id),
    FOREIGN KEY (account_type) REFERENCES ACCOUNT_TYPE(account_type)
);

CREATE TABLE IF NOT EXISTS TRANSACTION_TYPE (
    transaction_type_id INTEGER PRIMARY KEY,
    category_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS CATEGORIES (
    sub_category_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    transaction_type_id INTEGER NOT NULL,
    FOREIGN KEY (transaction_type_id) REFERENCES TRANSACTION_TYPE(transaction_type_id)
);

CREATE TABLE IF NOT EXISTS TRANSACTIONS (
    transaction_id TEXT PRIMARY KEY,
    account_id TEXT NOT NULL,
    sub_category_id TEXT NOT NULL,
    type_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES ACCOUNT(account_id),
    FOREIGN KEY (type_id) REFERENCES TRANSACTION_TYPE(transaction_type_id)
    FOREIGN KEY (sub_category_id) REFERENCES CATEGORIES(sub_category_id)
);

CREATE TABLE IF NOT EXISTS EXPORT_LOGS (
    export_id TEXT PRIMARY KEY,
    account_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    file_path TEXT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES ACCOUNT(account_id)
);
""")

# === Step 5: Insert cleaned data ===
user_df.to_sql("USERS", conn, if_exists="append", index=False)
account_type_df.to_sql("ACCOUNT_TYPE", conn, if_exists="append", index=False)
account_df.to_sql("ACCOUNT", conn, if_exists="append", index=False)
transaction_type_df.to_sql("TRANSACTION_TYPE", conn, if_exists="append", index=False)
categories_df.to_sql("CATEGORIES", conn, if_exists="append", index=False)
transaction_df.to_sql("TRANSACTIONS", conn, if_exists="append", index=False)
export_logs_df.to_sql("EXPORT_LOGS", conn, if_exists="append", index=False)

conn.commit()
conn.close()

print("Database successfully created and populated.")

# === Step 6: Create Data Dictionary ===
dataDictionary = []