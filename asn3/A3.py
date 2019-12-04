## Name: Me [100 % Version]
## Student Number:
## Partners: None
## Grade: 100
from os import walk
import os

os.environ["PROJ_LIB"] = 'C:\\ProgramData\\Anaconda3\\Library\\share'
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.basemap import Basemap
import re


def load_station_info(directory='./data/'):

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


station_data = load_station_info()


def load_temperature_data(directory='./data/'):

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

    td = temperature_dict
    sdd = station_info_dict
    ids_to_remove = []
    for sid in temperature_dict:
        if sdd[sid]['begin_year'] > start_year or sdd[sid]['end_year'] < end_year:
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
    fig.savefig(plot_title + ".png")


def sort_dictionary_by_absolute_value_ascending(dictionary):


    return sorted(dictionary.items(), key=lambda x: abs(x[1]))


def sort_dictionary_by_absolute_value_descending(dictionary):


    return sorted(dictionary.items(), key=lambda x: abs(x[1]), reverse=True)


def compute_average_temp(temperatures):

    return np.mean(temperatures)


def compute_average_change(temperatures):

    # This is a list that holds temperatures to be averaged
    avg_list = []
    # A counter variable
    i = 0
    # This for loop will iterate over every temperature in the list.
    # The if statement will ensure that the for loop doesn't exceed the length of the list of temperatures
    for temp in temperatures:
        if i + 1 < len(temperatures):
            # This will obtain the difference between the first two temperature values
            avg = temperatures[i + 1] - temperatures[i]
            # This will append the difference to the list initialized earlier
            avg_list.append(avg)
        i += 1
    # Returns the average of the differences of the temperature values
    return np.mean(avg_list)


def compute_average_changes_dict(station_info_dict,
                                 temperature_data_dict,
                                 start_year,
                                 end_year):

    # Create an empty dictionary to hold average changes
    average_changes_dict = {}
    # Iterate through each station by using data dict keys
    for station_key in temperature_data_dict.keys():
        # make list to hold data from inner loop
        sub_average_list = []
        # Loop through years to collect data
        for year in list(range(start_year, end_year)):
            # Compute average temp from each station
            sub_average = compute_average_temp(temperature_data_dict[station_key][year])
            # Append to list
            sub_average_list.append(sub_average)
        # Append to dictionary
        average_changes_dict[station_key] = compute_average_change(sub_average_list)
        # return completed dictionary
    return average_changes_dict


def compute_top_average_change_dict(average_changes_dict, n):

    # Create dictionary to hold top values
    top_avg_changes_dict = {}
    # Sort values by descending
    sorted_avg_changes = sort_dictionary_by_absolute_value_descending(average_changes_dict)
    # Iterate through from the range of n
    for i in range(n):
        # re-append sorted values and keys
        top_avg_changes_dict[sorted_avg_changes[i][0]] = sorted_avg_changes[i][1]
    # return top n values with their station keys
    return top_avg_changes_dict


def make_average_change_dict_for_map(station_info_dict, average_change_dict):

    # Initialize dictionary for storage of map values
    average_change_dict_for_map = {}
    # Iterate over dictionary keys, then assign value station name to a lat, long and value from avg. change dict.
    for x in average_change_dict.keys():
        average_change_dict_for_map[station_info_dict[x]['station_name']] = (station_info_dict[x]['lat'],
                                                                             station_info_dict[x]['lon'],
                                                                             average_change_dict[x])
    return average_change_dict_for_map


def draw_top_average_changes_map(top_average_changes_dict_for_map,
                                 start_year,
                                 end_year,
                                 num_top_values):

    draw_map(("Top {} Average Changes Between {} and {}").format(num_top_values, start_year, end_year - 1),
             top_average_changes_dict_for_map)


def draw_maps_by_range(station_info_dict,
                       valid_temperature_data_dict,
                       start_year,
                       years_per_map,
                       num_top_values,
                       num_maps):

    # call(st,map,1950, 10, 5, 3)
    # 1950-1959
    # 1960-1969
    # 1970-1970

    for i in range(num_maps):
        end_year = start_year + years_per_map  # 1950 - 1959, 1960 - 1969
        avg = compute_average_changes_dict(station_info_dict, valid_temperature_data_dict, start_year, end_year)
        topavg = compute_top_average_change_dict(avg, num_top_values)  # top five for 1950-1959 stored as dict
        # (station id: temp change)
        # add long, lat, avg temp
        passing_dict = make_average_change_dict_for_map(station_info_dict, topavg)
        # draw_top_average_changes_map()
        draw_top_average_changes_map(passing_dict, start_year, end_year, num_top_values)
        start_year = end_year  # 1960 as start year


### Example to test your finished program. Uncomment to run. ###
#
# # Nested dict of station details.
station_data = load_station_info()
#
# # Nested dict of temperature data.
temperature_data = load_temperature_data()
#
# # Range of years to consider
start_year = 1980
end_year = 2000
#
# # Extract the valid data for this range of years
temperature_data = make_valid_temperature_data_dict(station_data,
                                                    temperature_data,
                                                    start_year,
                                                    end_year)

# # Draw multiple temperature change maps. This call should result in two maps being drawn:
# # one for years 1950 to 1959, and the other from 1960 to 1969.
start_year = 1980
years_per_map = 10
num_top_values = 5
num_maps = 2

draw_maps_by_range(station_data,
                   temperature_data,
                   start_year,
                   years_per_map,
                   num_top_values,
                   num_maps)
