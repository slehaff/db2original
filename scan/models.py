from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.


class ScanFolder(models.Model):
    date = models.DateTimeField(auto_now=True)
    folderName = models.CharField(max_length=200)
    fileCount = models.IntegerField(default=0)


class ScanJob(models.Model):
    data = models.DateTimeField(auto_now=True)


def get_absolute_url(self):
    # return "/calib/%s/" %(self.id)
    return reverse('camdetail', kwargs={'id': self.id})
