from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^callback/', views.callback, name='callback'),
    url(r'^clear_cache/', views.clear_auth_cache, name='clear_auth_cache'),
]
