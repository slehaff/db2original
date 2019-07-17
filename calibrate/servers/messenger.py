import socket


def message1():
    IP = '192.168.0.50'
    port = 5005
    message = b'3singlecos'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (IP, port))


def message24():
    IP = '192.168.0.50'
    port = 5005
    message = b'3cos'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (IP, port))


def cam_cal_mess():
    IP = '192.168.0.50'
    port = 5005
    message = b'cam_cal'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (IP, port))


def pro_cal_mess():
    IP = '192.168.0.50'
    port = 5005
    message = b'procal'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (IP, port))


def wilm_cal_mess():
    IP = '192.168.0.50'
    port = 5005
    message = b'wilm_cal'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (IP, port))


