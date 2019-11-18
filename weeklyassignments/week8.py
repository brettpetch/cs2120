import csv
import numpy as np
from pylab import *


def load_data(z, filename='sports_data.csv'):
    reader = csv.reader(open(filename, 'r'))
    data_list = []

    for row in reader:
        data_list.append(row)
    column_titles = data_list[0][:]

    month_info = []
    data = []
    data_list.remove(data_list[0][:])
    for item in data_list[1:]:
        month_info.append(item[0])
        data.append(item[1:])
    data = np.array(data).astype(np.float).transpose()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    searches = [0] * 12
    counter = [0] * 12
    for i, x in enumerate(data[z]):
        if month_info[i][:3] == 'Jan':
            searches[0] += data[z][i]
            counter[0] += 1
        elif month_info[i][:3] == 'Feb':
            searches[1] += data[z][i]
            counter[1] += 1
        elif month_info[i][:3] == 'Mar':
            searches[2] += data[z][i]
            counter[2] += 1
        elif month_info[i][:3] == 'Apr':
            searches[3] += data[z][i]
            counter[3] += 1
        elif month_info[i][:3] == 'May':
            searches[4] += data[z][i]
            counter[4] += 1
        elif month_info[i][:3] == 'Jun':
            searches[5] += data[z][i]
            counter[5] += 1
        elif month_info[i][:3] == 'Jul':
            searches[6] += data[z][i]
            counter[6] += 1
        elif month_info[i][:3] == 'Aug':
            searches[7] += data[z][i]
            counter[7] += 1
        elif month_info[i][:3] == 'Sep':
            searches[8] += data[z][i]
            counter[8] += 1
        elif month_info[i][:3] == 'Oct':
            searches[9] += data[z][i]
            counter[9] += 1
        elif month_info[i][:3] == 'Nov':
            searches[10] += data[z][i]
            counter[10] += 1
        elif month_info[i][:3] == 'Dec':
            searches[11] += data[z][i]
            counter[11] += 1
    mean = []
    for i, x in enumerate(searches):
        mean.append(searches[i] / counter[i])

    font = {'family': 'normal', 'weight': 'normal', 'size': 14}
    rc('font', **font)
    figure(figsize=(10, 7), dpi=120)
    matplotlib.pyplot.title(('Mean Search Volume for', column_titles[z+1], 'by Month: 2004 to Present'))
    plt.xlabel('Month')
    plt.ylabel('Search Volume')
    matplotlib.pyplot.bar(months, mean)
    matplotlib.pyplot.savefig('figure_0'+str(z+1)+'.png')


load_data(0)
load_data(1)
load_data(2)
load_data(3)
