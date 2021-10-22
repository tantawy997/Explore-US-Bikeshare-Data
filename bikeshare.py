import time
import pandas as pd
import numpy as np


CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).

    while True:
        cities = ['chicago', 'new york city', 'washington']
        city = input(
            "\n Which city would you like to fliter by? (chicago, new york city, washington) \n").lower().strip()
        if city in cities:
            break
        else:
            print("\n input is invalid")

        # get user input for month (january, february, ... , june or all)

    while True:
        months = ['january', 'february', 'march',
                  'april', 'june', 'may', 'all']
        month = input(
            "\n Which month would you like to fliter by? (january, february, march, april, may, june)? Type 'all' for no month filter\n").lower().strip()
        if month in months:
            break
        else:
            print("\n Please enter a valid month name")

    # get user input for day of week (monday, tuesday, ... sunday or all)

    while True:
        days = ['monday', 'tuesday', 'wednesday', 'thursday',
                'friday', 'saturday', 'sunday', 'all']
        day = input("\n Which day would you like to filter by from week days ? (monday, tuesday, wednesday, thursday, friday, saturday, sunday)? Type 'all' for no day filter \n").lower().strip()
        if day in days:
            break
        else:
            print("\n Please enter a valid day name")

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        pop_month = df['month'].mode()[0]
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        pop_month = months[pop_month-1]
        print("The most Popular month is", pop_month)

    # display the most common day of week
    if day == 'all':
        pop_day = df['day_of_week'].mode()[0]
        print("The most Popular day is", pop_day)

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Hour'] = df['Start Time'].dt.hour
    pop_hour = df['Hour'].mode()[0]
    print("The popular Start Hour is {}:00 hrs".format(pop_hour))

    print("\n This took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start_station = df['Start Station'].mode()[0]
    print("The most commonly used Start Station is {}".format(pop_start_station))

    # display most commonly used end station
    pop_end_station = df['End Station'].mode()[0]
    print("The most commonly used End Station is {}".format(pop_end_station))

    # display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station']+" "+"to"+" " + df['End Station']
    pop_com = df['combination'].mode()[0]
    print("The most frequent combination of Start and End Station is {} ".format(pop_com))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    print("The total trip duration: {} hour(s) {} minute(s) {} second(s)".format(
        hour, minute, second))

    # display mean travel time
    average_duration = round(df['Trip Duration'].mean())
    m, sec = divmod(average_duration, 60)
    if m > 60:
        h, m = divmod(m, 60)
        print("The total trip duration: {} hour(s) {} minute(s) {} second(s)".format(
            h, m, sec))
    else:
        print("The total trip duration: {} minute(s) {} second(s)".format(m, sec))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print("The user types are:\n", user_counts)

    # Display counts of gender
    if city.title() == 'Chicago' or city.title() == 'New York City':
        gender_counts = df['Gender'].value_counts()
        print("\nThe counts of each gender are:\n", gender_counts)

    # Display earliest, most recent, and most common year of birth
        earliest = int(df['Birth Year'].min())
        print("\nThe oldest user is born of the year", earliest)
        most_recent = int(df['Birth Year'].max())
        print("The youngest user is born of the year", most_recent)
        common = int(df['Birth Year'].mode()[0])
        print("Most users are born of the year", common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):

    while True:
        choice = input(
            "Would you like to view individual trip data (5 entries)? Type 'yes' or 'no'\n").lower().strip()
        if choice == 'yes':
            print(df.sample(n=5))
            while choice == 'yes':
                print(df.sample(n=5))
                break
        elif choice == 'no':
            break
        else:
            print("Please enter a valid response")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
