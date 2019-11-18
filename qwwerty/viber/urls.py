from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('set_webhook/', views.set_webhook),
    path('callback/', views.callback),
]