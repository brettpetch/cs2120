import numpy as np
from sklearn import datasets


def train_test_split(data, labels, n, test_proportion):
    """
    :param data: Returns iris dataset (150 records)
    :param labels: returns iris labels (4 columns wide)
    :param n: number of splits
    :param test_proportion: test proportion (0-1)
    :return: touple (train_data, train_labels, test_data, test_labels)

    train_data = []
    train_labels = []
    test = round(len(data) * test_proportion)
    train = round(len(data) * (1 - test_proportion))
    for data_set in range(int(train)):
        for x in range(n):
            train_labels.append(labels[x])
            train_data.append(data[data_set][x])
    test_data = []
    test_labels = []
    for data_set in range(int(test)):
        for x in range(n):
            test_data.append(labels[x])
            test_labels.append(data[data_set][x])

    return (train_data, train_labels, test_data, test_labels)
"""
    train_data = [] #[label1, 2, 3, 4] <=n  0
                    # data 1            1
                    # data 2            2
    length = int(len(data) * test_proportion) # always a whole number
                                        # assume 1/3 of 150 = 50
    dict = {}
    train_labels = []
    for x in range(length):
        temp = [] # store the restricted categories for each data index
        temp_labels = []
        while(1):
            toAdd = np.random.randint(len(data))
            check = dict.get(toAdd)
            if check==None:
                for y in range(n):
                    temp.append(data[toAdd][y])
                    temp_labels.append(labels[y])
                dict[toAdd] = temp
                train_data.append(temp)
                train_labels.append(temp_labels)
                break

    # want 51 -150
    test_data = []
    test_labels = []
    for x in range(len(data)-(length-1)):
        temp = []  # store the restricted categories for each data index
        temp_labels = []
        while (1):
            toAdd = np.random.randint(len(data))
            check = dict.get(toAdd)
            if check == None:
                for y in range(n):
                    temp.append(data[toAdd][y])
                    temp_labels.append(labels[y])
                dict[toAdd] = temp
                test_data.append(temp)
                test_labels.append(temp_labels)
                break

    return (train_data, train_labels, test_data, test_labels)



iris = datasets.load_iris()
data = iris.data
labels = iris.feature_names
train_test_split(data, labels, 3, 0.45)
