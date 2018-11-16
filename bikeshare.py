import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': '/Users/Jagadeesh/Desktop/Udacity/pdsnd_github/chicago.csv',
              'new york city': '/Users/Jagadeesh/Desktop/Udacity/pdsnd_github/new_york_city.csv',
              'washington': '/Users/Jagadeesh/Desktop/Udacity/pdsnd_github/washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington?: ')
        city = city.lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print(" enter valid city name: 'chicago' or 'new york city' or 'washington' ")
            continue
#        except ValueError:
#            print("Sorry, I didn't understand that.")
#            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)

    while True:
        month = input("What month do you like to filter the data by? \n (Enter the month as: january, february, ..., june) \n Enter 'all' to include all months for the analysis:  ")
        month = month.lower()
        if month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
            print(" enter valid month name: if don't want to filter by month then enter 'all' ")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        day = input("What day of a week you like to filter the data by? \n Enter the day: monday, tuesday, ... sunday) \n Enter 'all' to include all days of a week for the analysis:  ")
        day = day.lower()
        if day not in ('all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'):
            print(" enter valid day of a week name: if don't want to filter by month then enter 'all' ")
            continue
        else:
            break

    print()
    print('-'*60)

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable

    if month != 'all':
    # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

    # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time & End Time column to datetime

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # display the most common month

    common_month = df['month'].mode()[0]
    print('Most common month: ', common_month)
    print()

    # display the most common day of week

    common_day = df['day_of_week'].mode()[0]
    print('Most common day of week: ', common_day)
    print()

    # display the most common start hour

    common_start_hr = df['hour'].mode()[0]
    print('Most common start hour: ', common_start_hr)
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    common_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station: ', common_start_station)
    print()

    # display most commonly used end station

    common_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station: ', common_end_station)
    print()

    # display most frequent combination of start station and end station trip

    df['str_end'] = df['Start Station'].astype(str)+' to '+df['End Station']
    str_end_pop = df['str_end'].mode()[0]
    print('Most Popular common start n stops: ', str_end_pop)
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    df['tot_travel_t'] = df['End Time'] - df['Start Time']
    df['total_trav_sec'] = df['tot_travel_t'].dt.total_seconds()
    total_time_sec = df['total_trav_sec'].sum()
    total_time = str(datetime.timedelta(seconds=total_time_sec))
    print('Total travel time is: ', total_time)
    print()

    # display mean travel time

    print('Mean travel time is: ', df['tot_travel_t'].mean())
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    count_user_type = df['User Type'].value_counts(dropna = True)
    print('counts of user types are: \n', count_user_type)
    print()

    # Display counts of gender
    try:
        count_gender = df['Gender'].value_counts(dropna = True)
        print('Counts of user types are: \n', count_gender)
        print()
    except KeyError:
        print('No Gender information available for the Washington bikeshare data')
        print()

    # Display earliest, most recent, and most common year of birth

    try:
        yob_earliest = df['Birth Year'].min()
        yob_recent = df['Birth Year'].max()
        yob_common = df['Birth Year'].mode()
        print("The earlist year of birth is {} \n Most recent year of birth is {} \n Most common year of birth {}".format(int(yob_earliest), int(yob_recent), int(yob_common)))
    except KeyError:
        print("No information on users' birth year available from the Washington bikeshare data")

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

        rawdata_view = input('\nWould you like to see the first 5 lines of raw data? Enter yes or no.\n')
        if rawdata_view.lower() == 'yes':
            print(df.head())
            print()
        else:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break

if __name__ == "__main__":
	main()
