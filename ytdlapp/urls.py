from django.contrib import admin
from django.urls import path
from .views import helloworld, videoTest

app_name = "youtube"
urlpatterns = [
    path('video_url/', helloworld, name='youtube'),
    path('video_url_test/', videoTest, name='youtube_test'),
]