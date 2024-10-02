import unittest
import pandas as pd
from datetime import datetime
from etl import *
import os


class TransactionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load the DataFrame from a CSV file before running any tests."""
        cls.csv_file = 'retail_15_01_2022.csv'
        if not os.path.exists(cls.csv_file):
            raise FileNotFoundError(f"CSV file '{cls.csv_file}' not found.")

        # Load the CSV file into a DataFrame
        cls.df = pd.read_csv(cls.csv_file)
        cls.transaction_date = datetime(2022, 1, 15)

    def test_number_of_transactions_on_15_01_2022(self):
        """Test that the number of transactions matches the expected value."""
        # Suppose we know the expected number of transactions for this date.
        expected_nb_transactions = 54
        actual_nb_transactions = len(self.df)
        self.assertEqual(actual_nb_transactions, expected_nb_transactions,
                         f"Expected {expected_nb_transactions} transactions but got {actual_nb_transactions}.")

    def test_transform_dataFrame(self):
        """Test the transformation of the DataFrame."""
        transformed_df = transform_dataframe(self.df.copy(), self.transaction_date)
        self.assertIn('transaction_date', transformed_df.columns,
                      "The 'transaction_date' column was not inserted.")
        self.assertTrue((transformed_df['transaction_date'] == self.transaction_date).all(),
                        "The 'transaction_date' column does not have the correct value.")

        self.assertIn('name', transformed_df.columns, "The 'description' column was not renamed to 'name'.")
        self.assertNotIn('description', transformed_df.columns, "The 'description' column still exists after renaming.")


if __name__ == '__main__':
    unittest.main()
