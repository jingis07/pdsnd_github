import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_slicers():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "None" to apply no month filter
        (str) day - name of the day of week to filter by, or "None" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    while True:
        cities = ['chicago', 'new york city', 'washington']
        city = input(
            "\n Which city would you like to analyze? Input either Chicago, New york city, or Washington) \n").lower()
        if city in cities:
            break
        else:
            print("\n Invalid input, Please enter a valid city name")

    # get user input for month (january, february, ... , june or none)
    while True:
        months = ['January', 'February', 'March',
                  'April', 'June', 'May', 'None']
        month = input(
            "\n Which month would you like to filter by? Input either January, February, March, April, May, or June. Type 'None' for no month filter \n").title()
        if month in months:
            break
        else:
            print("\n Invalid input, Please enter a valid month")

    # get user input for day of week (monday, tuesday, ... sunday or none)
    while True:
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                'Friday', 'Saturday', 'Sunday', 'None']
        day = input("\n Which day of the week would you like to filter by? Input either Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday. Type 'None' for no day filter \n").title()
        if day in days:
            break
        else:
            print("\n Invalid input, Please enter a valid day")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "None" to apply no month filter
        (str) day - name of the day of week to filter by, or "None" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    if month != 'None':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month)+1
        df = df[df['month'] == month]
    if day != 'None':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    mcm(df, month)

    # display the most common day of week
    if day == 'None':
        pop_day = df['day_of_week'].mode()[0]
        print("The most Popular day is", pop_day)

    # display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    pop_hour = df['Start Hour'].mode()[0]
    print("The popular Start Hour is {}:00 hrs".format(pop_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def mcm(df, month):
    if month == 'None':
        pop_month = df['month'].mode()[0]
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        pop_month = months[pop_month-1]
        print("The most Popular month is", pop_month)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display the most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The most commonly used Start Station is {}".format(common_start_station))

    # display the most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most commonly used End Station is {}".format(common_end_station))

    # display the most frequent combination of start station and end station trip
    df['combination'] = df['Start Station']+" "+"to"+" " + df['End Station']
    comb_start_end = df['combination'].mode()[0]
    print("The most frequent combination of Start and End Station is {} ".format(
        comb_start_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    minute, second = divmod(total_time, 60)
    hour, minute = divmod(minute, 60)
    print("The total trip duration: {} hour(s) {} minute(s) {} second(s)".format(
        hour, minute, second))

    # display mean travel time
    average_time = round(df['Trip Duration'].mean())
    m, sec = divmod(average_time, 60)
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
        oldest = int(df['Birth Year'].min())
        print("\nThe oldest user was born in the year", oldest)
        youngest = int(df['Birth Year'].max())
        print("The youngest user was born in the year", youngest)
        common_birthyear = int(df['Birth Year'].mode()[0])
        print("Most users were born in the year", common_birthyear)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):

    while True:
        response = ['yes', 'no']
        choice = input(
            "Would you like to view 5 lines of raw data? Type 'yes' or 'no'\n").lower()
        if choice in response:
            if choice == 'yes':
                start = 0
                end = 5
                data = df.iloc[start:end, :9]
                print(data)
            break
        else:
            print("Invalid input, Please enter a valid response")
    if choice == 'yes':
        while True:
            choice_2 = input(
                "Would you like to view more raw data? Type 'yes' or 'no'\n").lower()
            if choice_2 in response:
                if choice_2 == 'yes':
                    start += 5
                    end += 5
                    data = df.iloc[start:end, :9]
                    print(data)
                else:
                    break
            else:
                print("Invalid input, Please enter a valid response")


def main():
    while True:
        city, month, day = get_slicers()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\n Would you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
