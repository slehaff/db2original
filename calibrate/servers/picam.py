import os
import shutil
import socket
import struct
import threading

import cv2
import numpy as np
import time
import pygame


def make_sound(filename):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    time.sleep(.9)
    # pygame.event.wait()


def mov_files( dir_to):
    path = '/home/samir/db2/calibrate/static/calib_folder/im_folder/'
    moveto = dir_to
    files = os.listdir(path)
    files.sort()
    for f in files:
        src = path + f
        dst = moveto + f
        shutil.move(src, dst)


def rcv_all(sock, count):
    buf = b''
    while count:
        new_buf = sock.recv(count)
        if not new_buf:
            return None
        buf += new_buf
        count -= len(new_buf)
    return buf


def receive_pi_data(n):
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8001))
    server_socket.listen(0)
    conn, adr = server_socket.accept()
    i = 0
    try:
        while True:
            make_sound('/home/samir/db2/calibrate/static/sound/take.mp3')
            image_len = struct.unpack('<L', conn.recv(struct.calcsize('<L')))[0]
            if not image_len:
                break
            string_data = rcv_all(conn, int(image_len))
            data = np.fromstring(string_data, dtype='uint8')
            dec_img = cv2.imdecode(data, 1)
            dec_img = cv2.flip(dec_img, 1)  # Invert image
            dec_img = cv2.flip(dec_img, 1)  # Invert image
            # dec_img = dec_img[25:265, 180:630]
            i += 1
            folder = '/home/samir/db2/calibrate/static/calib_folder/im_folder'
            cv2.imwrite(folder + '/image' + str(i)+'.png', dec_img)
            print(image_len)
    finally:
        conn.close()
        server_socket.close()
        print('closed')


def new_receive_pi_data(n, to_folder):
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8001))
    server_socket.listen(0)
    conn, adr = server_socket.accept()
    i = 0
    try:
        while True:
            file= 'home/samir'
            make_sound('/home/samir/db2/calibrate/static/sound/take.mp3')
            image_len = struct.unpack('<L', conn.recv(struct.calcsize('<L')))[0]
            if not image_len:
                break
            string_data = rcv_all(conn, int(image_len))
            data = np.fromstring(string_data, dtype='uint8')
            dec_img = cv2.imdecode(data, 1)
            dec_img = cv2.flip(dec_img, 1)  # Invert image
            dec_img = cv2.flip(dec_img, 1)  # Invert image
            # dec_img = dec_img[40:270, 170:600]
            i += 1
            folder = '/home/samir/db2/calibrate/static/calib_folder/im_folder'
            cv2.imwrite(folder + '/image' + str(i)+'.png', dec_img)
            print(image_len)
    finally:
        conn.close()
        server_socket.close()
        mov_files(to_folder)
        print('closed')


def make_receiver_thread(n):
    t = threading.Thread(target=receive_pi_data,
                         args=(n),
                         name='T1')
    t.start()


def new_receiver_thread(n, folder):
    t = threading.Thread(target=new_receive_pi_data,
                         args=(n, folder),
                         name='T1')
    t.start()
    return t

# folder = '/home/samir/danbotsIII/scan/static/scan/scanfolders/folder' + str(32)
# receive_pi_data()
