from django.contrib import admin
from django.urls import path
from .views import helloworld

app_name = "youtube"
urlpatterns = [
    path('video_url/',helloworld ,name='youtube'),
]