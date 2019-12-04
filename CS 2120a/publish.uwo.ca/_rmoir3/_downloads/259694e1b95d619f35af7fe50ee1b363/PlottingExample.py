import csv
import matplotlib.pyplot as plt
import numpy as np
from pylab import *

csv_reader = csv.reader(open('./sports_data.csv', 'r'))
data = []
for line in csv_reader:
    data.append(line)

col_titles = data[0]
data = data[1:]
months = [row[0] for row in data]
data = [row[1:] for row in data]

data_array = np.array(data).astype(np.float).T

plot(data_array[0], label='NHL')
plot(data_array[1], label='MLB')
plot(data_array[2], label='NBA')
plot(data_array[3], label='NFL')
legend()

import scipy.stats
print('NHL-MLB Correlation: {}'.format(scipy.stats.pearsonr(data_array[0],data_array[1])[0]))
print('NHL-NBA Correlation: {}'.format(scipy.stats.pearsonr(data_array[0],data_array[2])[0]))

labels = ['NHL', 'MLB', 'NBA', 'NFL']

# Set up a figure object for more placement options
fig = figure()
# Create a subfigure
ax = fig.add_subplot(111)
# Compute the correlation matrix
cor = np.corrcoef(data_array)
# Plot it
ax_mat = ax.matshow(cor)
ax_mat = ax.matshow(cor, cmap='hot')
# Set matrix labels
ax.set_xticklabels(['']+labels)
ax.set_yticklabels(['']+labels)
# Change display options
fig.colorbar(ax_mat)
# Set a title
ax.set_title('Correlation Between Professional\nSports Searches')

