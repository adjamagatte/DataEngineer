import sqlite3

# Function to connect to the SQLite database
def connect_to_database(db_path):
    """Establish a connection to the SQLite database."""
    try:
        return sqlite3.connect(db_path)
    except sqlite3.Error as e:
        raise Exception(f"Database connection error: {e}")


# Function to get the number of transactions on 14/01/2022
def get_number_of_transactions(cursor, date):
    """Return the number of transactions on a specific date."""
    cursor.execute("SELECT COUNT(*) AS number_of_transactions FROM transactions WHERE transaction_date = ?;", (date,))
    row_counts = cursor.fetchone() # Use fetchone() since there's only one result
    return row_counts[0] if row_counts else 0  # Handle case where there are no results


# Function to get the total amount of sell transactions
def get_total_sell_transactions(cursor):
    """Return the total amount of sell transactions including tax."""
    cursor.execute("""
        SELECT SUM(amount_inc_tax) AS total_amount_sell_transactions_incltax  
        FROM transactions   
        WHERE category = 'SELL';
    """)
    total_row = cursor.fetchone()
    return total_row[0] if total_row else 0



# Consider the product Amazon Echo Dot:
#   What is the balance (SELL - BUY) by date?
# Function to get balance (SELL - BUY) by date for a specific product
def get_balance_by_date(cursor, product_name):
    """Return balance (SELL - BUY) by transaction date for a specific product."""
    cursor.execute("""
        SELECT   
            transaction_date,   
            SUM(CASE   
                WHEN category = 'SELL' THEN amount_inc_tax   
                WHEN category = 'BUY' THEN -amount_inc_tax   
                ELSE 0   
            END) AS balance  
        FROM   
            transactions   
        WHERE   
            name = ?   
        GROUP BY   
            transaction_date   
        ORDER BY   
            transaction_date;
    """, (product_name,))
    return cursor.fetchall()

# (Optional) What is the cumulated balance (SELL - BUY) by date?
# Function to get cumulative balance by date
def get_cumulative_balance(cursor):
    """Return cumulative balance (SELL - BUY) by date."""
    cursor.execute("""
        WITH DailyBalances AS (  
            SELECT   
                transaction_date,   
                SUM(CASE   
                    WHEN category = 'SELL' THEN amount_inc_tax   
                    WHEN category = 'BUY' THEN -amount_inc_tax   
                    ELSE 0   
                END) AS daily_balance  
            FROM   
                transactions   
            GROUP BY   
                transaction_date   
        )  
        SELECT   
            transaction_date,   
            SUM(daily_balance) OVER (ORDER BY transaction_date) AS cumulated_balance  
        FROM   
            DailyBalances  
        ORDER BY   
            transaction_date;
    """)
    return cursor.fetchall()


# Main function to run the queries
def main():
    db_path = 'retail.db'

    with connect_to_database(db_path) as conn:
        cursor = conn.cursor()

        # Get the number of transactions on 14/01/2022
        date_query = '2022-01-14'
        number_of_transactions = get_number_of_transactions(cursor, date_query)
        print(f"Number of transactions on {date_query}: {number_of_transactions}")

        # Get the total amount of SELL transactions
        total_amount = get_total_sell_transactions(cursor)
        print(f"Total Amount of Sell Transactions (including tax): {total_amount:.2f}")

        # Get balance for the product "Amazon Echo Dot"
        product_name = 'Amazon Echo Dot'
        balances = get_balance_by_date(cursor, product_name)
        print("Transaction Date       | Balance")
        print("------------------|------------------")
        for transaction_date, balance in balances:
            print(f"{transaction_date} | {balance:.2f}")

        # Get cumulative balance by date
        cumulative_balances = get_cumulative_balance(cursor)
        print("\nTransaction Date       | Cumulated Balance")
        print("------------------------|------------------")
        for transaction_date, cumulated_balance in cumulative_balances:
            print(f"{transaction_date} | {cumulated_balance:.2f}")


if __name__ == "__main__":
    main()