# Name: Brett Petch
# Date: October 16, 2019

import numpy as np


def vector_mean(a):
    """
    :param a - receives an array from numpy
    :returns result_array, an array containing the averages of each row inputted to the function.
    """
    result_array = np.array([])
    for i in range(a.shape[0]):
        result_array = np.append(result_array, np.mean(a[i]))
    result_array = result_array.reshape(5, 1)
    return result_array


outarr = np.random.randint(9, size=(5, 7))
print(vector_mean(outarr))

"""
Test Result: 
[[3.14285714]
 [3.42857143]
 [2.42857143]
 [4.85714286]
 [5.14285714]]
"""
