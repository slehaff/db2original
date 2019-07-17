import numpy as np
import cv2
import math as m


def a_range(x, axis=0):
    return np.max(x, axis=axis) - np.min(x, axis=axis)


def unwrap_r(phi_min, high_f, folder):
    file1 = folder + '/' + phi_min
    file2 = folder + '/' + high_f
    unw_min_data = np.load(file1)  # To be continued
    wrap2data = np.load(file2)
    unwrap_data = np.zeros((480, 640), dtype=np.float)
    kdata = np.zeros((480, 640), dtype=np.float)
    phi_diff = np.zeros((480, 640), dtype=np.float)
    depth = np.zeros((480, 640), dtype=np.float)
    for i in range(480):
        for j in range(640):
            kdata[i, j] = m.ceil((1.0 * unw_min_data[i, j] - 1.0 * wrap2data[i, j])/(2.0*np.pi))
            unwrap_data[i, j] = 1.0 * wrap2data[i, j] + 2.0*kdata[i, j]*np.pi
            phi_diff[i, j] = unwrap_data[i, j] - unw_min_data[i, j]
    wr_save = folder + 'unwrap.npy'
    np.save(wr_save, unwrap_data, allow_pickle=False)
    # unwrap_data = np.multiply(unwrap_data, 1.0)
    cv2.imwrite(folder + 'unwrap.png', unwrap_data)
    cv2.imwrite(folder + 'phi_diff.png', phi_diff)
