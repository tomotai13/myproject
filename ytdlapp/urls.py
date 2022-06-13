from django.urls import path
from .views import helloworld, pytubeView, a, ajax_search, ajax_stream

app_name = "youtube"
urlpatterns = [
    path('video_url/', helloworld, name='youtube'),
    path('pytube_url/', pytubeView, name='pytube'),
    path('a/', a, name='a'),
    path('ajax_search/',ajax_search, name='ajax_search'),
    path('ajax_stream/', ajax_stream, name='ajax_stream'),
]