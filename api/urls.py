from django.conf.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^(?P<proxy_path>.*)$', views.index, name='index'),
]
