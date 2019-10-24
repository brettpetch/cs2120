## CS 2120 Assignment #1
## Name: NAME STUDENT
## Student number: NUMBERRS


def load_a1_data(filename='London_mean_etr_max_etr_min.csv'):
    """
    This function loads the file `London_mean_etr_max_etr_min.csv` and returns 
    a LIST of temperature records... and each element of the list is ANOTHER 
    LIST that contains 5 values: 
        the year, 
        the month, 
        the mean temperature, 
        the extreme max temperature and 
        the extreme min temperature for that month.
    We'll talk about lists formally in class in a few lectures, but maybe
    you can start guessing how they work based on what you see here...
    """
    import re

    with open(filename, 'r') as file:
        records = []

        for r in file:
            r = re.sub(r'[^0-9.,-]+', '', r)
            records.append(r.split(','))

    return records


# HINT: creating a function to convert numbers to month names might help!

def month_convert(m):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']  # define months
    return months[m - 1]  # arrays start at 0, so subtract 1 from csv months


records = load_a1_data()


def coldest_month(records):
    """
    Function to find which month was the coldest on record.

    :returns: A string indicating the month, year, and mean temperature of the
    coldest month on record.
    """

    # HINT: You should probably initialize some kind of variables here.
    # Maybe to hold the current coldest month (and year!) and temperature.
    # INSERT YOUR CODE HERE!

    coldest_temp_so_far = float('+Inf')  # set to _inf to ensure that no value will be higher
    coldest_month_so_far = None  # create coldest month
    coldest_year_so_far = None  # create coldest year

    # This is an instruction to Python: Do the body (the indented code)
    # following `for` statement, for _every_ record in our list of temperature
    # data.
    # This is a LOOP. It's already written for you...you just have to fill in
    # the body
    for record in records:

        # INSERT YOUR CODE HERE!
        # Here we're extracting the information from each record and storing it
        # in variables. This is here to get you started, and should help you
        # with other parts of the assignment.

        year = int(record[0])
        month = int(record[1])
        if record[4] != '' and record[4] != 'nan':  # sterilize input
            temp = float(record[4])  # pass sterilized input to temp

        if temp < coldest_temp_so_far:
            coldest_temp_so_far = temp  # set coldest temp to temp if temp is less than temp so far var
            coldest_month_so_far = month  # set month so far variable if temp is less than temp_so_far
            coldest_year_so_far = year  # set year so far variable if temp is less than temp_so_far

    # RETURN a string indicating the month, year, and coldest temperature.
    # e.g. "January 2015 was the coldest month on record with an extreme
    # minimum temperature of -3 degrees."

    return "{} {} was the coldest month on record with an extreme minimum temperature of {} degrees.".format(
        month_convert(coldest_month_so_far), coldest_year_so_far,
        coldest_temp_so_far)  # input month name and coldest dates


# Test your function.
print(coldest_month(records))  # print function


def warmest_month(records):
    """
    Function to find which month was the coldest on record.

    :returns: A string indicating the month, year, and mean temperature of the
    hottest month on record.
    """

    # HINT: You should probably initialize some kind of variables here. Maybe
    # to hold the current coldest month (and year!) and temperature.

    # INSERT YOUR CODE HERE!

    warmest_year_so_far = None  # create warmest year
    warmest_month_so_far = None  # create warmest month
    warmest_temp_so_far = float('-inf')  # set to -inf to ensure that no value will be lower

    # This is an instruction to Python: Do the body (the indented code)
    # following `for` statement, for _every_ record in our list of temperature
    # data.
    # This is a LOOP. It's already written for you... you just have to fill in
    # the body
    for record in records:

        # INSERT YOUR CODE HERE! (remove 'pass' when you add your code.)
        year = int(record[0])
        month = int(record[1])
        if record[3] != '' and record[3] != 'nan':
            temp = float(record[3])

            if temp > warmest_temp_so_far:  # if temperature is greater than the current warmest temp, execute this:
                warmest_temp_so_far = temp  # assign warmest temp
                warmest_month_so_far = month  # assign warmest month based on temp
                warmest_year_so_far = year  # assign warmest year based on temp

    # RETURN a string indicating the month, year, and warmest temperature.
    # e.g. "July 2004 was the hottest month on record with an extreme
    # maximum temperature of 38 degrees."

    return "{} {} was the hottest month on record with an extreme maximum temperature of {} degrees.".format(
        month_convert(warmest_month_so_far), warmest_year_so_far, warmest_temp_so_far)


# Test your function.
print(warmest_month(records))


def print_mean_annual_temperature(year, records):
    """
    Given a year, print the average temperature over that year. If the records
    are incomplete for that year, the program should not crash - instead it
    should print a message saying the data is unavailable.

    :param year: Year for which mean temperature should be printed.
    :param records: A list of lists containing temperature data.
    """

    # INSERT YOUR CODE HERE!
    # Initialize variables
    import math

    month_count = 0
    mean_temp = 0

    # A loop to get you started.
    # HINT: Remember there is more than one way the records for a year could
    # be incomplete.

    for record in records:
        this_year = int(record[0])
        # INSERT YOUR CODE HERE! (remove 'pass' when you add your code.)
        if year == this_year:  # Conditional to check if this year is the same as the current year
            if record[2] != '' and record[2] != 'nan':
                avg_temp = float(record[2])
                mean_temp += avg_temp  # check mean temp
                month_count += 1  # add to month count

    if month_count != 12:
        return "Full data not available for {}.".format(year)
        # saying that the temperature data is unavailable for that year if there are not 12 months of data.
    elif month_count == 12:
        mean_temp = mean_temp / month_count
        return "Mean annual temperature of {} was {} degrees.".format(year, mean_temp)

# Test your function.


print(print_mean_annual_temperature(2019, records))  # Prints that there is no temperature data available
print(print_mean_annual_temperature(1992, records))  # Prints 1992 records


### BONUS - No marks, just for the curious/ambitious. Write a function that
### takes 'records' and produces a plot of the mean temperature over all years
### in the data. You should be able to do this using simple functions from
### matplotlib - just search for it online!


def all_temp_plot():
    import pandas as pd  # Use pandas instead to map the data easily
    import matplotlib.pyplot as plt  # Use Matplotlib PyPlot to create graph
    import numpy as np  # Use Numpy to take mean

    # Note: This will not drop years with incomplete datsets.
    # Read CSV, but only 3 columns because no one cares about the other ones
    # then group years, then take mean of months and append it to a new column in a new dataframe.
    df = pd.read_csv("London_mean_etr_max_etr_min.csv", delimiter=',', usecols=[0, 1, 2],
                     names=['Year', 'Month', 'Temperature']).groupby('Year').agg(
        Average_Temperature=pd.NamedAgg(column='Temperature', aggfunc=np.mean))
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
