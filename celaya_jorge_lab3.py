"""
Jorge Celaya
NCC CSCE 364; Spring 2022
Lab #3; celaya_jorge_lab3.py

Code Summary: Provides an overview summary of national and
state covid statistics
"""

import pandas as pd
import requests
import sys
from io import StringIO

from sqlalchemy import column


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
    state = input('Please enter a state (2-Letter State Code): ')

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
    n = input('Please enter a number for the top number of states: ')

    try:
        n = int(n)
    except ValueError:
        print('That input was invalid.')
        return False

    tot_cases = df.groupby(
        'state')['tot_cases'].sum().sort_values(ascending=False)
    new_cases = df.groupby(
        'state')['new_case'].sum().sort_values(ascending=False)
    tot_death = df.groupby(
        'state')['tot_death'].sum().sort_values(ascending=False)
    new_death = df.groupby(
        'state')['new_death'].sum().sort_values(ascending=False)

    print(f'\n\Here are the top {n} states for the following stats:')

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
def write_to_file(df: pd.DataFrame) -> bool:
    # create new columns
    df['7-Day Moving Avg'] = 0
    df['Historic Cases'] = 0

    df = df[['state', 'submission_date', 'new_case', '7-Day Moving Avg', 'Historic Cases']
            ].sort_values(by='submission_date')

    # Rename some columns
    df.rename(columns={'state': 'State', 'submission_date': 'Date',
              'new_case': 'New Cases'}, inplace=True)

    # Compute 7-day avg and historic cases
    # 7-day avg is calculated by averaging the previous 7 days
    # and rounding to the nearest whole number
    df['7-Day Moving Avg'] = df.apply(lambda row: round(df['New Cases']
                                      [row.name:row.name+7].mean()), axis=1)

    print(df)

    # Format Date column
    df['Date'] = df['Date'].apply(lambda date: date.dt.strftime('%b'))

    # df.to_csv('output.csv')

    return


def main():
    req = requests.get(
        'https://data.cdc.gov/api/views/9mfq-cb36/rows.csv?accessType=DOWNLOAD')
    df = pd.read_csv(StringIO(req.text))

    write_to_file(df)


main()
