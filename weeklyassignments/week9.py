import csv
import numpy as np
from pylab import *


def week8():
    csv_reader = csv.reader(open('./sports_data.csv', 'r'))
    data = []
    for line in csv_reader:
        data.append(line)

    col_titles = data[0]
    data = data[1:]
    months = [row[0] for row in data]
    data = [row[1:] for row in data]

    data_array = np.array(data).astype(np.float).T

    nhl = data_array[0]
    mlb = data_array[1]
    nba = data_array[2]
    nfl = data_array[3]
    numpy

week8()
