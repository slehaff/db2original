# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from django.contrib import admin

# Register your models here.
admin.site.register(ImageFolder)
admin.site.register(Image)
admin.site.register(Campose)
admin.site.register(Test)
admin.site.register(Calibration)
