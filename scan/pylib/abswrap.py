# Under development, will be taking shots for calibration
import cv2
import numpy as np
import time


def arc_tan4(a,b,c,d):
    return


def ave_energy(a, b, c, d):
    average = .25*(a + b + c + d)
    return average


def abs_wrap1(folder, numpy_file, png_file, preamble, offset):
    mask = np.zeros((480, 640), dtype=np.bool)
    process = np.zeros((480, 640), dtype=np.bool)
    c_range = np.zeros((480, 640), dtype=np.float)
    depth = np.zeros((480, 640), dtype=np.float)

    noise_threshold = 0.1

    image_cnt = 4  # Number of images to be taken
    im0 = np.zeros((640, 480), dtype=np.float)
    im1 = np.zeros((640, 480), dtype=np.float)
    im2 = np.zeros((640, 480), dtype=np.float)
    im3 = np.zeros((640, 480), dtype=np.float)

    a_sum = np.zeros((480, 640), dtype=np.float)

    im_arr = [im0, im1, im2, im3]
    for i in range(image_cnt):
        my_file = folder + preamble + str(offset+i+1) + ".png"
        print(my_file)
        image = cv2.imread(my_file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        im_arr[i] = gray
    wrap = np.zeros((480, 640), dtype=np.float)
    im_wrap= np.zeros((480, 640), dtype=np.float)
    for i in range(480):
        for j in range(640):
            phi_sum = float(int(im_arr[0][i, j]) + int(im_arr[1][i, j]) + int(im_arr[2][i, j] + int(im_arr[3][i, j])))
            phi_max = float(max(im_arr[0][i, j], im_arr[1][i, j], im_arr[2][i, j], im_arr[3][i, j]))
            phi_min = float(min(im_arr[0][i, j], im_arr[1][i, j], im_arr[2][i, j], im_arr[2][i, j]))
            phi_range = float(phi_max - phi_min)
            if phi_sum == 0:
                phi_sum = 1
            noise = float(phi_range / phi_sum)
            mask[i, j] = (noise < noise_threshold)
            process[i, j] = not(mask[i, j])
            c_range[i, j] = phi_range
            if process[i, j]:
                a_sum[i, j] = ave_energy(im_arr[0][i, j], im_arr[1][i, j], im_arr[2][i, j], im_arr[3][i, j])
                wrap[i, j] = np.arctan2(1.0 * (1.0*im_arr[3][i, j]-1.0*im_arr[1][i, j]), (1.0*im_arr[0][i, j] - 1.0*im_arr[2][i, j]))
                if wrap[i, j] < 0:
                    wrap[i, j] += 2*np.pi
                im_wrap[i, j] = 128/np.pi * wrap[i, j]
            else:
                wrap[i, j] = 0
                im_wrap[i, j] = 0
    file_path = folder + '/' + numpy_file
    np.save(file_path, wrap, allow_pickle=False)
    file_path = folder + '/mask.npy'
    np.save(file_path, mask, allow_pickle=False)
    file_path = folder + '/process.npy'
    np.save(file_path, process, allow_pickle=False)
    file_path = folder + '/c_range.npy'
    np.save(file_path, c_range, allow_pickle=False)
    png_file = folder + '/' + png_file
    cv2.imwrite(png_file, im_wrap)
    cv2.imwrite(folder + '/image7.png', a_sum)
    cv2.imwrite(folder + '/image8.png', a_sum)
    cv2.imwrite(folder + '/image11.png', a_sum)
    cv2.imwrite(folder + '/image12.png', a_sum)
    cv2.destroyAllWindows()
    return


def abs_wrap2(folder, numpy_file, png_file, preamble, offset):
    process = np.load(folder + '/process.npy')
    image_cnt = 4  # Number of images to be taken
    im0 = np.zeros((640, 480), dtype=np.float)
    im1 = np.zeros((640, 480), dtype=np.float)
    im2 = np.zeros((640, 480), dtype=np.float)
    im3 = np.zeros((640, 480), dtype=np.float)
    im_arr = [im0, im1, im2, im3]
    for i in range(image_cnt):
        my_file = folder + preamble + str(offset+i+1) + ".png"
        print(my_file)
        image = cv2.imread(my_file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        im_arr[i] = gray
    wrap = np.zeros((480, 640), dtype=np.float)
    im_wrap= np.zeros((480, 640), dtype=np.float)
    for i in range(480):
        for j in range(640):
            if process[i, j]:
                wrap[i, j] = np.arctan2(1.0 * (1.0*im_arr[3][i, j]-1.0*im_arr[1][i, j]), (1.0*im_arr[0][i, j] - 1.0*im_arr[2][i, j]))
                if wrap[i, j] < 0:
                    wrap[i, j] += 2*np.pi
                im_wrap[i, j] = 128/np.pi * wrap[i, j]
            else:
                wrap[i, j] = 0
                im_wrap[i, j] = 0
    file_path = folder + '/' + numpy_file
    np.save(file_path, wrap, allow_pickle=False)
    png_file = folder + '/' + png_file
    cv2.imwrite(png_file, im_wrap)
    cv2.destroyAllWindows()
    return


def abs_wrap3(folder, numpy_file, png_file, preamble, offset):
    process = np.load(folder + '/process.npy')
    image_cnt = 4  # Number of images to be taken
    im0 = np.zeros((640, 480), dtype=np.float)
    im1 = np.zeros((640, 480), dtype=np.float)
    im2 = np.zeros((640, 480), dtype=np.float)
    im3 = np.zeros((640, 480), dtype=np.float)
    im_arr = [im0, im1, im2, im3]
    for i in range(image_cnt):
        my_file = folder + preamble + str(offset+i+1) + ".png"
        print(my_file)
        image = cv2.imread(my_file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        im_arr[i] = gray
    wrap = np.zeros((480, 640), dtype=np.float)
    im_wrap= np.zeros((480, 640), dtype=np.float)
    for i in range(480):
        for j in range(640):
            if process[i, j]:
                wrap[i, j] = np.arctan2(1.0 * (1.0*im_arr[3][i, j]-1.0*im_arr[1][i, j]), (1.0*im_arr[0][i, j] - 1.0*im_arr[2][i, j]))
                if wrap[i, j] < 0:
                    wrap[i, j] += 2*np.pi
                im_wrap[i, j] = 128/np.pi * wrap[i, j]
            else:
                wrap[i, j] = 0
                im_wrap[i, j] = 0
    file_path = folder + '/' + numpy_file
    np.save(file_path, wrap, allow_pickle=False)
    png_file = folder + '/' + png_file
    cv2.imwrite(png_file, im_wrap)
    cv2.destroyAllWindows()
    return
