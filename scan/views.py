# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from scan.models import ScanFolder
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from scan.pylib.cmakewrap import *
from scan.pylib.cppmakewrap import *
from scan.pylib.naive_unwrapper import *
from scan.pylib.abswrap import *
from scan.pylib.unwrap import *
from scan.pylib.pointcloud import *
from scan.pylib.jsoncloud import *
from scan.servers.picam import new_receiver_thread
import os
from scan.servers.picam import receive_pi_data
from scan.servers.picam import make_receiver_thread
from scan.servers.messenger import *
import shutil
import json
from distutils.dir_util import copy_tree
import shutil

# ************************************************ Help Methods *******************************************************
foldercount = 0  # folder counter

def mov_files(dir_to):
    path = '/home/samir/db2/scan/static/scan/scans/'
    moveto = dir_to
    files = os.listdir(path)
    files.sort()
    for f in files:
        src = path + f
        dst = moveto + f
        shutil.move(src, dst)


def trim_files(folder):
    for i in range(6):
        my_file = folder + '/image' + str(i+1) + '.png'
        image = cv2.imread(my_file)
        image = image[40:270, 170:600]
        cv2.imwrite(my_file, image)
    return


def scan_wrap(folder):
    print('scan_wrap started')
    print(folder)
    take_wrap(folder, 'scan_wrap1.npy', 'im_wrap1.png', 'image', 1)
    take_wrap(folder, 'scan_wrap2.npy', 'im_wrap2.png', 'image', 4)


def cppscan_wrap(folder):
    print('cppscan_wrap started')
    print(folder)
    cpptake_wrap(folder, 'scan_wrap1.npy', 'im_wrap1.png', 'image', 1)
    cpptake_wrap(folder, 'scan_wrap2.npy', 'im_wrap2.png', 'image', 4)


def train_wrap(folder):
    print('train_wrap started')
    print(folder)
    take_wrap(folder, 'scan_wrap1.npy', 'im_wrap1.png', 'image', 1)
    take_wrap(folder, 'scan_wrap2.npy', 'im_wrap2.png', 'image', 4)


def scan_wrap4(folder):
    print('scan_wrap started')
    print(folder)
    take_wrap4(folder, 'scan_wrap1.npy', 'im_wrap1.png', 'image', 0)


# def abs_wrap(folder):
#     print('abs_scan_wrap started')
#     print(folder)
#     os.rename(folder + 'image7.png', folder + 'image9.png')
#     os.rename(folder + 'image8.png', folder + 'image10.png')
#     abs_wrap1(folder, 'scan_wrap1.npy', 'im_wrap1.png', 'image', 0)
#     abs_wrap2(folder, 'scan_wrap2.npy', 'im_wrap2.png', 'image', 4)
#     abs_wrap3(folder, 'scan_wrap3.npy', 'im_wrap3.png', 'image', 8)
#     abs_unwrap_r('scan_wrap3.npy', 'scan_wrap2.npy',
#                  'unwrap_low.png', folder + '/')
#     abs_unwrap_r('scan_wrap2.npy', 'scan_wrap1.npy',
#                  'unwrap_high.png', folder + '/')

# ***********************************************Main Methods *********************************************************


def main(request):
    # folder = ScanFolder.objects.last().folderName + '/'
    folder = '/static/scan_folder/' + 'scan_im_folder'
    # make_receiver_thread()
    context = {
        'MyLink': folder + 'image1.png',
        'MyFolder': folder,
    }
    print('main')
    return render(request, 'scantemplate.html', context)


def take_scan(request):
    print('take scan')
    folder = '/home/samir/db2/scan/static/scan_folder/scan_im_folder/'
    t = new_receiver_thread('1', folder=folder)
    print('scan receiver started')
    print('start take')
    scan_mess()
    t.join()
    folder = '/home/samir/db2/scan/static/scan_folder/scan_im_folder/'
    # trim_files(folder)
    scan_wrap(folder=folder)
    # cppscan_wrap(folder=folder)
    return HttpResponse('This is the take images view of my scan %s')


def train_scan(request):
    print('train scan')
    folder = '/home/samir/db2/scan/static/scan_folder/train_scan_folder/'
    t = new_receiver_thread('1', folder=folder)
    print('train scan receiver started')
    print('start train take')
    train_scan_mess()
    t.join()
    train_wrap(folder=folder)
    return HttpResponse('This is the take images view of my scan %s')


def take_ref(request):
    print('take reference')
    folder = '/home/samir/db2/scan/static/scan_folder/scan_ref_folder/'
    t = new_receiver_thread('1', folder=folder)
    print('reference receiver started')
    print('start take')
    scan_mess()
    t.join()
    scan_wrap(folder=folder)
    unwrap_r('scan_wrap2.npy', 'scan_wrap1.npy', folder + '/')
    return HttpResponse('This is the take images view of my scan %s')


def train_data(request):
    global foldercount
    foldercount += 1
    print('train data!', foldercount)
    scanfolder = '/home/samir/db2/scan/static/scan_folder/scan_im_folder/'
    folder = '/home/samir/db2/scan/static/scan_folder/train_im_folder/'+str(foldercount)+ 'scan_im_folder/'
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)
    copy_tree(scanfolder, folder)
    ref_folder = '/home/samir/db2/scan/static/scan_folder/scan_ref_folder'
    three_folder = '/home/samir/db2/3D/static/3scan_folder'
    unwrap_r('scan_wrap2.npy', 'scan_wrap1.npy', folder )
    deduct_ref('unwrap.npy', 'unwrap.npy', folder, ref_folder)
    # generate_color_pointcloud(folder + 'image1.png', folder + '/abs_unwrap.png', folder + '/pointcl.ply')
    generate_json_pointcloud(folder + 'image1.png', folder +
                             '/unwrap.png', three_folder + '/pointcl.json')
    generate_json_pointcloud(folder + 'image1.png', folder +
                            '/unwrap.png', folder + '/pointcl.json')
    return render(request, 'scantemplate.html')


def unwrap(request):
    # folder = ScanFolder.objects.last().folderName
    folder = '/home/samir/db2/scan/static/scan_folder/scan_im_folder/'
    ref_folder = '/home/samir/db2/scan/static/scan_folder/scan_ref_folder'
    three_folder = '/home/samir/db2/3D/static/3scan_folder'
    unwrap_r('scan_wrap2.npy', 'scan_wrap1.npy', folder )
    deduct_ref('unwrap.npy', 'unwrap.npy', folder, ref_folder)
    # generate_color_pointcloud(folder + 'image1.png', folder + '/abs_unwrap.png', folder + '/pointcl.ply')
    generate_json_pointcloud(folder + 'image1.png', folder +
                             '/abs_unwrap.png', three_folder + '/pointcl.json')
    generate_color_pointcloud(folder + 'image1.png', folder + '/unwrap.png', folder + 'pointcloud.ply')
    return render(request, 'scantemplate.html')


def newscan(request):
    make_receiver_thread('1')
    print('receiver started')
    return render(request, 'scantemplate.html')


def dropdown(request):
    # print('server dropdown')
    # # return render(request, 'scantemplate.html')
    # folder = '/static/scan/scanfolders/' + 'something'
    # # make_receiver_thread()
    # context = {
    #     'MyFolder': folder,
    # }
    return render(request, 'scantemplate.html')


# def gamma_cal(request):
#     print('3D')
#     folder = '/home/samir/db2/scan/static/scan_folder/gamma_im_folder/'
#     t = new_receiver_thread('1', folder=folder)
#     gamma_mess()
#     t.join()
#     # gam = gamma_curve(folder)
#     compensate_gamma(folder + 'image1.png')
#     return render(request, 'scantemplate.html')


#  #********************************************************************************************************************


# def wrap(request):
#     # folder = ScanFolder.objects.last().folderName
#     folder = '/home/samir/danbotsIII/scan/static/scan/scanfolders/folder20'  # +folder
#     # os.makedirs(folder)
#     print('wrap me')
#     message1()
#     time.sleep(10)
#     take_wrap(folder, 'wrap1.npy', 'imwrap1.png', 'image1')
#     make_receiver_thread('2')
#     message24()
#     time.sleep(10)
#     take_wrap(folder, 'wrap2.npy', 'imwrap2.png', 'image2')
#     print('wrap')
#     return render(request, 'scantemplate.html')


def refs(request):
    print('refs')
    return render(request, 'scantemplate.html')


def ph1(request):
    print('ph1')
    return render(request, 'scantemplate.html')


def ph24(request):
    folder = ScanFolder.objects.last().folderName
    folder = '/home/samir/danbotsIII/scan/static/scan/scanfolders/' + folder

    context = {
        'MyFolder': folder,
    }
    print('ph24')
    return render(request, 'scantemplate.html', context)
