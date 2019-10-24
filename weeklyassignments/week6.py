# Name: Brett Petch
# Date: October 16, 2019

import numpy as np


def vector_mean_fast(a):
    """
    :param a - receives an array from numpy
    :returns result_array, an array containing the averages of each row inputted to the function.
    """
    result_array = np.array([])
    for i, b in enumerate(a):
        result_array = np.append(result_array, np.mean(a[i]))
    return result_array


outarr = np.random.randint(9, size=(5, 7))
print(vector_mean_fast(outarr))
print(outarr)


def vector_mean_ans(a):
    result_array = np.array([])
    for i in range(a.shape[0]):
        result_array = np.append(result_array, np.mean(a[i]))
    return result_array


print(vector_mean_ans(outarr))


"""
Test Result: 
[4.42857143 3.85714286 3.28571429 4.14285714 4.71428571]
"""
