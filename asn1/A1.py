## CS 2120 Assignment #1
## Name: Brett Petch
## Student number: 251038051


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

def numtodate(m):
    month = ["January", "Feb", "March", "April", "May", "June", "July", "August", "September", "October", "November",
             "December"]
    return month[m - 1]


def coldest_month(records):
    """
    Function to find which month was the coldest on record.

    :returns: A string indicating the month, year, and mean temperature of the 
    coldest month on record.
    """

    # HINT: You should probably initialize some kind of variables here. 
    # Maybe to hold the current coldest month (and year!) and temperature.
    # INSERT YOUR CODE HERE!

    coldest_month_so_far = None
    coldest_year = None
    coldest_temp = 100

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
        temp = float(record[4])

        if temp < coldest_temp:
            coldest_temp = temp
            coldest_year = year
            coldest_month_so_far = month

    # RETURN a string indicating the month, year, and coldest temperature. 
    # e.g. "January 2015 was the coldest month on record with an extreme 
    # minimum temperature of -3 degrees."
    coldest_month_so_far = str(numtodate(coldest_month_so_far))
    print(coldest_month_so_far, coldest_year, "was the coldest month on record with a temperature of", coldest_temp,
          "degrees!")


# Test your function.

def warmest_month(records):
    """
    Function to find which month was the coldest on record.

    :returns: A string indicating the month, year, and mean temperature of the 
    hottest month on record.
    """

    # HINT: You should probably initialize some kind of variables here. Maybe 
    # to hold the current coldest month (and year!) and temperature.

    # INSERT YOUR CODE HERE!

    warmest_year_so_far = None
    warmest_month_so_far = None
    warmest_temp_so_far = -100

    # This is an instruction to Python: Do the body (the indented code) 
    # following `for` statement, for _every_ record in our list of temperature 
    # data.
    # This is a LOOP. It's already written for you... you just have to fill in 
    # the body
    for record in records:

        # INSERT YOUR CODE HERE! (remove 'pass' when you add your code.)
        year = int(record[0])
        month = int(record[1])
        temp = float(record[4])

        if temp > warmest_temp_so_far:
            warmest_temp_so_far = temp
            warmest_year_so_far = year
            warmest_month_so_far = month

            warmest_month_so_far = numtodate(warmest_month_so_far)

    # RETURN a string indicating the month, year, and warmest temperature.
    # e.g. "July 2004 was the hottest month on record with an extreme 
    # maximum temperature of 38 degrees."
    return "{} {} was the coldest month on record with an extreme minimum temperature of {} degrees.".format(
        str(warmest_month_so_far), str(warmest_year_so_far), str(warmest_temp_so_far))


# Test your function.

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

    mean = []
    # A loop to get you started.
    # HINT: Remember there is more than one way the records for a year could 
    # be incomplete.

    for record in records:

        # INSERT YOUR CODE HERE! (remove 'pass' when you add your code.)
        allyears = int(record[0])
        month = int(record[1])
        temp = float(record[4])
        if year == allyears:
            mean.append(temp)
    if month_count == 0:
        print("Temperature data is unavailable for that year.")
    else:
        for month_count in range(mean):
            sum = sum + float(record[month_count])
    return sum / month_count
    # Print a formatted string with the mean annual temperature or a message
    # saying that the temperature data is unavailable for that year.

# Test your function.

### BONUS - No marks, just for the curious/ambitious. Write a function that 
### takes 'records' and produces a plot of the mean temperature over all years 
### in the data. You should be able to do this using simple functions from 
### matplotlib - just search for it online!
