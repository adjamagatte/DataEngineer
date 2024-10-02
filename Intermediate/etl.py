import sqlite3
import pandas as pd
import re
import os  # Import os for file existence checking
from datetime import datetime

DB_PATH = 'retail.db'
FILENAME = 'retail_15_01_2022.csv'
TAX_RATE = 0.20


# Extract
def extract_data(filename):
    """Extract data from the CSV file into a pandas DataFrame.

    Args:
        filename: Path to the CSV file.

    Returns:
        DataFrame containing the extracted data.

    Raises:
        FileNotFoundError: If the specified CSV file does not exist.
    """
    try:
        return pd.read_csv(filename)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {e}")
    except Exception as e:
        raise Exception(f"An error occurred while reading the file: {e}")

# Transform
def extract_date_from_filename(filename):
    """Extract the date part from the name of the file using regex.

    Args:
        filename: Name of the CSV file.

    Returns:
        Extracted date in 'dd_mm_yyyy' format.

    Raises:
        ValueError: If the date is not found in the filename.
    """
    match = re.search(r'_(\d{2}_\d{2}_\d{4})', filename)
    if match:
        return match.group(1)
    raise ValueError("Date not found in the filename")


def transform_value_to_date(value):
    """Convert string to datetime.

    Args:
        value: Date string in 'dd_mm_yyyy' format.

    Returns:
        Corresponding datetime object.
    """
    try:
        return pd.to_datetime(value, format='%d_%m_%Y')
    except ValueError as e:
        raise ValueError(f"Error converting string to date: {e}")


def transform_dataframe(df, transaction_date):
    """Transform the DataFrame by adding a transaction_date column and renaming description to name.

    Args:
        df: DataFrame containing the data.
        transaction_date: Date of the transaction.

    Returns:
        Transformed DataFrame with new columns and renamed columns.
    """
    df.insert(1, 'transaction_date', transaction_date)
    df.rename(columns={"description": "name"}, inplace=True)
    return df

# Load
def load_data(df, db_path):
    """Load the transformed data into the SQLite database.

    Args:
        df: DataFrame containing the data to load.
        db_path: Path to the SQLite database.
    """

    # Check if the database path exists
    if not os.path.isfile(db_path):
        raise FileNotFoundError(f"The database file '{db_path}' does not exist.")
    try:
        with sqlite3.connect(db_path) as conn:
            df.to_sql('transactions', conn, if_exists='append', index=False)
            print(f"{len(df)} lines were successfully loaded into the database.")
    except sqlite3.DatabaseError as e:
        raise Exception(f"Database error: {e}")

# Main function
if __name__ == "__main__":
    try:
        # Extract step
        df = extract_data(FILENAME)
        print(f"Extracted {len(df)} rows from {FILENAME}.")  # Print number of rows extracted

        # Transform steps
        date_str = extract_date_from_filename(FILENAME)
        print(f"Extracted date: {date_str}")  # Print the extracted date
        transaction_date = transform_value_to_date(date_str)
        df = transform_dataframe(df, transaction_date)

        # Load step
        load_data(df, DB_PATH)

    except Exception as e:
        print(f"An error occurred: {e}")  # Catch and print any exceptions
