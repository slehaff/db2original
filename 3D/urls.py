from django.conf.urls import url

from . import views

app_name = '3D'
urlpatterns = [
    url(r'$', views.main, name='main'),
]
