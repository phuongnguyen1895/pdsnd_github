import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington?\n').lower()
        
        if city in CITY_DATA:
            break
        else:
            print('Invalid input. Please enter a valid city name.')
            
    # get time filter preference
    while True:
        time_filter = input('Would you like to filter the data by month, day, both, or not at all? Type "none" for no time filter\n').lower()
        
        if time_filter in ['month', 'day', 'both', 'none']:
            if time_filter == 'month':
                month = filter_by_month()
                day = 'all'
            elif time_filter == 'day':
                day = filter_by_day()
                month = 'all'
            elif time_filter == 'both':
                month = filter_by_month()
                day = filter_by_day()
            else:
                month = 'all'
                day = 'all'
            break
        else:
            print('Invalid input. Please enter a valid time filter or "none".')

    print('-'*40)
    return city, month, day


def filter_by_month():
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Which month? January, February, March, April, May, or June?\n').lower()
        
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print('Invalid input. Please enter a valid month name or "all".')

    return month


def filter_by_day():
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Which day? Please type a day of the week (e.g., Monday) or "all" to apply no day filter.\n').lower()
        
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print('Invalid input. Please enter a valid day name or "all".')

    return day


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
    # Load data file for the specified city
    file_name = CITY_DATA[city]
    df = pd.read_csv(file_name)
    
    # Convert 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Extract month and day of week from 'Start Time'
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding integer
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    
    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('The most common month:', most_common_month)

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('The most common day of week:', most_common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('The most common start hour:', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station:', most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station:', most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('The most frequent combination of start station and end station trip:', most_common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', total_travel_time, 'seconds')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:', mean_travel_time, 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
  

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_counts = df['User Type'].value_counts()
    print('Counts of user types:')
    for user_type, count in user_types_counts.items():
        print(f'{user_type}: {count}')

    # Display counts of gender if 'Gender' column exists
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print('\nCounts of gender:')
        for gender, count in gender_counts.items():
            print(f'{gender}: {count}')
    else:
        print('\nGender data not available.')

    # Display earliest, most recent, and most common year of birth if 'Birth Year' column exists
    if 'Birth Year' in df:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        print('\nEarliest year of birth:', int(earliest_birth_year))
        print('Most recent year of birth:', int(most_recent_birth_year))
        print('Most common year of birth:', int(most_common_birth_year))
    else:
        print('\nBirth year data not available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
