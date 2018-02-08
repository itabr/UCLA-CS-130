from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main-view'),
    path('create/', views.create, name='create-view'),
    path('ajax/', views.whatever, name='ajax-view'),
    path('error/', views.error_page, name='error-view'),
    path('<workplace_id>/', views.workplace, name='workplace-view'),
]
