import cv2
import numpy as np
import math


rheight = 480
rwidth = 640


def getPhase(I1, I2, I3):
    phase = np.zeros((rheight, rwidth), dtype=np.float)
    nom = np.zeros((rheight, rwidth), dtype=np.float)
    denom = np.zeros((rheight, rwidth), dtype=np.float)
    for i in range(rheight):
        for j in range(rwidth):
            nom[i, j] = 1.7320508 * (I1[i, j] - I3[i, j])
            denom[i, j] = 2*I2[i, j] - (I1[i, j] + I3[i, j])
            phase[i, j] = np.arctan2(nom[i, j], denom[i, j])
            if phase[i, j] < 0:
                if nom[i, j] < 0:
                    phase[i, j] += 2*np.pi
                else:
                    phase[i, j] += 1 * np.pi
            # im_wrap[i, j] = 128/np.pi * wrap[i, j]

    # phase = 128/np.pi*phase
    return(phase, nom, denom)


def getNom(I1, I2, I3):
    nom = np.subtract(np.multiply(2, I1), np.add(I2, I3))
    return(nom)


def getDenom(I1, I2, I3):
    denom = 1.7320508 * np.subtract(I2, I3)
    return(denom)


def getMagnitude(I1, I2, I3):
    magnitude = cv2.magnitude(2*I1 - I3 - I2, 3**.5 * (I2 - I3))
    return(magnitude)


def unwrapWithCue(up, upCue, nphases):
    return


def decodeFrames():
    return


def cpptake_wrap(folder, numpy_file, png_file, preamble, offset):
    image_cnt = 3  # Number of images to be taken
    mask = np.zeros((rwidth, rheight), dtype=np.bool)
    im0 = np.zeros((rwidth, rheight), dtype=np.float)
    im1 = np.zeros((rwidth, rheight), dtype=np.float)
    im2 = np.zeros((rwidth, rheight), dtype=np.float)
    im_arr = [im0, im1, im2]
    for i in range(image_cnt):
        my_file = folder + preamble + str(offset+i+1) + ".png"
        print(my_file)
        image = cv2.imread(my_file)
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        im_arr[i] = grey

    up, nom, denom = getPhase(im_arr[0], im_arr[1], im_arr[2])
    nom_file = folder + '/' + str(offset) + 'nom.png'
    cv2.imwrite(nom_file, nom)
    denom_file = folder + '/' + str(offset) + 'denom.png'
    cv2.imwrite(denom_file, denom)
    print('shape:', up.shape)
    up *= up / (2*math.pi)
    up = cv2.GaussianBlur(up, (3, 3), 0)
    shading = getMagnitude(im0, im1, im2)
    avg = .333 * im0 + .333 * im1 + .333 * im2
    mask = shading > 10
    dx = cv2.Sobel(shading, -1, 1, 0, 3)
    dy = cv2.Sobel(shading, -1, 0, 1, 3)
    edgeshading = np.absolute(dx) + np.absolute(dy)
    dx = cv2.Sobel(up, -1, 1, 0, 3)
    dy = cv2.Sobel(up, -1, 0, 1, 3)
    edgesup = np.absolute(dx) + np.absolute(dy)
    edgesup = np.transpose(edgesup)
    print('eup:', edgesup.shape)
    print('mask:', mask.shape)

    mask = mask & (edgesup < 80)
    mask = np.transpose(mask)
    mask_im = mask * 128

    im_wrap = up*128/np.pi * up
    file_path = folder + '/' + numpy_file
    np.save(file_path, up, allow_pickle=False)  # Save wrap
    png_file = folder + '/' + png_file
    cv2.imwrite(png_file, im_wrap)  # Save im_wrap
    file_path = folder + '/' + numpy_file[:-4] + '_mask.npy'
    np.save(file_path, mask, allow_pickle=False)  # Save mask
    file_path = folder + '/' + numpy_file[:-4] + '_mask.png'
    cv2.imwrite(file_path, mask_im)  # Save mask_im

    return
