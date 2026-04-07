#libs imports
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
        (str) city  - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day   - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # city inpt
    while True:
        city = input('\nHey there so choose a city you would like to explore? '
                     '(chicago, new york city, washington)\n').strip().lower()
        if city in CITY_DATA:
            break
        print('  You sure its not a typo, Kindly Enter from chicago, new york city, or washington.')

    # month inpt
    while True:
        month = input('\nWhich month would you like to filter by? '
                      '(all, january, february, march, april, may, june)\n').strip().lower()
        if month in MONTHS:
            break
        print('  Wrong input . Kindly Enter a month between january–june, or "all".')

    # day inpt
    while True:
        day = input('\nWhich day of the week would you like to filter by? '
                    '(all, monday, tuesday, wednesday, thursday, friday, saturday, sunday)\n').strip().lower()
        if day in DAYS:
            break
        print('  This input is not valid, Kindly enter a valid day name, or "all".')

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city  - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day   - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # time start
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month']      = df['Start Time'].dt.month     
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour']       = df['Start Time'].dt.hour
    # month filter
    if month != 'all':
        df = df[df['month'] == MONTHS.index(month)] 
    # filter for day
    if day != 'all':
        df = df[df['day_of_week'] == day]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # Most common month
    common_month = df['month'].mode()[0]
    print(f'  Most Common Month is     : {MONTHS[common_month].title()}')
    # Most common day of week
    common_day = df['day_of_week'].mode()[0]
    print(f'  Most Common Day is      : {common_day.title()}')
    # Most common start hour
    common_hour = df['hour'].mode()[0]
    print(f'  Most Common Start Hour : {common_hour}:00')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # Most common start station in db
    common_start = df['Start Station'].mode()[0]
    print(f'  Most Common Start Station :{common_start}')
    # Most common end station in db
    common_end = df['End Station'].mode()[0]
    print(f'  Most Common End Station : {common_end}')
    # Most frequent combination present
    df['trip'] = df['Start Station'] + '  -->  ' + df['End Station']
    common_trip = df['trip'].mode()[0]
    print(f'  Most Common Trip :{common_trip}')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total_seconds = df['Trip Duration'].sum()
    mean_seconds  = df['Trip Duration'].mean()
    # Formatting total as hours / minutes / seconds
    total_h = int(total_seconds // 3600)
    total_m = int((total_seconds % 3600) // 60)
    total_s = int(total_seconds % 60)
    mean_m = int(mean_seconds // 60)
    mean_s = int(mean_seconds % 60)
    print(f'  Total Travel Time : {total_h}h {total_m}m {total_s}s')
    print(f'  Mean Travel Time  : {mean_m}m {mean_s}s')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Counts of user types
    print('  User Type Counts:')
    print(df['User Type'].value_counts().to_string(header=False))
    # Gender except washington
    if 'Gender' in df.columns:
        print('\n  Gender Counts:')
        print(df['Gender'].value_counts().to_string(header=False))
    else:
        print('\n  Gender data not available for this city.')

    # birth year stats except for washington
    if 'Birth Year' in df.columns:
        earliest   = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])
        print(f'\n  Earliest Birth Year   : {earliest}')
        print(f'  Most Recent Birth Year: {most_recent}')
        print(f'  Most Common Birth Year: {most_common}')
    else:
        print('\n  Apologoies Birth year data not available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def display_raw_data(df):
    #Asks the user if they want to see 10 rows of raw data at a time
    indix = 0
    while True:
        show = input('\nWanna see 10 more rows of raw data? Enter yes or no.\n').strip().lower()
        if show != 'yes':
            break
        print(df.iloc[indix: indix + 10].to_string())
        indix += 10
        if indix >= len(df):
            print('\n  Thats the endddd.')
            break

MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
DAYS   = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
#main loop
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()