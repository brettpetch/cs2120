## Name:
## Student Number:
## Partners:

from os import walk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.basemap import Basemap
import re


def load_station_info(directory='./data/'):
    """
    Loads information about each weather station and stores it in a nested 
    dictionary.
    
    :param directory: Directory (folder) containing the station information 
    file.
    
    :return: A nested dictionary STATION ID -> dict of STATION INFO
    """
    with open(directory + 'Temperature_Stations.csv', 'r') as temp_station_file:
        temp_station_lines = temp_station_file.readlines()[4:]
        temp_station_dict = dict()
        for line in temp_station_lines:
            line = re.sub(r'[^a-zA-Z0-9.,-]+', '', line)
            line = line.split(',')
            line = [str(x) for x in line]
            prov = line[0]
            station_name = line[1]
            station_id = line[2]
            begin_year = int(line[3])
            begin_month = int(line[4])
            end_year = int(line[5])
            end_month = int(line[6])
            lat = float(line[7])
            lon = float(line[8])
            elev = int(line[9])
            joined = line[10]
    
            temp_station_dict[station_id] = {'prov': prov, 
                                             'station_name': station_name, 
                                             'station_id': station_id,
                                             'begin_year': begin_year, 
                                             'begin_month': begin_month, 
                                             'end_year': end_year,
                                             'end_month': end_month,
                                             'lat': lat, 
                                             'lon': lon, 
                                             'elev': elev, 
                                             'joined': joined}

    return temp_station_dict


def load_temperature_data(directory='./data/'):
    """
    Loads temperature data from all files into a nested dict with station_id as
    top level keys. Data for each station is then stored as a dict: 
                  YEAR -> list of monthly mean temperatures.
    NOTE: Missing data is not handled gracefully - it is simply ignored.
    
    :param directory: Directory containing the temperature data files.
    
    :return: A nested dictionary STATION ID -> YEAR -> LIST OF TEMPERATURES
    """
    all_stations_temp_dict = dict()
    for _, _, files in walk(directory):
        for file_name in files:
            if file_name.startswith('mm'):
                station_temp_dict = dict()
                file = open(directory + file_name, 'r')
                station_id = file.readline().strip().split(',')[0]
                file.seek(0)
                file_lines = file.readlines()[4:]
                for line in file_lines:
                    line = re.sub(r'[^a-zA-Z0-9.,-]+', '', line)
                    line = line.strip().split(',')
                    year = int(line[0])
                    monthly_temperatures = []
                    for i in range(1, 24, 2):
                        value = float(line[i])
                        if value > -100:
                            monthly_temperatures.append(value)
                    station_temp_dict[year] = monthly_temperatures
                all_stations_temp_dict[station_id] = station_temp_dict
    return all_stations_temp_dict


def make_valid_temperature_data_dict(station_info_dict,
                                     temperature_dict,
                                     start_year,
                                     end_year):
    """
    Processes the input temperature data dictionary to remove data from 
    stations that do not have valid data over the period from the input start 
    year to the input end year. This routine will change the input temperature
    dictionary.
    
    :param station_info_dict: Dictionary mapping 
     STATION ID -> dict of STATION INFO
    :param temperature_data_dict: Dictionary mapping 
     STATION ID -> YEAR -> LIST OF TEMPERATURES
    :param start_year: starting year of the valid data to retain.
    :param end_year: ending year of the valid data to retain.
    
    :return: A reduced temperature data dictionary containing data only from 
     stations with valid data over the indicated range of years and only the 
     temperature data over that same range of years.
    """
    td = temperature_dict
    sdd = station_info_dict
    ids_to_remove = []
    for sid in temperature_dict:        
        if sdd[sid]['begin_year']>start_year or sdd[sid]['end_year']<end_year:
            ids_to_remove.append(sid)
            continue        
        is_valid = True        
        years_to_remove = []
        for year in td[sid]:            
            if year < start_year or year > end_year:                
                years_to_remove.append(year)                
            elif len(td[sid][year]) != 12:
                is_valid = False
                break                
        if not is_valid:
            ids_to_remove.append(sid)
        else:
            for year in years_to_remove:
                td[sid].pop(year)    
    for idn in ids_to_remove:
        td.pop(idn)    
    return temperature_dict

def draw_map(plot_title, data_dict):
    """
    Draws a map of North America with temperature station names and values. 
    Positive values are drawn next to red dots and negative values next to 
    blue dots. The location of values are determined by the latitude and 
    longitude. A dictionary (data_dict) is used to provide a map from 
    station_name names to a tuple containing the (latitude, longitude, value)
    used for drawing.
    
    :param plot_title: Title for the plot.
    :param data_dict: A dictionary mapping 
     STATION NAME -> tuple(LATITUDE, LONGITUDE, VALUE)
    """
    fig = plt.figure(figsize=(9, 9), dpi=100)
    map1 = Basemap(projection='ortho', resolution=None, lat_0=53, lon_0=-97, )
    map1.etopo(scale=0.5, alpha=0.5)

    for station_name_name in data_dict:
        data = data_dict[station_name_name]
        print(station_name_name, data)
        x, y = map1(data[1], data[0])
        value = data[2]
        color = 'black'
        if value < 0:
            color = 'blue'
        elif value > 0:
            color = 'red'
        plt.plot(x, y, 'ok', markersize=3, color=color)
        plt.text(x, y, '{}\n {:.2f}°C'.format(station_name_name, value), fontsize=8)
    plt.title(plot_title)
    plt.show()
    fig.savefig(plot_title+".png")

def sort_dictionary_by_absolute_value_ascending(dictionary):
    """
    Sort a dictionary so that the items appear in ascending order according 
    to the values.
    
    :param dictionary: A dictionary.
    
    :return: A sorted list of tupes of key-value pairs
    """
    
    return sorted(dictionary.items(), key=lambda x:abs(x[1]))

def sort_dictionary_by_absolute_value_descending(dictionary):
    """
    Sort a dictionary so that the items appear in descending order according 
    to the values.
    
    :param dictionary: A dictionary.
    
    :return: A sorted list of tupes of key-value pairs
    """
    
    return sorted(dictionary.items(), key=lambda x:abs(x[1]), reverse=True)

"""
Your code starts here! Implement each function, one at a time, testing them 
along the way. There are lots of parameters in this assignment - so make sure 
you're using them correctly. The first function, for example, can be tested as 
follows:

 station_data = load_station_info()
 temperature_data = load_temperature_data()
 start_year = 1950
 end_year = 2000
 temperature_data = make_valid_temperature_data_dict(station_data,
                                                     temperature_data,
                                                     start_year,
                                                     end_year)
 temperatures = temperature_data['2204101'][1989]
 mean_temp = compute_average_temp(temperatures)

Test each function along the way using a similar strategy.

"""

def compute_average_temp(temperatures):
    """
    Compute the average of a list of temperatures.
    
    :param temperatures: A list of temperature values.
    
    :return: Their average.
    """
    

def compute_average_change(temperatures):
    """
    Compute the average CHANGE over a list of temperatures. For example, if 
    temperatures is [0, 1, 2, 3, 4], this function should return 1.0. If 
    annual_temperatures is [2, 1.5, 1, 0.5, 0], this function should return 
    -0.5
    
    :param temperatures: A list of temperature values.
    
    :return: The average change of these values.
    """
    

def compute_average_changes_dict(station_info_dict,
                                 temperature_data_dict,
                                 start_year,
                                 end_year):
    """
    Create a dictionary mapping STATION IDS to the AVERAGE TEMP CHANGE over the
    range from start_year (inclusive) to end_year (exclusive).

    Here you are asked to create and fill a dictionary. The keys of this 
    dictionary will be the same as the keys of the temperature data dictionary.
    The values will be float values of the average change in the annual 
    mean temperature over the time period from the start year to the end year.
    This requires, for each station, first computing all of the annual mean 
    temperatures over the time period and then computing the average change in 
    these annual means.
    
    Assume that the temperature_data_dict contains only valid data over a 
    period at least as long as the range from start_year to end_year. Stated 
    otherwise, assume that temperature_data_dict is the result of a call to 
    make_valid_temperature_data_dict over a time period that includes 
    start_year to end_year.
    
    :param station_info_dict: Dictionary mapping 
     STATION ID -> dict of STATION INFO
    :param temperature_data_dict: Dictionary mapping 
     STATION ID -> YEAR -> LIST OF TEMPERATURES
    :param start_year: The first year to take into account (inclusive)
    :param end_year: The last year to take into account (exclusive)
    
    :return: A dictionary mapping STATION ID -> AVERAGE TEMP CHANGE
    """
    

def compute_top_average_change_dict(average_changes_dict,n):
    """
    Create a reduced dictionary that maps STATION IDS to the AVERAGE TEMP 
    CHANGES that contains only the top n AVERAGE TEMP CHANGES (in absolute 
    value).

    Here you are asked to remove items from an existing dictionary, all of 
    the items except for the top n items in terms of AVERAGE TEMP CHANGE (in 
    absolute value). So you take in a dictionary that maps STATION IDs to 
    AVERAGE TEMP CHANGES and remove the appropriate items from it.
    
    :param average_changes_dict: Dictionary mapping 
     STATION ID -> AVERAGE TEMP CHANGE
    :param n: The number of changes to include in the output dictionary.
    
    :return: For convenience, a reference to the reduced input dictionary 
     containing the items in the input with the n largest (in absolute value) 
     temperature changes.
    """  
    

def make_average_change_dict_for_map(station_info_dict, average_change_dict):
    """
    Create a dictionary mapping STATION NAMES to 
    tuples(LATITUDE, LONGITUDE, AVERAGE TEMP CHANGE).

    Here again you are asked to create and fill a dictionary. This time, it
    needs to have the right keys and values so that it can be passed to the 
    draw_map function. As is indicated in the return comment below, this 
    dictionary needs to map station names (strings) to a tuple that includes 
    the latitude, longitude, and average temperature change.

    HINT: The average temperature changes can be generated by calling the 
    compute_average_changes_dict function (and possibly reducing it by calling 
    the compute_top_average_change_dict function), which returns a dictionary.
    What are its keys and values?

    :param station_info_dict: Dictionary mapping 
     STATION ID -> dict of STATION INFO
    :param average_changes_dict: Dictionary mapping 
     STATION ID -> AVERAGE TEMP CHANGE
    
    :return: A dictionary mapping 
     STATION NAME -> (LATITUDE, LONGITUDE, AVERAGE TEMP CHANGE)
    """
    

def draw_top_average_changes_map(top_average_changes_dict_for_map,
                                 start_year,
                                 end_year,
                                 num_top_values):
    """
    Given the a dictionary mapping station names to mapping data, together with
    a start_year (inclusive) and end_year (exclusive) and the number of top
    average changes computed, draw a map with this data by calling the draw_map
    function. In addition to the mapping data dictionary, you also need a plot 
    title to call this function, so make a string that uses start_year,
    end_year and num_top_values to create an  appropriate title, e.g 
    'Top 10 Average Annual Temperature Changes Between 1990 and 1999.'
    
    :param top_average_changes_dict_for_map: A dictionary mapping 
     STATION NAME -> (LATITUDE, LONGITUDE, AVERAGE TEMP CHANGE)
     containing the num_top_values largest (in absolute value) changes in 
     temperature over the analysis period.
    :param start_year: Start year, as integer, inclusive, for years in 
     analysis.
    :param end_year: End year, as integer, exclusive, for years in 
     analysis.
    :param num_top_values: The number of largest average annual temperature
     changes.
    
    :return: No return statement.
    """
    

def draw_maps_by_range(station_info_dict, 
                       valid_temperature_data_dict, 
                       start_year, 
                       years_per_map, 
                       num_top_values,
                       num_maps):
    """
    Given the station data dictionary, a dictionary of valid temperature 
    data over the years to be plotted, a start_year (inclusive, 
    integer), the number of years_per_map (integer), the num_top_values to 
    compute, and the num_maps (integer), draw num_maps maps, each 
    showing the top num_top_values average changes in temperature over 
    years_per_map. For example, calling draw_maps_by_range(station_info, 
    valid_temperature_data, 1950, 10, 5, 2) will draw two maps, one with the 
    top five temp changes from 1950 to 1959, and the other with the top five 
    temp changes from 1960 to 1969.

    HINT: You can use a loop here to draw the maps!

    :param station_info_dict: Dictionary mapping 
     STATION ID -> dict of STATION INFO
    :param valid_temperature_data_dict: Dictionary mapping 
     STATION NAME -> YEAR -> LIST OF TEMPERATURES
     containing valid temperature data over the period from start_year to 
     end_year.
    :param start_year: Start year, as integer, inclusive, for years in 
     analysis.
    :param end_year: End year, as integer, exclusive, for years in analysis.
    :param num_top_values: The number of largest average annual temperature
     changes.
    :param num_maps: The number of maps to draw.
        
    :return: No return statement.
    """
    
### Example to test your finished program. Uncomment to run. ###
#
# # Nested dict of station details.
#station_data = load_station_info()
#
# # Nested dict of temperature data.
#temperature_data = load_temperature_data()
#
# # Range of years to consider
#start_year = 1980
#end_year = 2000
#
# # Extract the valid data for this range of years
#temperature_data = make_valid_temperature_data_dict(station_data,
#                                                    temperature_data,
#                                                    start_year,
#                                                    end_year)
#
# # Draw multiple temperature change maps. This call should result in two maps being drawn:
# # one for years 1950 to 1959, and the other from 1960 to 1969.
#start_year = 1980
#years_per_map = 10
#num_top_values = 5
#num_maps = 2
#draw_maps_by_range(station_data, 
#                   temperature_data,
#                   start_year,
#                   years_per_map,
#                   num_top_values,
#                   num_maps)
