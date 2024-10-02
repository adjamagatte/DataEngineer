## [Python/data] Bike Sharing

In this project, we will make use of Python to explore data related to bike share systems for the three major cities in the United States - Chicago, New York City, and Washington.
We will write code to import the data and answer interesting questions about it by computing descriptive statistics.

### Data sets

Randomly selected data from https://www.capitalbikeshare.com/system-data for the first six months of 2017 are provided for all three cities. All three of the data files contain the same core six columns:

- Start Time (e.g., 23/06/2017 15:09:32)
- End Time (e.g., 23/06/2017 15:14:53)
- Trip Duration (in seconds - e.g., 321)
- Start Station (e.g., Wood St & Hubbard St)
- End Station (e.g., Damen Ave & Chicago Ave)
- User Type (Subscriber or Customer)


### Bike investigation ( see bike_investigation.py)
#### Data loading
We load bikeshare data based on user-specified filters for city, month, and day
The load_data() function reads the relevant CSV file for the chosen city, processes the data to extract month and day information, and applies the specified filters. 

For **performance** and **calculation efficiency**, I extracted data such as the month, hour, and day of the week from the 'Start Time' datetime column. By creating the necessary columns once, I avoid repeated extraction. This allows me to easily perform groupings (groupby), sorting, filtering, and other analyses without having to repeatedly process the 'Start Time' column. Otherwise, extracting the data each time can be computationally expensive, especially since I will be performing multiple analyses and repeated operations on these data.

#### Descriptive Analysis
For descriptive statistics, the functions utilize the `mode()` method to find the most common occurrences in time and station data, and the `value_counts()` method for categorical data such as user types and gender.

#### Data Verification
Each function includes a verification step to check if the DataFrame is empty after filtering, ensuring that operations are only performed on valid data. Input correctness for city, month, and day is also validated in the `get_filters` function.

---



#### Summary of Functions

1. **get_filters**:  
   This function prompts the user to input their desired city, month, and day to filter bikeshare data. It ensures input correctness by validating the user’s inputs before proceeding with the analysis.

2. **load_data**:  
   This function loads the data for the selected city and filters it by the specified month and day. Additionally, new columns (`month`, `day_of_week`, and `hour`) are created from the 'Start Time' column to allow for further analysis. A check is included to verify if the DataFrame is empty after filtering.

3. **time_stats**:  
   Displays and returns statistics on the most frequent times of travel, including the most common month, day of the week, and hour. The function first checks if the DataFrame is empty before performing the analysis. The `mode()` method is used to find the most common values.

4. **station_stats**:  
   This function calculates and returns the most commonly used start station, end station, and the most frequent combination of trips (from start to end station). It checks if the DataFrame is empty and uses the `mode()` method to find the most frequent stations.

5. **trip_duration_stats**:  
   Displays and returns statistics on the total and average trip duration. The function ensures the 'Trip Duration' column exists and calculates the sum and mean travel time.

6. **user_stats**:  
   Displays and returns statistics on bikeshare users, including user type counts and gender counts. Additionally, for NYC and Chicago datasets, it calculates and returns the earliest, most recent, and most common year of birth. It checks if relevant columns ('User Type', 'Gender', and 'Birth Year') exist in the DataFrame before performing the calculations. The `value_counts()` method is used for categorical data, and the `min()`, `max()`, and `mode()` methods are used to determine birth year statistics.

#### Tests cases (See test_bike_ivestigation.py)
The test file uses `unittest` to validate functions from the bikeshare analysis module. In all tests, assertions are made based on expected values from sample data. For some tests, data is dynamically generated, while for others, the `setUp` function is used to initialize a DataFrame based on a predefined data dictionary. The tests check for correct outputs in functions like `time_stats`, `station_stats`, `trip_duration_stats`, and `user_stats`. Additionally, tests for empty DataFrames ensure the functions handle missing data appropriately.

