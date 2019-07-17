# This version uses flood fill for unwrapping, it isn't working properly

import cv2
import numpy as np


class UnwrapPath(object):
    def __init__(self, x, y, phi, q):
        self.x = x
        self.y = y
        self.phi = phi
        self.q = q


class Stack:
    # Constructor creates a list
    def __init__(self):
        self.stack = list()

    # Adding elements to stack
    def push(self, data):
        # Checking to avoid duplicate entries
        # if data not in self.stack:
        self.stack.append(data)
        return True

    # Removing last element from the stack
    def pop(self):
        if len(self.stack) <= 0:
            return ("Stack Empty!")
        return self.stack.pop()

    # Getting the size of the stack
    def size(self):
        return len(self.stack)

width = 430
height = 230
start_x = round(width/2)
start_y = round(height/2)
unwrap_stack = Stack()


def cc_unwrap(folder, file, x, y, phi, q, p):
    file1 = folder + file
    unwrap_data = np.load(file1)
    file_path = folder + file[:-4] + '_process.npy'
    print('path:', file_path)
    process = np.load(file_path)
    # file_path = folder + '/' + file[:-4] + '_quality.npy'
    # quality = np.load(file_path)
    quality = np.zeros((480, 640), dtype=np.float)
    if p:
        fraction = phi-round(phi)
        difference = unwrap_data[x, y] - fraction
        q += quality[x, y]
        if difference > 0.5:
            difference -= 1
        if difference < -0.5:
            difference += 1
        u = UnwrapPath(x, y, phi+difference, q)
        unwrap_stack.push(u)


def unwrap_r(low_f, high_f, folder):
    file1 = folder + '/' + high_f
    wrap_data = np.load(file1)
    file_path = folder + '/' + high_f[:-4] + '_mask.npy'
    mask = np.load(file_path)
    file_path = folder + '/' + high_f[:-4] + '_process.npy'
    process = np.load(file_path)
    file_path = folder + '/' + high_f[:-4] + '_c_range.npy'
    c_range = np.load(file_path)
    unwrap_data = wrap_data
    phi = unwrap_data[start_x, start_y]
    path = UnwrapPath(x=start_x, y=start_y, phi=phi, q=0)
    unwrap_stack.push(path)
    while unwrap_stack.size() > 0:
        current = unwrap_stack.pop()
        if process[current.x, current.y]:
            unwrap_data[current.x, current.y] = current.phi
            process[current.x, current.y] = False
            if current.y > 0:
                cc_unwrap(folder, high_f, current.x, current.y-1, current.phi, current.q, process[current.x, current.y])
            if current.y < (height-1):
                cc_unwrap(folder, high_f, current.x, current.y + 1, current.phi, current.q, process[current.x, current.y])
            if current.x > 0:
                cc_unwrap(folder, high_f, current.x - 1, current.y, current.phi, current.q, process[current.x, current.y])
            if current.x < width-1:
                cc_unwrap(folder, high_f, current.x + 1, current.y, current.phi, current.q, process[current.x, current.y])
    unwrap_data = np.multiply(unwrap_data, 125.0)
    # unwrapdata = np.unwrap(np.transpose(unwrapdata))
    # unwrapdata = cv2.GaussianBlur(unwrapdata,(0,0),3,3)
    cv2.imwrite(folder + 'c_unwrap.png', unwrap_data)




