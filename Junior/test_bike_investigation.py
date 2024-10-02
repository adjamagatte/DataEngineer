import unittest
import pandas as pd
from bike_investigation import time_stats, station_stats, trip_duration_stats, user_stats



class TestBikeShareData(unittest.TestCase):

    def setUp(self):
        """
        This method is called before every test. It will initialize the DataFrame
        that will be used in all tests.
        """
        # The data as a dictionary
        data = {
            'Start Time': ['2017-01-01 09:07:57', '2017-01-02 09:07:57', '2017-01-03 00:07:57'],
            'End Time': ['2017-01-01 09:20:53', '2017-01-02 09:20:53', '2017-01-03 00:20:53'],
            'Start Station': ['Station A', 'Station B', 'Station A'],
            'End Station': ['Station B', 'Station A', 'Station B']
        }
        # TO DO : create a panda DataFrame from the data dictionary
        self.df = pd.DataFrame(data)

        # Convert 'Start Time' to datetime
        self.df['Start Time'] = pd.to_datetime(self.df['Start Time'])

        # Extract 'month', 'day_of_week', and 'hour' columns from 'Start Time'
        self.df['month'] = self.df['Start Time'].dt.month_name()
        self.df['day_of_week'] = self.df['Start Time'].dt.day_name()
        self.df['hour'] = self.df['Start Time'].dt.hour

    def test_time_stats(self):
        # Call the time_stats function and capture the result
        result = time_stats(self.df)

        # Test assertions based on the result dictionary
        self.assertEqual(result['mostCommonMonth'], 'January')  # All entries are in January
        self.assertEqual(result['mostCommonDay'],
                         'Monday')  # Mode of days ['Sunday', 'Monday', 'Tuesday'] is 'Monday' (first in mode)
        self.assertEqual(result['mostCommonHour'], 9)  # Hours are 9, 9, 0; mode is 9

        # self.assertEqual(result['mostCommonMonth'], ['january'])

    #def test_time_stats_missing_data(self):
    # TO DO : base on the above test, create tests for station_stats, trip_duration_stats and user_stats function. Make sure you cover common corner cases.

    def test_station_stats(self):
        # Call the station_stats function and capture the result
        result = station_stats(self.df)

        # Test assertions based on the result (assuming the function should return a dictionary)
        self.assertEqual(result['mostCommonStartStation'], 'Station A')  # The most commonly used start station
        self.assertEqual(result['mostCommonEndStation'], 'Station B')  # The most commonly used end station
        self.assertEqual(result['mostCommonTrip'], 'Station A to Station B')  # The most frequent trip

    def test_trip_duration_stats(self):
        # Prepare sample data
        data = {
            'Trip Duration': [300, 600, 1200, 1500, 900]
        }

        # Create a DataFrame from the dictionary
        df = pd.DataFrame(data)

        # Call the trip_duration_stats function and capture the result
        result = trip_duration_stats(df)

        # Test assertions based on the result
        expected_total_duration = sum(data['Trip Duration'])  # Total should be 3600 seconds
        expected_mean_duration = sum(data['Trip Duration']) / len(data['Trip Duration'])  # Mean should be 720 seconds

        self.assertEqual(result['totalTravelTime'], expected_total_duration)  # Check total duration
        self.assertEqual(result['meanTravelTime'], expected_mean_duration)  # Check mean duration


    def test_trip_duration_stats_missing_data(self):
        # Test with an empty DataFrame
        df_empty = pd.DataFrame()

        # Call the trip_duration_stats function with empty data
        result = trip_duration_stats(df_empty)

        # Test that the result is an empty dictionary
        self.assertEqual(result, {})

    def test_user_stats(self):
        # Prepare sample data
        data = {
            'User Type': ['Subscriber', 'Customer', 'Subscriber', 'Subscriber', 'Customer'],
            'Gender': ['Male', 'Female', 'Female', 'Male', 'Female'],
            'Birth Year': [1980, 1992, 1985, 1978, 1990]  # Added birth years for testing
        }

        # Create a DataFrame from the dictionary
        df = pd.DataFrame(data)

        # Call the user_stats function and capture the result
        result = user_stats(df)

        # Test assertions based on the result
        expected_user_types = {'Subscriber': 3, 'Customer': 2}
        expected_gender_counts = {'Male': 2, 'Female': 3}
        expected_birth_years = {
            'Earliest Year of Birth': df['Birth Year'].min(),  # 1978
            'Most Recent Year of Birth': df['Birth Year'].max(),  # 1992
            'Most Common Year of Birth': df['Birth Year'].mode()[0]  # 1985
        }

        self.assertEqual(result['User Types'], expected_user_types)  # Check user type counts
        self.assertEqual(result['Gender'], expected_gender_counts)  # Check gender counts
        self.assertEqual(result['Earliest Year of Birth'],
                         expected_birth_years['Earliest Year of Birth'])  # Check earliest year
        self.assertEqual(result['Most Recent Year of Birth'],
                         expected_birth_years['Most Recent Year of Birth'])  # Check most recent year
        self.assertEqual(result['Most Common Year of Birth'],
                         expected_birth_years['Most Common Year of Birth'])  # Check most common year

    def test_user_stats_missing_data(self):
        # Test with an empty DataFrame
        df_empty = pd.DataFrame()

        # Call the user_stats function with empty data
        result = user_stats(df_empty)

        # Test that the result is an empty dictionary
        self.assertEqual(result, {})


if __name__ == '__main__':
    unittest.main()