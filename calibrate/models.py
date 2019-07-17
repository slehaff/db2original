# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.


class Camera(models.Model):
    date = models.DateTimeField(auto_now=True)
    cameraID = models.IntegerField(default=0)
    cameraType = models.CharField(max_length=200)
    resolution = models.CharField(max_length=20)
    calibrated = models.BooleanField(default=False)
    focusX = models.FloatField(default=0)
    focusY = models.FloatField(default=0)
    uCount = models.FloatField(default=0)
    vCount = models.FloatField(default=0)


class Calibration(models.Model):
    date = models.DateTimeField(auto_now=True)
    intrinsic = models.TextField(null=True, blank=True)
    distortion = models.TextField(null=True, blank=True)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, blank=True, null=True)


class ImageFolder(models.Model):
    date = models.DateTimeField(auto_now=True)
    folderName = models.CharField(max_length=200)
    imageCount = models.IntegerField(default=0)
    ResolutionX = models.IntegerField(default=0)
    ResolutionY = models.IntegerField(default=0)


class Image(models.Model):
    ResolutionX = models.IntegerField(default=0)
    ResolutionY = models.IntegerField(default=0)
    folder = models.ForeignKey(ImageFolder, on_delete=models.CASCADE)


class Campose(models.Model):
    date = models.DateTimeField(auto_now=True)
    coordx = models.FloatField(default=0)
    coordy = models.FloatField(default=0)
    coordz = models.FloatField(default=0)
    anglex = models.FloatField(default=0)
    angley = models.FloatField(default=0)
    anglez = models.FloatField(default=0)


class Test(models.Model):
    date = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=1)


def get_absolute_url(self):
    # return "/calib/%s/" %(self.id)
    return reverse('camdetail', kwargs={'id': self.id})


def __unicoede__(self):
    return self.title
