import numpy as np
import cv2
import argparse
import sys
import os
from PIL import Image
import os
from makewrap import *
from unwrap import *
from jsoncloud import *

high_freq = 15
low_freq = .7


def unwrap2():
    folder = '/home/samir/db2/scan/static/scan_folder/stars/scan_im_folder11/'
    # ref_folder = '/home/samir/db3/scan/static/scan_folder/scan_ref_folder'
    unwrap_r('scan_wrap2.npy', 'scan_wrap1.npy', folder )
    # deduct_ref('unwrap.npy', 'unwrap.npy', folder, ref_folder)
    # generate_json_pointcloud(folder + 'image2.png', folder + 'unwrap.png', folder +'pointcl.json')
    generate_pointcloud(folder + 'image2.png', folder + 'unwrap.png', folder +'pointcl.ply')
    
    return

unwrap2()