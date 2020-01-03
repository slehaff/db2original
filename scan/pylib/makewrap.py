# Under development, will be taking shots for calibration
import cv2
import socket
import numpy as np
import time


# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# host = '192.168.0.14'
# port = 5454


def take_wrap(folder, numpy_file, png_file, preamble, offset):
    image_cnt = 3  # Number of images to be taken
    im0 = np.zeros((400, 480), dtype=np.float)
    im1 = np.zeros((400, 480), dtype=np.float)
    im2 = np.zeros((400, 480), dtype=np.float)
    im_arr = [im0, im1, im2]
    # s.sendto(str(0),(host, port)) # Sync projector
    for i in range(image_cnt):
        my_file = folder + preamble + str(offset+i+1) + ".png"
        print(my_file)
        image = cv2.imread(my_file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        im_arr[i] = gray
        # cv2.imshow("take", im_arr[i])
        # cv2.waitKey(0)
    wrap = np.zeros((480, 400), dtype=np.float)
    im_wrap= np.zeros((480, 400), dtype=np.float)
    for i in range(480):
        for j in range(400):
            wrap[i, j] = np.arctan2(1.7320508 * (1.0*im_arr[0][i, j]-1.0*im_arr[2][i, j]), (2.0*im_arr[1][i, j] - 1.0*im_arr[0][i, j] - 1.0*im_arr[2][i, j]))
            if wrap[i, j] < 0:
                wrap[i, j] += 2*np.pi
            im_wrap[i, j] = 128/np.pi * wrap[i, j]
    file_path = folder + '/' + numpy_file
    print(numpy_file, wrap[100, :])
    print(png_file, im_wrap[100, :])
    np.save(file_path, wrap, allow_pickle=False)
    png_file = folder + '/' + png_file
    cv2.imwrite(png_file, im_wrap)
    cv2.destroyAllWindows()


def take_v_wrap(folder, numpy_file, png_file, preamble, offset):
    image_cnt = 3  # Number of images to be taken
    im0 = np.zeros((400, 480), dtype=np.float)
    im1 = np.zeros((400, 480), dtype=np.float)
    im2 = np.zeros((400, 480), dtype=np.float)
    im_arr = [im0, im1, im2]
    # s.sendto(str(0),(host, port)) # Sync projector
    for i in range(image_cnt):
        my_file = folder + preamble + str(offset+i+1) + ".png"
        print(my_file)
        image = cv2.imread(my_file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        im_arr[i] = gray
        # cv2.imshow("take", im_arr[i])
        # cv2.waitKey(0)
    wrap = np.zeros((480, 400), dtype=np.float)
    im_wrap= np.zeros((480, 400), dtype=np.float)
    for j in range(400):
        for i in range(480):
            wrap[i, j] = np.arctan2(1.7320508 * (1.0*im_arr[0][i, j]-im_arr[2][i, j])/2, (im_arr[1][i, j]-.5*im_arr[0][i, j]-.5*im_arr[2][i, j]))
            if wrap[i, j] < 0:
                wrap[i, j] += 2*np.pi
            im_wrap[i, j] = 128/np.pi * wrap[i, j]
    file_path = folder + '/' + numpy_file
    np.save(file_path, wrap, allow_pickle=False)
    png_file = folder + '/' + png_file
    cv2.imwrite(png_file, im_wrap)
    cv2.destroyAllWindows()


cv2.destroyAllWindows()
