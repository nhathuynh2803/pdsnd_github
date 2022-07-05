from ast import Break
import string
import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}
cities = ['chicago', 'new york', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['sunday', 'monday', 'tuesday', 'wednesday',
        'thursday', 'friday', 'saturday', 'all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    month = ''
    day = ''
    while True:
        city = input(
            'please input the city? in (chicago, new york, washington)').lower()
        if(city in cities):
            break

    # Get user input for month (all, january, february, ... , june)
    while True:
        month = input('please input the month? ').lower()
        if(month in months):
            break

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('please input day of week? ').lower()
        if(day in days):
            break

    print('-'*40)
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
    file_name = CITY_DATA[city]
    df = pd.read_csv(file_name)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['weekday_name'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    if month != 'all':
        num_month = months.index(month) + 1
        df = df[df['month'] == num_month]
    if day != 'all':
        df = df[df['weekday_name'] == day]
    return df


def time_stats(df: pd.DataFrame):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    the_most_common_month = df['month'].value_counts().idxmax()
    print('The most common month is: ', the_most_common_month)

    # Display the most common day of week
    the_most_common_day_of_week = df['weekday_name'].value_counts().idxmax()
    print('The most common day of week is: ', the_most_common_day_of_week)

    # Display the most common start hour
    the_most_common_start_hour = df['hour'].value_counts().idxmax()
    print('The most common  hour is: ', the_most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df: pd.DataFrame):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_commonly_used_start_station = df['Start Station'].value_counts(
    ).idxmax()
    print('The most commonly used start station: ',
          most_commonly_used_start_station)

    # Display most commonly used end station
    most_commonly_used_end_station = df['End Station'].value_counts().idxmax()
    print('The most commonly used end station: ',
          most_commonly_used_end_station)

    # Display most frequent combination of start station and end station trip
    most_commonly_used_start_end_station = df.groupby(
        ['Start Station', 'End Station']).size().nlargest(1)
    print('The most frequent combination of start station and end station trip: {}; {}'.format(
        most_commonly_used_start_end_station.index[0][0], most_commonly_used_start_end_station.index[0][1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df: pd.DataFrame):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time: ', total_travel_time)

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df: pd.DataFrame, city: string):
    """Displays statistics on bike share users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of user types: ')
    user_counts = df['User Type'].value_counts()
    for index, value in enumerate(user_counts):
        print('{}, {}, {}'.format(
            index + 1, user_counts.index[index-1], value))

    # Display counts of gender
    if city.lower() != 'washington':
        print('Counts of gender: ')
        gender_counts = df['Gender'].value_counts()
        for index, value in enumerate(gender_counts):
            print('{}, {}, {}'.format(
                index + 1, gender_counts.index[index-1], value))

    # Display earliest, most recent, and most common year of birth
    if city.lower() != 'washington':
        birth_day_year = df['Birth Year']
        # 1. earliest
        earliest = birth_day_year.min()
        print("The most earliest year of birth: ", int(earliest))
        # 2. most recent
        most_recent = birth_day_year.max()
        print("The most recent year of birth: ", int(most_recent))
        # 3. most common
        most_common = birth_day_year.value_counts().idxmax()
        print("The most common year of birth: ", int(most_common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# Function to display the data frame itself as per user request
def show_data(df: pd.DataFrame):
    """Displays 5 rows of data from the csv file for the selected city.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """
    condition_list = ['yes', 'no']
    condition = ''
    page_index = 0
    page_size = 5
    while condition not in condition_list:
        condition = input(
            "\nWould you like to show raw data? Enter yes or no.\n").lower()
        if condition == 'yes':
            print(df.head())

    while condition == 'yes':
        page_index += page_size
        condition = input(
            "\nWould you like to show more raw data? Enter yes or no.\n").lower()
        # If user opts for it, this displays next 5 rows of data
        if condition == "yes":
            print(df[page_index:page_index+page_size])
        elif condition == 'no':
            break

    print('-'*80)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if(df.empty != True):
            show_data(df)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)
        else:
            print('Data is Empty')
        restart = input(
            '\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
    main()
