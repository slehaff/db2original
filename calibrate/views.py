# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
import shutil
import time

from calibrate.models import Calibration, Campose
from calibrate.models import Camera
from calibrate.pylib.calibrate import calibrate, undistort
from calibrate.pylib.pose import pose
from calibrate.pylib.takes import *
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from calibrate.servers.messenger import cam_cal_mess
from calibrate.servers.picam import make_receiver_thread
from calibrate.servers.picam import new_receiver_thread


def cam_librate(folder):
    mtx, dist, rvecs, tvecs = calibrate(folder)
    mtxs = json.dumps(mtx.tolist())
    dists = json.dumps(dist.tolist())
    cal = Calibration(
        intrinsic=mtxs,
        distortion=dists,
        camera=Camera.objects.last())
    cal.save()
    # undistort(folder, mtx, dist, 640, 480)


def mov_files(dir_to):
    path = '/home/samir/db2/calibrate/static/calib_folder/im_folder/'
    moveto = dir_to
    files = os.listdir(path)
    files.sort()
    for f in files:
        src = path + f
        dst = moveto + f
        shutil.move(src, dst)


# def wrap_wil(set_count, folder):
#     print('wrap_wil started')
#     for i in range(set_count):
#         print(i)
#         print(folder)
#         take_v_wrap(folder, 'wil_wrap1' + str(i) + '.npy', 'im_wrap1' + str(i) + '.png', 'image', i*13+1)
#         take_wrap(folder, 'wil_wrap2' + str(i) + '.npy', 'im_wrap2' + str(i) + '.png', 'image', i*13+4)
#         take_wrap(folder, 'wil_wrap3' + str(i) + '.npy', 'im_wrap3' + str(i) + '.png', 'image', i*13+7)
#         take_v_wrap(folder, 'wil_wrap4' + str(i) + '.npy', 'im_wrap4' + str(i) + '.png', 'image', i*13+10)
#         shutil.move(folder + 'image' + str(i*13 + 1) + '.png', folder + 'cal_wil/image' + str(i*13 + 1) + '.png')
#         i += 1


# Create your views here.


def index(request):
    return HttpResponse(' Cool irt')


def main(request):
    folder = '/static/scan/scanfolders/' + 'folder20'
    # make_receiver_thread()
    context = {
        'MyLink': folder + '/image1.png',
        'MyFolder': folder,
    }
    print('main')
    return render(request, 'calibtemplate.html', context)


def camdetail(request, id=None):
    instance = get_object_or_404(Camera, id=id)
    context = {
        'instance': instance,
    }
    return render(request, 'camera_detail.html', context)


def camlist(request):
    qset = Camera.objects.all()
    context = {
        'qset': qset,
        'title': 'List'
    }
    return render(request, 'camera_list.html', context)


def bootstrap(request):
    context = {
        'title': 'List'
    }
    return render(request, 'bootstrap.html', context)


def buttest(request):
    context = {
        'title': 'List'
    }
    return render(request, 'buttest.html', context)


def results(request, input_id):
    return HttpResponse('This is the detail view of my calibration %s' % input_id)


def campose(request):
    folder = '/home/samir/db2/calibrate/static/calib_folder/cal_im_folder/'
    mypose = pose(folder)
    print('campose:', mypose)
    print('json campose', mypose)
    newpose = Campose(
        coordx=mypose['campositionx'][0],
        coordy=mypose['campositiony'][0],
        coordz=mypose['campositionz'][0],
        anglex=mypose['anglex'],
        angley=mypose['angley'],
        anglez=mypose['anglez']
    )
    newpose.save()
    return HttpResponse('This is the pose view of my calib app %s')


def camcalib(request):
    print('camcalib called')
    folder = '/home/samir/db2/calibrate/static/calib_folder/cal_im_folder/'  # + folder
    cam_librate(folder=folder)
    return HttpResponse('This is the calibrate view of my calibration %s')


def takeimages(request):
    print('take me!')
    folder = '/home/samir/db2/calibrate/static/calib_folder/cal_im_folder/'
    t = new_receiver_thread('1', folder=folder)
    time.sleep(5)
    print('start take!')
    cam_cal_mess()
    time.sleep(20)
    folder = '/home/samir/db2/calibrate/static/calib_folder/cal_im_folder/'
    mov_files(folder)
    return HttpResponse('This is the take images view of my calibration %s')


# def take_wilm(request):
#     scans = 1
#     print('take wilm')
#     folder = '/home/samir/danbotsIII/calibrate/static/calib_folder/wilm_im_folder/'
#     t = new_receiver_thread('1', folder=folder)
#     print('calibrate receiver started')
#     time.sleep(5)
#     print('start take')
#     wilm_cal_mess()
#     t.join()
#     wrap_wil(set_count=scans, folder=folder)
#     # cam_librate(folder=folder + 'cal_wil')
#     return HttpResponse('This is the take images view of my calibration %s')


# def takeproimages(request):
#     print('take pro!')
#     time.sleep(5)
#     print('start pro take!')
#     pro_cal_mess()
#     folder = '/home/samir/danbotsIII/calibrate/static/calib_folder/pro_im_folder/'  # +folder
#     print('pro_wrap me')
#     time.sleep(15)
#     mov_files(folder)
#     os.rename(folder+'image14.png', folder+'image21.png')
#     os.rename(folder+'image15.png', folder+'image22.png')
#     os.rename(folder+'image16.png', folder+'image23.png')
#     take_wrap(folder, 'pro_wrap1.npy', 'im_wrap1.png', 'image1', 0)
#     take_v_wrap(folder, 'pro_wrap2.npy', 'im_wrap2.png', 'image2', 0)
#     return HttpResponse('This is the take images view of my calibration %s')


def newscan(request):
    make_receiver_thread('1')
    print('calibrate receiver started')
    return render(request, 'calibtemplate.html')
