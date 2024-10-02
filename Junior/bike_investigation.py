import pandas as pd
import time

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some bikeshare data!")

    # List of valid cities, months, and days
    cities = ["chicago", "new york city", "washington"]
    months = ["january", "february", "march", "april", "may", "june", "all"]
    # days = list(calendar.day_name)
    # days.append("all")
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]


    # Get user input for city
    while True:
        city = input("Please choose a city (chicago, new york city, washington): ").lower()
        if city in cities:
            break
        else:
            print("Invalid city! Please enter one of the following: chicago, new york city, washington.")


    # Get user input for month
    while True:
        month = input("Please choose a month (january, february, ..., june) or 'all' for no filter: ").lower()
        if month in months:
            break
        else:
            print("Invalid month! Please enter one of the following: january, february, march, april, may, june, or 'all'.")

    # Get user input for day of the week
    while True:
        day = input("Please choose a day of the week (monday, tuesday, ..., sunday) or 'all' for no filter: ").lower()
        if day in days:
            break
        else:
            print("Invalid day! Please enter one of the following: monday, tuesday, wednesday, thursday, friday, saturday, sunday, or 'all'.")

    print("-" * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    try:
        df = pd.read_csv("Bike_raw_data/" + CITY_DATA[city])
    except FileNotFoundError:
        print(f"Data file for {city} not found.")
        return pd.DataFrame()  # Return an empty DataFrame

    # Convert the 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from 'Start Time' to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]

    if df.empty:
        print("There is no data for the selected time period.")

    return df


def time_stats(df):
    """Displays and returns statistics on the most frequent times of travel if data is available.
    input: df
    output: mostCommonMonth,mostCommonDay, mostCommonHour """

    if df.empty:
        print("There is no data to display statistics.")
        return {}

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # Display the most common month
    most_common_month = df['month'].mode()[0]
    print(f"The most common month is: {most_common_month}")

    # Display the most common day of the week
    most_common_day = df['day_of_week'].mode()[0]
    print(f"The most common day of the week is: {most_common_day}")

    # Display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print(f"The most common start hour is: {most_common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)
    # Return the statistics as a dictionary
    return {
        'mostCommonMonth': most_common_month,
        'mostCommonDay': most_common_day,
        'mostCommonHour': most_common_hour
    }



def station_stats(df):
    """Displays and returns statistics on the most popular stations and trip.
    inpurt: df
    output: mostCommonStartStation, mostCommonEndsStation, mostCommonTrip """
    if df.empty:
        print("There is no data to display statistics.")
        return {}

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # TO DO: Display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station is: {most_common_start_station}")

    # TO DO: Display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station is: {most_common_end_station}")

    # TO DO: Display most frequent combination of start station and end station trip
    most_common_trip = (df['Start Station'] + " to " + df['End Station']).mode()[0]
    print(f"The most frequent combination of start station and end station trip is: {most_common_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)
    # Return the statistics as a dictionary
    return {
        'mostCommonStartStation': most_common_start_station,
        'mostCommonEndStation': most_common_end_station,
        'mostCommonTrip': most_common_trip
    }


def trip_duration_stats(df):
    """Displays and returns statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # Check if 'Trip Duration' column exists in the DataFrame
    if 'Trip Duration' not in df.columns:
        print("Trip Duration data is not available for this dataset.")
        return {}

    # Calculate total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time: {total_travel_time} seconds")

    # Calculate mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean travel time: {mean_travel_time} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)

    # Return the statistics as a dictionary
    return {
        'totalTravelTime': total_travel_time,
        'meanTravelTime': mean_travel_time
    }


def user_stats(df):
    """Displays and returns statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    user_stats_data = {}  # Initialize a dictionary to store the results

    # Check if 'User Type' column exists in the DataFrame
    if 'User Type' in df.columns:
        # Display counts of user types
        user_types_counts = df['User Type'].value_counts().to_dict()
        user_stats_data['User Types'] = user_types_counts
        print("Counts of user types:\n", user_types_counts)
    else:
        print("\nUser type data is not available for this dataset.")

    # Check if 'Gender' column exists in the DataFrame
    if 'Gender' in df.columns:
        # Display counts of gender
        gender_counts = df['Gender'].value_counts().to_dict()
        user_stats_data['Gender'] = gender_counts
        print("\nCounts of gender:")
        print(gender_counts)
    else:
        print("\nGender data is not available for this city.")

    # Check if 'Birth Year' column exists in the DataFrame
    if 'Birth Year' in df.columns:
        user_stats_data['Earliest Year of Birth'] = int(df['Birth Year'].min())
        user_stats_data['Most Recent Year of Birth'] = int(df['Birth Year'].max())
        user_stats_data['Most Common Year of Birth'] = int(df['Birth Year'].mode()[0])
        print("\nEarliest year of birth:", user_stats_data['Earliest Year of Birth'])
        print("Most recent year of birth:", user_stats_data['Most Recent Year of Birth'])
        print("Most common year of birth:", user_stats_data['Most Common Year of Birth'])
    else:
        print("\nBirth year data is not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)

    return user_stats_data  # Return the statistics as a dictionary


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if df.empty:
            print("There is no data to display statistics.")
            continue
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break

if __name__ == "__main__":
    main()
