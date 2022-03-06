#from django
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

#from third party
import youtube_dl
from pytube import YouTube, Search

#from other file
from .forms import UrlForm

#from standard
import json
import logging
import re
# Create your views here.

logger = logging.getLogger('ytdlapp')

def pytubeView(request):
    context={'form':UrlForm(), 'video':'', 'message':'','title':'',}


    if request.method == 'POST':

        url = request.POST.get('url')
        #mp34 = request.POST.get('mp34')
        g_url = re.compile(r'%3D([a-zA-Z0-9-_\.]{11})&usg').search(url)

        if g_url is not None:
            id = g_url.groups()[0]
            url = 'https://www.youtube.com/watch?v={}'.format(id)

        if len(url) == 11:
            url = 'https://www.youtube.com/watch?v={}'.format(url)

        check_url = url[0:33]

        if 'https:' in check_url and 'youtu' in check_url:
            try:
                try:
                    streams = YouTube(url).streams
                    stream = streams.get_by_itag(22)
                    context['video'] = stream.url
                    context['title'] = stream.title

                except:
                    streams = YouTube(url).streams
                    stream = streams.get_by_itag(18)
                    context['video'] = stream.url
                    context['title'] = stream.title

            except Exception as e:
                context['message'] = e
                logger.error(e)

            else:
                logger.info(context['title'])
        else:
            context['message'] = '正しいURLを入力してください'

    return render(request, 'ytdl/ptd.html', context)