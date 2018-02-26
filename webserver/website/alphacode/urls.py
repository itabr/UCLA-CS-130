from django.conf.urls import url
from django.contrib import admin
# from django.urls import path
from . import views
from alphacode.models import RandomURLs

urlpatterns = [
    url(r'^$', views.index, name='post_list'),

    url(r'create/', views.create, name='create-view'),
    url(r'ajax/', views.getTag, name='ajax-view'),
    url(r'error/', views.error_page, name='error-view'),
    url(r'(?P<workplace_id>.*)/', views.workplace, name='workplace-view'),
]