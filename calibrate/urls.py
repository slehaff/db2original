from django.conf.urls import url

from . import views

app_name = 'calibrate'
urlpatterns = [
    url(r'$', views.main, name='main'),
    url(r'take/$', views.takeimages),
    url(r'camera/$', views.camcalib),
    url(r'wilm/$', views.main),
    url(r'pose/$', views.campose),
    url(r'pro/$', views.main),
    url(r'newscan/$', views.newscan),
]