## CS 2120 Assignment #1
## Name: Mark Cam
## Student number: 251027741


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
            r = re.sub(r'[^a-zA-Z0-9.,-]+', '', r)
            s = r.split(',')
            s = [str(x) for x in s]
            records.append(s)

    return records


records = load_a1_data()


# HINT: creating a function to convert numbers to month names might help!
def number_to_month(num):
    if num == 1:
        return "January"
    if num == 2:
        return "February"
    if num == 3:
        return "March"
    if num == 4:
        return "April"
    if num == 5:
        return "May"
    if num == 6:
        return "June"
    if num == 7:
        return "July"
    if num == 8:
        return "August"
    if num == 9:
        return "September"
    if num == 10:
        return "October"
    if num == 11:
        return "November"
    if num == 12:
        return "December"


def coldest_month(records):
    """
    Function to find which month was the coldest on record.

    :returns: A string indicating the month, year, and extreme cold temperature
    of the coldest month on record.
    """

    # HINT: You should probably initialize some kind of variables here. 
    # Maybe to hold the current coldest month (and year!) and temperature.
    # INSERT YOUR CODE HERE!

    coldest_y = None  # variable to hold current coldest year
    coldest_m = None  # variable to hold current coldest month
    coldest_t = 100  # variable to hold current coldest temperature

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

        if temp < coldest_t:
            coldest_t = temp
            coldest_m = month
            coldest_y = year

    # RETURN a string indicating the month, year, and coldest temperature. 
    # e.g. "January 2015 was the coldest month on record with an extreme 
    # minimum temperature of -3 degrees."

    return number_to_month(
        coldest_m), coldest_y, 'was the coldest month on record with an extreme minimum temperature of', coldest_t, \
           'degrees. '


# Test your function.
print(coldest_month(records))


def warmest_month(records):
    """
    Function to find which month was the coldest on record.

    :returns: A string indicating the month, year, and extreme hot temperature 
    of the hottest month on record.
    """

    # HINT: You should probably initialize some kind of variables here. Maybe 
    # to hold the current coldest month (and year!) and temperature.

    # INSERT YOUR CODE HERE!

    warmest_year_so_far = None  # Variable to hold warmest year so far
    warmest_month_so_far = None  # Variable to hold warmest month so far
    warmest_temp_so_far = 0  # Variable to hold warmest temp so far

    # This is an instruction to Python: Do the body (the indented code) 
    # following `for` statement, for _every_ record in our list of temperature 
    # data.
    # This is a LOOP. It's already written for you... you just have to fill in 
    # the body
    for record in records:

        # INSERT YOUR CODE HERE! (remove 'pass' when you add your code.)
        year_warmest = int(record[0])
        month_warmest = int(record[1])
        temp_warmest = float(record[3])

        if temp_warmest > warmest_temp_so_far:
            warmest_temp_so_far = temp_warmest
            warmest_month_so_far = month_warmest
            warmest_year_so_far = year_warmest

    # RETURN a string indicating the month, year, and warmest temperature.
    # e.g. "July 2004 was the hottest month on record with an extreme 
    # maximum temperature of 38 degrees."

    coldestmonth_string = number_to_month(
        warmest_month_so_far), warmest_year_so_far, 'was the hottest month on record with an ' \
                                                    'extreme maximum temperature of', warmest_temp_so_far, 'degrees.'

    return coldestmonth_string


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

    month_count = 0  # Holds the number of months counted
    mean_temp = 0  # Holds the average mean temperature for the entire year

    # A loop to get you started.
    # HINT: Remember there is more than one way the records for a year could 
    # be incomplete.

    for record in records:

        # INSERT YOUR CODE HERE! (remove 'pass' when you add your code.)
        year_m = int(record[0])
        temp = float(record[2])
        month = int(record[1])

        if year_m == year:
            if not math.isnan(year_m):  # If this returns a NaN, the function will not move to the next statement
                if not math.isnan(month):
                    if not math.isnan(temp):
                        month_count += 1  # For each record add 1 to the month count
                        # For each record add the mean temperature for that month to the variable 'mean_temp'
                        mean_temp += temp
                        if month_count == 12:
                            mean_temp = mean_temp / 12

    if month_count == 12:
        return 'The mean annual temperature in', year, 'was', mean_temp, 'degrees.'
    # This condition is set up to cover all NaN scenarios. If NaN was ever returned for a year, month,
    # or mean temp, we would never reach a count of 12 months, therefore it will print the below statement.
    if month_count != 12:
        return 'Mean annual temperature data is unavailable for this year.'

    # Print a formatted string with the mean annual temperature or a message
    # saying that the temperature data is unavailable for that year.


# Test your function.
print(print_mean_annual_temperature(2011, records))
print(print_mean_annual_temperature(1992, records))

### BONUS - No marks, just for the curious/ambitious. Write a function that
### takes 'records' and produces a plot of the mean temperature over all years 
### in the data. You should be able to do this using simple functions from 
### matplotlib - just search for it online!
