from django.contrib import admin
from django.urls import path, include
from .views import ViberUserView, set_webhook, callback, unset_webhook, ViberUserListView, ViberUserCreate


urlpatterns = [

    path('user/add/', ViberUserCreate.as_view()),
    path('all/', ViberUserListView.as_view(), name='users_all'),
    path('hi/', ViberUserView.as_view()),
    path('set_webhook/', set_webhook),
    path('callback/', callback),
    path('unset_webhook/', unset_webhook),
]