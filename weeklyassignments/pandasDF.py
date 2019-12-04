import numpy as np
import pandas as pd
from sklearn import datasets


def train_test_split(data, labels, n, test_proportion):
    """
    :param data: Returns iris dataset (150 records)
    :param labels: returns iris labels (4 columns wide)
    :param n: number of splits
    :param test_proportion: test proportion (0-1)
    :return: touple (train_data, train_labels, test_data, test_labels)
    """
    data_df = pd.DataFrame(data)
    data_df.columns = [labels]
    split = np.random.rand(len(data_df)) < test_proportion
    tmp = data_df[split]
    train_data = tmp.values.tolist()
    train_labels = list(tmp.columns)
    tmp_columns = data_df[~split]
    test_data = data_df[~split].values.tolist()
    test_labels = list(tmp_columns.columns)

    return (train_data, train_labels, test_data, test_labels)


iris = datasets.load_iris()
data = iris.data
labels = iris.feature_names
print(train_test_split(data, labels, 3, .45)