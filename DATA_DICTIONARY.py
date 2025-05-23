import sqlite3
import pandas as pd
import os

def dataDictionary():
    """
    This function creates a data dictionary for the SQLite database.
    It reads CSV files, infers data types, and stores the data dictionary in a SQLite table.
    """
    # Optional: Change working directory if needed
    # os.chdir(r"Flat Files for DB")

    # Load CSVs
    csv_files = {
        "USER": "USER.csv",
        "ACCOUNT_TYPE": "ACCOUNT_TYPE.csv",
        "ACCOUNT": "ACCOUNT.csv",
        "TRANSACTION_TYPE": "TRANSACTION_TYPE.csv",
        "CATEGORIES": "CATEGORIES.csv",
        "TRANSACTION": "TRANSACTION.csv",
        "EXPORT_LOGS": "EXPORT_LOGS.csv"
    }

    # Dictionary to store dataframes
    dataframes = {table: pd.read_csv(file) for table, file in csv_files.items()}

    # Build data dictionary dynamically
    dataDictionaryRecords = []

    for table_name, df in dataframes.items():
        for column_name, dtype in df.dtypes.items():
            # Convert pandas dtype to SQLite equivalent
            if "int" in str(dtype):
                sql_type = "INTEGER"
            elif "float" in str(dtype):
                sql_type = "REAL"
            else:
                sql_type = "TEXT"

            dataDictionaryRecords.append((column_name, sql_type, table_name))

    # Convert list to DataFrame
    data_dictionary_df = pd.DataFrame(dataDictionaryRecords, columns=["Column name", "Type", "Table"])

    # Connect to SQLite database
    conn = sqlite3.connect("walletApp.db")
    cursor = conn.cursor()

    # Create table for data dictionary
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data_dictionary (
            column_name TEXT,
            data_type TEXT,
            table_name TEXT
        )
    """)

    # Insert data dictionary into SQLite table
    data_dictionary_df.to_sql("data_dictionary", conn, if_exists="replace", index=False)

    # Commit and close connection
    conn.commit()
    conn.close()

    print("Data dictionary has been successfully stored in SQLite.")
    return data_dictionary_df
