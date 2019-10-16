## Brett Petch
## October 10, 2019

import numpy as np


def make_list_of_lists(n, m):
    lol = np.random.randint(1, 10, size=(n, m)).tolist()
    return lol


def deep_copy_list_of_lists(listname):
    deepcopy = []
    for x in range(0, len(listname), 1):
        anothercopy = []
        for y in range(0, len(listname[x]), 1):
            anothercopy.append(listname[x][y])
        deepcopy.append(anothercopy)
    return deepcopy


a = list(make_list_of_lists(3, 5))
ab = deep_copy_list_of_lists(a)
ab[0][0] = 'a'
ab[1][1] = 'a'
ab[2][2] = 'a'
print(a)
print(ab)

b = make_list_of_lists(3, 5)
bb = deep_copy_list_of_lists(b)
bb[0][0] = 'a'
bb[1][1] = 'a'
bb[2][2] = 'a'
print(b)
print(bb)

c = make_list_of_lists(3, 5)
cb = deep_copy_list_of_lists(c)
cb[0][0] = 'a'
cb[1][1] = 'a'
cb[2][2] = 'a'
print(c)
print(cb)

"""

:output: 

a = [[6, 7, 6, 5, 6], [1, 4, 2, 7, 9], [8, 3, 9, 1, 2]]
copy of a (ab) = [['a', 7, 6, 5, 6], [1, 'a', 2, 7, 9], [8, 3, 'a', 1, 2]]

b =[[5, 3, 5, 8, 5], [5, 2, 2, 6, 9], [8, 8, 5, 9, 1]]
copy of b (bb) = [['a', 3, 5, 8, 5], [5, 'a', 2, 6, 9], [8, 8, 'a', 9, 1]]

c = [[6, 1, 8, 1, 3], [7, 8, 9, 4, 1], [6, 1, 7, 2, 1]]
copy of c (cb) = [['a', 1, 8, 1, 3], [7, 'a', 9, 4, 1], [6, 1, 'a', 2, 1]]

"""
