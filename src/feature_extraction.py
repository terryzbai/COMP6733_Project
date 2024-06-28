import numpy as np

'''
Input:
    @window_length  integer
    @magnitudes     array with size of (window_length, num_dimension)
Output: 
'''
def ACEnergy(window_length, magnitudes):
    return (1 / (window_length / 2)) * np.sum(magnitudes ** 2)