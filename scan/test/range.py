import numpy as np
import fnmatch
import os


def a_range(x, axis=0):
    return np.max(x, axis=axis) - np.min(x, axis=axis)

# ********************************************************************************************************************

for file in os.listdir('.'):
    if fnmatch.fnmatch(file, '*.npy'):
        print(file)
x = np.load(file)
print(file, a_range(x, 1))