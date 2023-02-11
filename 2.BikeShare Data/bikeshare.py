import time
from datetime import datetime
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
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data in one of 3 American states!')
    while True:
        try:
            city = input("Please Enter the required city from('chicago','new york city','washington') : ")
            city = city.lower()
            if (city == 'chicago') | (city == 'new york city') | (city == 'washington'):
                break
        except Exception as e:
            print("Error city name is entered , please enter the city name again : {} ".format(e))        

    while True:
        try:
            month = input("Please Enter the required month from ['january','february','march','april','may','june'] or 'all' : ")
            month = month.lower()
            if(month=='january')|(month=='february')|(month=='march')|(month=='april')|(month=='may')|(month=='june')|(month=='all'):
                break
        except Exception as e:
            print("Error month or day is entered , please enter the month name again : {} ".format(e))

   
    while True:
       try:
           day = input("Please Enter the required 'day' from week days or 'all' : ")
           day = day.lower() 
           if(day=='saturday')|(day=='sunday')|(day=='monday')|(day=='tuesday')|(day=='wednesday')|(day=='thursday')|(day=='friday')|(day=='all'):
                break
       except Exception as e:
           print("Error month or day is entered , please enter the day again : {} ".format(e))

        
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
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most Popular Start month:', popular_month)

    df['day_of_week'] = df['Start Time'].dt.weekday_name
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Start day:', popular_day)

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start station:', popular_start_station)

    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End station:', popular_end_station)


    df['Start End'] = df['Start Station'].map(str) + ' - ' + df['End Station'].map(str)
    popular_start_end = df['Start End'].mode()[0]
    print('Most Popular Start and End station:', popular_start_end)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['Start Time'] =  pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M:%S')
    df['End Time'] =  pd.to_datetime(df['End Time'], format='%Y-%m-%d %H:%M:%S')

    #Display total travel time in seconds
    total_trip_time = (df['End Time']-df['Start Time']).sum()
    print("Total trip time in (days hours:minutes:seconds) : ",total_trip_time)
    # Display mean travel time
    mean_time = (df['End Time']-df['Start Time']).mean()
    print('Mean travel time in (days hours:minutes:seconds) :',mean_time)

    
def user_stats(df):
    """Displays statistics on bikeshare users."""
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['year'] = df['Start Time'].dt.year
    user_types = df['User Type'].value_counts()
    print('user types :\n',user_types)


    if 'Gender' not in df.columns:
        print("Gender not available")
    else:
        # filling the missing data in the gender column
        df.fillna(method = 'ffill' , axis = 0)
        gender = df['Gender'].value_counts()
        print('Gender counts :\n', gender)
            

    earliest_year = df['year'].min()
    recent_year = df['year'].max()
    common_year = df['year'].mode()[0]
    print("Earliest year : ",earliest_year)
    print("Recent year : ",recent_year)
    print("Most Common year : ",common_year)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_data(df):     
    """Displays statistics of the first 5 raw data , and asking the user for more rows to display."""
    #Display the first five rows
    i = 5
    print("The fisrt 5 rows of the raw data : ",df.head(i))
    
    # Ask the user for more data rows to display
    while True:
        while True:
            try:
                data = input("Do you want to display the next 5 rows type 'yes' or 'no' :  ")
                data = data.lower()
                if (data == 'yes') | (data == 'no'):
                    break
            except Exception as e:
                print("Error choice is entered , please enter 'yes' or 'no' again : {} ".format(e))   
        if (data == 'yes'):
            i += 5
            print ("The next 5 raw data :\n",df.head(i))
        else:
            break            
            

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
