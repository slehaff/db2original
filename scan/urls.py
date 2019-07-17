from django.conf.urls import url
from . import views

app_name = 'scan'
urlpatterns = [
    url(r'$', views.main, name='main'),
    url(r'scan/$', views.take_scan),
    url(r'train/$', views.train_scan),
    url(r'ph24/$', views.ph24),
    url(r'reference/$', views.take_ref),
    url(r'unw/$', views.unwrap),
    # url(r'drop/$', views.dropdown),
    # url(r'3D/$', views.gamma_cal),

]
