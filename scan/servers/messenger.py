import socket
import pickle

IP = '192.168.0.50'
port = 5005


def message1():
    message = b'3singlecos'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (IP, port))


def message24():
    message = b'3cos'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (IP, port))


def cam_cal_mess():
    message = b'cam_cal'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (IP, port))


def pro_cal_mess():
    message = b'pro_cal'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (IP, port))


def scan_mess():
    print('NewIP, port:', IP, port)
    message = b'scan'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (IP, port))


def abs_scan_mess():
    message = b'abs_scan'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (IP, port))


def train_scan_mess():
    message = b'train_scan'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (IP, port))


def gamma_mess():
    message = b'gamma_scan'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (IP, port))


def gamma_correction(gam_cor):
    message = pickle.dumps(gam_cor)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (IP, port))
