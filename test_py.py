import collections
import itertools
# import matplotlib.pyplot as plt
# import numpy as np
import random
import sys
import timeit


def is_sorted(data):
    '''check whether a list is sorted
    
    Parameters
    ----------
    data : list
        list to check
        
    Returns
    -------
    bool
        True if the list is sorted, False otherwise
    '''
    for i in range(1, len(data)):
        # print(data[i])
        # print(data[i-1])
        print("----")
        if data[i- 1] > data[i]:
            return False
    return True

## test case best case scenario
# data = list(range(4))
# print(data)
# print(is_sorted(data))
# test worst case scenario
data = list(range(4))[::-1]
print(data)
print(is_sorted(data))
data2 = [4, 3, 2, 1]
print(data2)