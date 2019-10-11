## Brett Petch
## October 10, 2019

import numpy as np


def make_list_of_lists(n, m):
    lol = np.random.randint(9, size=(n, m)).tolist()
    return lol


def deep_copy_list_of_lists(listname):
    deeplist = []
    for x in listname:
        deeplist.append(x)
    return deeplist


def modifylist(listname):
    for x in listname:
        list = make_list_of_lists(3, 5)
        return list


a = make_list_of_lists(3, 5)
print(a)
ab = deep_copy_list_of_lists(a)
print(modifylist(a))
print(ab)

b = make_list_of_lists(3, 5)
print(b)
bb = deep_copy_list_of_lists(b)
print(modifylist(b))
print(bb)

c = make_list_of_lists(3, 5)
print(c)
cb = deep_copy_list_of_lists(c)
print(modifylist(c))
print(cb)

""" 
:output: 

a = [[1, 1, 7, 5, 4], [4, 5, 5, 3, 1], [7, 2, 8, 8, 7]]
change a to = [[3, 0, 0, 2, 5], [3, 4, 3, 7, 2], [2, 6, 8, 3, 4]]
ab = [[1, 1, 7, 5, 4], [4, 5, 5, 3, 1], [7, 2, 8, 8, 7]]

b = [[1, 5, 5, 1, 5], [1, 1, 3, 4, 1], [4, 0, 1, 7, 6]]
change b to = [[1, 0, 3, 5, 6], [8, 2, 6, 2, 0], [4, 1, 2, 0, 5]]
bb = [[1, 5, 5, 1, 5], [1, 1, 3, 4, 1], [4, 0, 1, 7, 6]]

c  = [[3, 0, 4, 5, 3], [4, 4, 2, 5, 0], [4, 3, 6, 5, 1]]
change c to = [[8, 2, 6, 2, 8], [2, 5, 4, 6, 6], [3, 1, 7, 0, 1]]
cc = [[3, 0, 4, 5, 3], [4, 4, 2, 5, 0], [4, 3, 6, 5, 1]]
"""
