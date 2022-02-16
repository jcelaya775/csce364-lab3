'''
Jorge Celaya
NCC CSCE 364; Spring 2022
Lab  # 3; celaya_jorge_lab3.py

Code Summary: Provides an overview summary of national and
state covid statistics
'''

import pandas as pd
import requests
import sys
from os.path import exists
from io import StringIO
from sqlalchemy import column
from datetime import date, timezone
import datetime


'''
TODO: Include Documentation on how you will make decisions about missing data
'''

# Displays a national summary of covid stats


def national_summary(df: pd.DataFrame) -> None:
    # get national stats
    tot_cases = df['tot_cases'].sum()
    new_cases = df['new_case'].sum()
    tot_death = df['tot_death'].sum()
    new_death = df['new_death'].sum()

    print('\t\tNational Summary:\n')

    print(f'\t\tTotal Cases: {tot_cases}')
    print(f'\t\tNew Cases: {new_cases}')
    print(f'\t\tTotal Deaths: {tot_death}')
    print(f'\t\tNew Deaths: {new_death}')

    return


# Displays a state summary of covid stats
def state_summary(df: pd.DataFrame) -> bool:
    state = input('\tPlease enter a state (2-Letter State Code): ')

    # get state data
    try:
        df = df.loc[df['state'] == state]
    except:
        print('That input was invalid.')
        return False

    # get state stats
    tot_cases = df['tot_cases'].sum()
    new_cases = df['new_case'].sum()
    tot_death = df['tot_death'].sum()
    new_death = df['new_death'].sum()

    print('\n\tState Summary:\n')

    print(f'\t\tTotal Cases: {tot_cases}')
    print(f'\t\tNew Cases: {new_cases}')
    print(f'\t\tTotal Deaths: {tot_death}')
    print(f'\t\tNew Deaths: {new_death}')

    return True


# Displays the top n number of states by the summary statistics
def analysis(df: pd.DataFrame) -> bool:
    n = input('\tPlease enter a number for the top number of states: ')

    try:
        n = int(n)
    except ValueError:
        print('That input was invalid.')
        return False

    states = df.groupby('state')

    tot_cases = states['tot_cases'].sum().sort_values(ascending=False)
    new_cases = states['new_case'].sum().sort_values(ascending=False)
    tot_death = states['tot_death'].sum().sort_values(ascending=False)
    new_death = states['new_death'].sum().sort_values(ascending=False)

    print(f'\n\tHere are the top {n} states for the following stats:')

    print('\n\tTotal Cases:')
    print(tot_cases.head(n))

    print('\n\tNew Cases:')
    print(new_cases.head(n))

    print('\n\tTotal Deaths:')
    print(tot_death.head(n))

    print('\n\tNew Deaths:')
    print(new_death.head(n))

    return True


# Processes and outputs data to create a Covid data file
def output_data(df: pd.DataFrame) -> bool:
    print('\tWriting data to \'output.csv\'...')
    # create new columns
    df['7-Day Moving Avg'] = 0
    df['Historic Cases'] = 0

    df = df[['state', 'submission_date', 'new_case', '7-Day Moving Avg', 'Historic Cases']
            ].sort_values(by='submission_date')

    # Rename some columns
    df.rename(columns={'state': 'State', 'submission_date': 'Date',
              'new_case': 'New Cases'}, inplace=True)

    # 7-day avg is calculated by averaging the previous 7 days
    # and rounding to the nearest whole number
    df['7-Day Moving Avg'] = df.apply(lambda row: round(df['New Cases']
                                      [row.name:row.name+7].mean()), axis=1)

    # Historic cases is calculated by...

    # Format Date column
    df['Date'] = pd.to_datetime(df['Date']).apply(
        lambda date: date.strftime('%b %d %Y'))

    # write title and date generated rows
    with open('output.csv', 'w') as outfile:
        today = date.today()
        timezone = datetime.datetime.utcnow().astimezone().tzinfo
        outfile.write('Data Table for Daily Case Trends - The United States\n')
        outfile.write("Date generated: " + today.strftime('%a %b %d %Y %X '))
        outfile.write('(' + str(timezone) + ')\n')

    # Format output
    df.style.format('%20s')

    df.to_csv('output.csv', index=False, mode='a')

    print('\tFinished.')

    return


def user_options():
    print('\nPlease choose from one of the following.\n')
    print('\t1.) Display a national summary.')
    print('\t2.) Diplay a state summary.')
    print('\t3.) Display an analysis of the top states for a given statistic.')
    print('\t4.) Output the data into a csv file.\n')

    option = input('Please enter which function to run. (enter number): ')

    return option


def main():
    print('Retrieving data...\n')
    req = requests.get(
        'https://data.cdc.gov/api/views/9mfq-cb36/rows.csv?accessType=DOWNLOAD')
    df = pd.read_csv(StringIO(req.text))

    print('Hello, and welcome to lab 3!\n')
    ans = input('Would you like to run a function? (yes/no): ')

    while(ans.lower() == 'yes' or ans.lower() == 'y'):
        option = user_options()
        print()

        if (option.lower() == 'exit' or option.lower() == 'quit'):
            break

        try:
            option = int(option)
        except ValueError:
            print('\nThat was not a valid option. Please try again.')

        if option == 1:
            national_summary(df)
        elif option == 2:
            state_summary(df)
        elif option == 3:
            analysis(df)
        elif option == 4:
            output_data(df)

        ans = input('\nWould you like to to run another function? (yes/no): ')

    print('\nThank you!')


main()
