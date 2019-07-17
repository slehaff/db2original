# Under development, will be taking shots for calibration
import cv2
import socket
import numpy as np
import time


# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# host = '192.168.0.14'
# port = 5454


def take_wrap(folder, numpy_file, png_file, preamble):
    image_cnt = 3  # Number of images to be taken
    im0 = np.zeros((450, 240))
    im1 = np.zeros((450, 240))
    im2 = np.zeros((450, 240))
    im_arr = [im0, im1, im2]
    # s.sendto(str(0),(host, port)) # Sync projector
    for i in range(image_cnt):
        my_file = folder + '/' + preamble + str(i+1) + ".png"
        print(my_file)
        image = cv2.imread(my_file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        im_arr[i] = gray
        # cv2.imshow("take", im_arr[i])
        # cv2.waitKey(0)
    wrap = np.zeros((240, 450))
    im_wrap= np.zeros((240, 450))
    for i in range(240):
        for j in range(450):
            wrap[i, j] = np.arctan2(1.7320508 * (im_arr[0][i, j]-im_arr[2][i, j]), (2*im_arr[1][i, j]-im_arr[0][i, j]-im_arr[2][i, j]))
            im_wrap[i, j] = 256/np.pi * wrap[i, j]
    file_path = folder + '/' + numpy_file
    np.save(file_path, wrap, allow_pickle=False)
    png_file = folder + '/' + png_file
    cv2.imwrite(png_file, im_wrap)
    cv2.destroyAllWindows()


def take_v_wrap(folder, numpy_file, png_file, preamble):
    image_cnt = 3  # Number of images to be taken
    im0 = np.zeros((450, 240))
    im1 = np.zeros((450, 240))
    im2 = np.zeros((450, 240))
    im_arr = [im0, im1, im2]
    # s.sendto(str(0),(host, port)) # Sync projector
    for i in range(image_cnt):
        my_file = folder + '/' + preamble + str(i+1) + ".png"
        print(my_file)
        image = cv2.imread(my_file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        im_arr[i] = gray
        # cv2.imshow("take", im_arr[i])
        # cv2.waitKey(0)
    wrap = np.zeros((240, 450))
    im_wrap= np.zeros((240, 450))
    for j in range(450):
        for i in range(240):
            wrap[i, j] = np.arctan2(1.7320508 * (im_arr[0][i, j]-im_arr[2][i, j]), (2*im_arr[1][i, j]-im_arr[0][i, j]-im_arr[2][i, j]))
            im_wrap[i, j] = 256/np.pi * wrap[i, j]
    file_path = folder + '/' + numpy_file
    np.save(file_path, wrap, allow_pickle=False)
    png_file = folder + '/' + png_file
    cv2.imwrite(png_file, im_wrap)
    cv2.destroyAllWindows()


cv2.destroyAllWindows()
