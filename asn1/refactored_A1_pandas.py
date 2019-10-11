import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
        the year, 
        the month, 
        the mean temperature, 
        the extreme max temperature and 
        the extreme min temperature for that month.
'''


def load_a1_data(filename="London_mean_etr_max_etr_min.csv"):
    df = pd.read_csv(filename, delimiter=',', usecols=[0, 1, 2, 3, 4],
                     names=['Year', 'Month', 'Mean Temperature', 'Warmest Temperature', 'Coldest Temperature'])
    return df


records = load_a1_data()
print(records)


def coldest_month(records):
    df = records.sort_values(by='Coldest Temperature', ascending=True)

    df = df.iloc[0]
    print(df[['Year', 'Month', 'Coldest Temperature']])


coldest_month(records)


def warmest_month(records):
    df = records.sort_values(by='Warmest Temperature', ascending=False)
    df = df.iloc[0]
    print(df[['Year', 'Month', 'Warmest Temperature']])


warmest_month(records)


def mean_temperature(records, year):
    df = records[['Year', 'Month', 'Mean Temperature']].groupby('Year').agg(
        Average_Temperature=pd.NamedAgg(column='Mean Temperature', aggfunc=np.mean)
    )
    df = df.ix[[year]]
    print(df)


mean_temperature(records, 2019)


def all_temp_plot():
    # Read CSV, but only 3 columns because no one cares about the other ones
    # then group years, then take mean of months and append it to a new column in a new dataframe.
    df = pd.read_csv("London_mean_etr_max_etr_min.csv", delimiter=',', usecols=[0, 1, 2],
                     names=['Year', 'Month', 'Temperature']).groupby('Year').agg(
        Average_Temperature=pd.NamedAgg(column='Temperature', aggfunc=np.mean)
    )
    # reset the index to have a proper record of records
    df.reset_index(inplace=True, drop=False)
    # rename columns to a human-readable form
    df.columns = ['Year', 'Average Temperature']
    # plot the thing
    df.plot(kind='line', x='Year', y='Average Temperature',
            color='red', title='Average Annual Temperature in London, Ontario')
    # show the plot
    plt.show()


# verify this works using a function
all_temp_plot()  # plot all records
