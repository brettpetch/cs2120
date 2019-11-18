import csv
import numpy as np
from pylab import *


def week8(n, filename='sports_data.csv'):
    file = open(filename, 'r')
    reader = csv.reader(file)
    data = []

    for row in reader:
        data.append(row)
    months = {}
    for row in data[1:]:
        date = row[0][0:3]
        data = int(row[n])

        if date in months.keys():
            months[date].append(data)
        else:
            months[date] = []
            months[date].append(data)

    monthly_averages = {}
    for date in months.keys():
        monthly_averages[date] = np.mean(months[date])

    font = {'family': 'normal', 'weight': 'normal', 'size': 14}
    rc('font', **font)
    figure(figsize=(10, 7), dpi=120)
    matplotlib.pyplot.title(('Mean Search Volume for NFL by Month: 2004 to Present'))
    plt.xlabel('Month')
    plt.ylabel('Search Volume')
    matplotlib.pyplot.bar(monthly_averages.keys(), monthly_averages.values())
    matplotlib.pyplot.savefig('figure_'+str(n)+'.png')


week8(1)
week8(2)
week8(3)
week8(4)
