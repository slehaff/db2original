# Under development, will be takin g shots for calibration
import cv2
import numpy as np
import time
import pyntcloud


rwidth = 640
rheight = 480


def sqdist(v1, v2):
    d = v1-v2
    return 1-d*d


def compute_quality(file, folder, c_range):
    file_path = folder + '/' + file
    wrap_data = np.load(file_path)
    quality = np.zeros((rheight, rwidth), dtype=np.float)
    for i in range(rheight):
        for j in range(rwidth):
            phi = wrap_data[i, j]
            quality[i, j] = (sqdist(phi, wrap_data[i+1, j]) + sqdist(phi, wrap_data[i-1, j]) +
                             sqdist(phi, wrap_data[i, j+1]) + sqdist(phi, wrap_data[i, j-1]))/c_range[i, j]
    file_path = folder + '/' + file[:-4] + '_quality.npy'
    np.save(file_path, quality, allow_pickle=False)


def take_wrap4(folder, numpy_file, png_file, preamble, offset):
    mask = np.zeros((rheight, rwidth), dtype=np.bool)
    process = np.zeros((rheight, rwidth), dtype=np.bool)
    c_range = np.zeros((rheight, rwidth), dtype=np.float)
    depth = np.zeros((rheight, rwidth), dtype=np.float)

    noise_threshold = 0.1

    image_cnt = 4  # Number of images to be taken
    im0 = np.zeros((rwidth, rheight), dtype=np.float)
    im1 = np.zeros((rwidth, rheight), dtype=np.float)
    im2 = np.zeros((rwidth, rheight), dtype=np.float)
    im3 = np.zeros((rwidth, rheight), dtype=np.float)

    im_arr = [im0, im1, im2, im3]
    for i in range(image_cnt):
        my_file = folder + preamble + str(offset+i+1) + ".png"
        print(my_file)
        image = cv2.imread(my_file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        im_arr[i] = gray
    wrap = np.zeros((rheight, rwidth), dtype=np.float)
    im_wrap = np.zeros((rheight, rwidth), dtype=np.float)
    for i in range(rheight):
        for j in range(rwidth):
            phi_sum = float(int(im_arr[0][i, j]) + int(im_arr[1]
                                                       [i, j]) + int(im_arr[2][i, j] + int(im_arr[3][i, j])))
            phi_max = float(
                max(im_arr[0][i, j], im_arr[1][i, j], im_arr[2][i, j], int(im_arr[3][i, j])))
            phi_min = float(
                min(im_arr[0][i, j], im_arr[1][i, j], im_arr[2][i, j], int(im_arr[2][i, j])))
            phi_range = float(phi_max - phi_min)
            signal = float(phi_range / phi_sum)
            mask[i, j] = (signal < noise_threshold)
            process[i, j] = not(mask[i, j])
            c_range[i, j] = phi_range
            if process[i, j]:
                wrap[i, j] = np.arctan2(
                    1.0 * (1.0*im_arr[3][i, j]-1.0*im_arr[1][i, j]), (1.0*im_arr[0][i, j] - 1.0*im_arr[2][i, j]))
                if wrap[i, j] < 0:
                    wrap[i, j] += 2*np.pi
                im_wrap[i, j] = 128/np.pi * wrap[i, j]
            else:
                wrap[i, j] = 0
                im_wrap[i, j] = 0
    file_path = folder + '/' + numpy_file
    np.save(file_path, wrap, allow_pickle=False)
    file_path = folder + '/' + numpy_file[:-4] + '_mask.npy'
    np.save(file_path, mask, allow_pickle=False)
    file_path = folder + '/' + numpy_file[:-4] + '_process.npy'
    np.save(file_path, process, allow_pickle=False)
    file_path = folder + '/' + numpy_file[:-4] + '_c_range.npy'
    np.save(file_path, c_range, allow_pickle=False)
    png_file = folder + '/' + png_file
    cv2.imwrite(png_file, im_wrap)
    cv2.destroyAllWindows()
    print(c_range)
    print(mask)
    # compute_quality()


def get_A(im_arr):
    A = np.zeros((rwidth, rheight), dtype=np.float)
    for i in range(3):
        A = np.sum(A, im_arr[i])
    A = np.divide(A, 3)
    return A


def get_B(im_arr):
    for i in range(im_arr.length):
        B = np.multiply(im_arr[i], (np.sin(2*np.pi * i / im_arr.length)))

    return B


def get_average(array, n):
    b = np.add(array[0], array[1])
    average = 1/n * np.add(b, array[2])
    print('average size =', average.shape)
    return average


def take_wrap(folder, numpy_file, png_file, preamble, offset):
    print('wrong call !!!!!')
    mask = np.zeros((rheight, rwidth), dtype=np.bool)
    process = np.zeros((rheight, rwidth), dtype=np.bool)
    c_range = np.zeros((rheight, rwidth), dtype=np.float)
    depth = np.zeros((rheight, rwidth), dtype=np.float)

    noise_threshold = 0.1
    z_scale = 130
    z_skew = 24

    image_cnt = 3  # Number of images to be taken
    im0 = np.zeros((rwidth, rheight), dtype=np.float)
    im1 = np.zeros((rwidth, rheight), dtype=np.float)
    im2 = np.zeros((rwidth, rheight), dtype=np.float)
    nom = np.zeros((rheight, rwidth), dtype=np.float)
    denom = np.zeros((rheight, rwidth), dtype=np.float)
    im_arr = [im0, im1, im2]
    for i in range(image_cnt):
        my_file = folder + preamble + str(offset+i+1) + ".png"
        print(my_file)
        image = cv2.imread(my_file)
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        im_arr[i] = grey
    bkg_intensity = get_average(im_arr, image_cnt)
    # bkg_intensity = get_A(im_arr)
    wrap = np.zeros((rheight, rwidth), dtype=np.float)
    im_wrap = np.zeros((rheight, rwidth), dtype=np.float)
    for i in range(rheight):
        for j in range(rwidth):
            phi_sum = float(
                int(im_arr[0][i, j]) + int(im_arr[1][i, j]) + int(im_arr[2][i, j]))
            phi_max = float(
                max(im_arr[0][i, j], im_arr[1][i, j], im_arr[2][i, j]))
            phi_min = float(
                min(im_arr[0][i, j], im_arr[1][i, j], im_arr[2][i, j]))
            phi_range = float(phi_max - phi_min)
            if phi_sum == 0:
                phi_sum = .01
            noise = float(phi_range / phi_sum)
            mask[i, j] = (noise < noise_threshold)
            process[i, j] = not(mask[i, j])
            c_range[i, j] = phi_range
            if True:  # process[i, j]:
                a = (1.0*im_arr[0][i, j]-1.0*im_arr[2][i, j])
                b = (2.0*im_arr[1][i, j] - 1.0*im_arr[0]
                     [i, j] - 1.0*im_arr[2][i, j])
                nom[i, j] = a
                denom[i, j] = b
                wrap[i, j] = np.arctan2(1.7320508 * a, b)
                if wrap[i, j] < 0:
                    if a < 0:
                        wrap[i, j] += 2*np.pi
                    else:
                        wrap[i, j] += 1 * np.pi
                im_wrap[i, j] = 128/np.pi * wrap[i, j]
            else:
                wrap[i, j] = 0
                im_wrap[i, j] = 0
    wrap = cv2.GaussianBlur(wrap, (3, 3), 0)
    file_path = folder + '/' + numpy_file
    np.save(file_path, wrap, allow_pickle=False)
    file_path = folder + '/' + numpy_file[:-4] + '_mask.npy'
    np.save(file_path, mask, allow_pickle=False)
    file_path = folder + '/' + numpy_file[:-4] + '_process.npy'
    np.save(file_path, process, allow_pickle=False)
    file_path = folder + '/' + numpy_file[:-4] + '_c_range.npy'
    np.save(file_path, c_range, allow_pickle=False)
    png_file = folder + '/' + png_file
    cv2.imwrite(png_file, im_wrap)
    nom_file = folder + '/' + str(offset) + 'nom.png'
    cv2.imwrite(nom_file, nom)
    denom_file = folder + '/' + str(offset) + 'denom.png'
    cv2.imwrite(denom_file, denom)
    bkg_file = folder + '/' + str(offset) + 'bkg.png'
    cv2.imwrite(bkg_file, bkg_intensity)
    # mask_file = folder + '/' + str(offset) + 'mask.png'
    # cv2.imwrite(mask_file, mask)
    cv2.destroyAllWindows()
    print('c_range', c_range)
    print('mask', mask)
    # compute_quality()


def take_v_wrap(folder, numpy_file, png_file, preamble, offset):
    image_cnt = 3  # Number of images to be taken
    im0 = np.zeros((rwidth, rheight), dtype=np.float)
    im1 = np.zeros((rwidth, rheight), dtype=np.float)
    im2 = np.zeros((rwidth, rheight), dtype=np.float)
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
    wrap = np.zeros((rheight, rwidth), dtype=np.float)
    im_wrap = np.zeros((rheight, rwidth), dtype=np.float)
    for j in range(rwidth):
        for i in range(rheight):
            wrap[i, j] = np.arctan2(1.7320508 * (1.0*im_arr[0][i, j]-im_arr[2][i, j])/2,
                                    (im_arr[1][i, j]-.5*im_arr[0][i, j]-.5*im_arr[2][i, j]))
            if wrap[i, j] < 0:
                wrap[i, j] += 2*np.pi
            im_wrap[i, j] = 128/np.pi * wrap[i, j]
    file_path = folder + '/' + numpy_file
    np.save(file_path, wrap, allow_pickle=False)
    png_file = folder + '/' + png_file
    cv2.imwrite(png_file, im_wrap)
    cv2.destroyAllWindows()


cv2.destroyAllWindows()
