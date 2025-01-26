import time
import pandas as pd
import numpy as np
from os import system, name
##edit python file
def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

clear()

def get_filters():
    print("Hello! Let's explore some US bikeshare data!")

    city_selection_list = ['1', '2', '3', 'chicago', 'new york city', 'washington']
    while True:
        city_selection = input(
            "\nWould you like to see data for:\n\n\t[1] Chicago\n\t[2] New York City\n\t[3] Washington\n\n[Type the city number or the city name]\n> ").strip().lower()
        
        if city_selection in city_selection_list:
            if city_selection == '1' or city_selection == 'chicago':
                city = 'chicago'
                break
            elif city_selection == '2' or city_selection == 'new york city':
                city = 'new york city'
                break
            elif city_selection == '3' or city_selection == 'washington':
                city = 'washington'
                break
        else:
            print(f"'{city_selection}' is not a valid input. Please try again.\n")

    time_filter_selection_list = ['1', '2', '3', '4', 'month', 'day', 'both', 'none']
    while True:
        time_filter = input(
            f"\n\nWould you like to filter {city.title()}'s data by:\n\n\t[1] Month\n\t[2] Day\n\t[3] Both\n\t[4] None\n\n[Type the filter number or the filter name.]\n> ").strip().lower()

        if time_filter in time_filter_selection_list:
            break
        else:
            print(f"'{time_filter}' is not a valid input. Please try again.\n")

    months = ['january', 'february', 'march', 'april', 'may', 'june']
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    if time_filter == '4' or time_filter == 'none':
        print(f"\nFiltering {city.title()}'s data for the whole 6 months.\n\n")
        month = 'all'
        day = 'all'

    elif time_filter == '3' or time_filter == 'both':
        while True:
            month = input("\nWhich month? [January, February, March, April, May, June]\n> ").strip().lower()
            if month in months:
                break
            else:
                print(f"'{month}' is not a valid month name. Please try again.")
        while True:
            day = input("\nWhich day? [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]\n> ").strip().lower()
            if day in days:
                break
            else:
                print(f"'{day}' is not a valid day name. Please try again.")

    elif time_filter == '1' or time_filter == 'month':
        while True:
            month = input("\nWhich month? [January, February, March, April, May, June]\n> ").strip().lower()
            if month in months:
                day = 'all'
                break
            else:
                print(f"'{month}' is not a valid month name. Please try again.")

    elif time_filter == '2' or time_filter == 'day':
        while True:
            day = input("\nWhich day? [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]\n> ").strip().lower()
            if day in days:
                month = 'all'
                break
            else:
                print(f"'{day}' is not a valid day name. Please try again.")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month_name().str.lower()
    df['Day'] = df['Start Time'].dt.day_name().str.lower()

    if month != 'all':
        df = df[df['Month'] == month]
    if day != 'all':
        df = df[df['Day'] == day]

    return df

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if 'Month' in df:
        popular_month = df['Month'].mode()[0]
        print(f"Most Popular Start Month: {popular_month}")
    if 'Day' in df:
        popular_day = df['Day'].mode()[0]
        print(f"Most Popular Start Day: {popular_day}")

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print(f"Most Popular Start Hour: {popular_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start_station = df['Start Station'].mode()[0]
    popular_end_station = df['End Station'].mode()[0]
    most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()

    print(f"Most Common Start Station: {popular_start_station}")
    print(f"Most Common End Station: {popular_end_station}")
    print(f"Most Common Trip: {most_common_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_duration = df['Trip Duration'].sum()
    average_duration = df['Trip Duration'].mean()

    print(f"Total Duration: {total_duration} seconds")
    print(f"Average Duration: {average_duration} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print(f"User Types:\n{df['User Type'].value_counts()}")
    
    if 'Gender' in df:
        print(f"Gender Distribution:\n{df['Gender'].value_counts()}")

    if 'Birth Year' in df:
        print(f"Earliest Birth Year: {int(df['Birth Year'].min())}")
        print(f"Most Recent Birth Year: {int(df['Birth Year'].max())}")
        print(f"Most Common Birth Year: {int(df['Birth Year'].mode()[0])}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    row_index = 0
    while True:
        display_data = input("Would you like to see 5 rows of raw data? Enter yes or no: ").lower()
        if display_data == 'yes':
            print(df.iloc[row_index:row_index + 5])
            row_index += 5
            if row_index >= len(df):
                print("No more data to display.")
                break
        elif display_data == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes':
            clear()
            break

if _name_ == "_main_":
    clear()
    main()