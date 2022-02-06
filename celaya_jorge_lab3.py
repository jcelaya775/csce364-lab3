"""
Jorge Celaya
NCC CSCE 364; Spring 2022
Lab #3; celaya_jorge_lab3.py

Code Summary: Provides an overview summary of national and 
state covid statistics 
"""

from hashlib import new
import pandas as pd
import requests
import sys
from io import StringIO

# Displays a national summary of covid stats


def national_summary(df: pd.DataFrame):
    tot_cases = df['tot_cases'].sum()
    new_cases = df['new_case'].sum()
    tot_death = df['tot_death'].sum()
    new_death = df['new_death'].sum()

    print('\tNational Summary:\n')

    print(f'\t\tTotal Cases: {tot_cases}')
    print(f'\t\tNew Cases: {new_cases}')
    print(f'\t\tTotal Deaths: {tot_death}')
    print(f'\t\tNew Deaths: {new_death}')

    return


# Displays a state summary of covid stats
def state_summary(df: pd.DataFrame):
    state = input('Please enter a state: ')

    tot_cases = (df['state'] == state)['tot_cases'].sum()
    new_cases = (df['state'] == state)['new_case'].sum()
    tot_death = (df['state'] == state)['tot_death'].sum()
    new_death = (df['state'] == state)['new_death'].sum()

    print('State Summary:\n')

    print(f'\t\tTotal Cases: {tot_cases}')
    print(f'\t\tNew Cases: {new_cases}')
    print(f'\t\tTotal Deaths: {tot_death}')
    print(f'\t\tNew Deaths: {new_death}')

    return


# Displays the top n number of states by the summary statistics
def analysis():

    return


def main():
    req = requests.get(
        'https://data.cdc.gov/api/views/9mfq-cb36/rows.csv?accessType=DOWNLOAD')
    df = pd.read_csv(StringIO(req.text))

    state_summary(df)


main()
