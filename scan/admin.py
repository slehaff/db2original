# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib import admin
from .models import ScanFolder, ScanJob


admin.site.register(ScanFolder)
admin.site.register(ScanJob)
