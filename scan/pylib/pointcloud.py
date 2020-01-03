
import argparse
import sys
import os
from PIL import Image
import cv2
import numpy as np
from pyntcloud import PyntCloud

focalLength = 1290
centerX = 292
centerY = 286
scalingFactor = 5000  # 5000.0
rwidth = 640
rheight = 480


def generate_color_pointcloud(rgb_file, depth_file, ply_file):
    """
    Generate a colored point cloud in PLY format from a color and a depth image.

    Input:
    rgb_file -- filename of color image
    depth_file -- filename of depth image
    ply_file -- filename of ply file

    """
    rgb = Image.open(rgb_file)
    depth = Image.open(depth_file)
    rgb = rgb.transpose(Image.FLIP_TOP_BOTTOM)
    depth = depth.transpose(Image.FLIP_TOP_BOTTOM)
    print(depth.mode)
    print(rgb.mode)
    if rgb.size != depth.size:
        raise Exception("Color and depth image do not have the same resolution.")
    if rgb.mode != "RGB":
        raise Exception("Color image is not in RGB format")
    if depth.mode != "L":
        raise Exception("Depth image is not in intensity format")

    points = []
    for v in range(rgb.size[1]):
        for u in range(rgb.size[0]):
            color = rgb.getpixel((u, v))
            # Z = depth.getpixel((u, v)) / scalingFactor
            # if Z == 0: continue
            # X = (u - centerX) * Z / focalLength
            # Y = (v - centerY) * Z / focalLength
            Z = depth.getpixel((u, v)) * .22
            if Z == 0: continue
            Y = .22 * v
            X = .22 * u
            points.append("%f %f %f %d %d %d 0\n" % (X, Y, Z, color[0], color[1], color[2]))
    file = open(ply_file, "w")
    file.write('''ply
        format ascii 1.0
        element vertex %d
        property float x
        property float y
        property float z
        property uchar red
        property uchar green
        property uchar blue
        property uchar alpha
        end_header
        %s
        ''' % (len(points), "".join(points)))
    file.close()


def generate_pointcloud(depth_file, ply_file):
    """
    Generate a colored point cloud in PLY format from a color and a depth image.

    Input:
    rgb_file -- filename of color image
    depth_file -- filename of depth image
    ply_file -- filename of ply file

    """
    my_depth = Image.open(depth_file)
    print(my_depth.mode)
    depth = cv2.imread(depth_file)

    # if depth.mode != "I":
    #     raise Exception("Depth image is not in intensity format")

    points = []
    for i in range(rheight):
        for j in range(rwidth):
            Z = depth[i, j]*.44
            Y = .22 * j
            X = .22 * i
            # print(Z[1])
            points.append("%d %d %d \0\n" % (X,Y,Z[1]))
    file = open(ply_file, "w")
    file.write('''ply
    format ascii 1.0
    element vertex %d
    property float x
    property float y
    property float z
    end_header
    %s
    ''' % (len(points), "".join(points)))
    file.write("\n")
    print(len(points))


