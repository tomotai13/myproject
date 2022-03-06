from unicodedata import name
from django.contrib import admin
from django.urls import path
from .views import pytubeView #test_view

app_name = "youtube"
urlpatterns = [
    path('pytube_url/', pytubeView, name='pytube'),
]