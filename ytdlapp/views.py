#from django
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

#from third party
import youtube_dl
from pytube import YouTube, Search, Channel

#from other file
from .forms import UrlForm

#from standard
import json
import logging
import re
#import sys

logger = logging.getLogger('ytdlapp')

# Create your views here.
def helloworld(request):
    context={'form': UrlForm(),'video_url':'','video_title':'','video_title_ext':'','message':'',}

    if request.method == 'POST':
        try:
            url = request.POST.get('url')
            if 'https://www.youtube.com/watch?v=' in url or 'https://m.youtube.com/watch?v=' in url:

                output_file_name = 'a'
                ydl_opts = {
                    'format':'bestvideo+bestaudio/best',
                    'outtmpl':output_file_name + '.%(ext)s',
                }

                ydl = youtube_dl.YoutubeDL(ydl_opts)
                result = ydl.extract_info(url, download=False)
                formats = result['formats']
                formats2 =[]
                i = 0
                for format in formats:
                    if (format['acodec'] != 'none') and (format['vcodec'] != 'none'):
                        i += 1
                        formats2.append(format)
                format2 = formats2[i-1]

                context['video_url'] = format2['url']
                context['video_title'] = result['title']
            else:
                context['message'] = '正しいURLを入力してください'
        except:
            context['message'] = 'エラーが発生しました'

    return render(request, 'ytdl/ytdl.html', context)



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


def a(request):
    return render(request, 'ytdl/serachPtd.html',{})


@csrf_exempt
def ajax_search(request):

    if request.method == 'POST' and request.body:
        try:
            json_dict = json.loads(request.body)
            query = json_dict['query']

            s = Search(query)
            dict_data = {}
            d = []
            for r in s.results:
                dict_data['video_id'] = r.video_id
                dict_data['thumbnail_url'] = 'https://i.ytimg.com/vi/' + r.video_id + '/mqdefault.jpg'
                dict_data['title'] = r.title
                d.append(dict_data.copy())
        except:
            logger.error(query)
            d.append('error')
        else:
            logger.info(query)
        d = json.dumps(d, ensure_ascii=False)

        return JsonResponse(d, safe=False)


@csrf_exempt
def ajax_stream(request):
    if request.method == "POST":

        d = {'error':None,}
        json_dict = json.loads(request.body)
        id = json_dict['video_id']
        if len(id) == 11:
            url = 'https://www.youtube.com/watch?v={}'.format(id)

        if 'https' in url or 'youtu' in url:
            yt_obj = YouTube(url)
            d['channel_id'] = yt_obj.channel_id
            d['author'] = yt_obj.author
            try:
                try:
                    stream = yt_obj.streams.get_by_itag(22)
                    d['stream_url'] = stream.url
                    d['stream_title'] = stream.title
                except:
                    stream = yt_obj.streams.get_by_itag(18)
                    d['stream_url'] = stream.url
                    d['stream_title'] = stream.title
            except:
                d['error'] = 'error'
                logger.error(url)
            else:
                logger.info(d['stream_title'])


        d = json.dumps(d, ensure_ascii=False)

        return JsonResponse(d, safe=False)


@csrf_exempt
def ajax_ch_search(request):

    if request.method == 'POST' and request.body:
        try:
            json_dict = json.loads(request.body)
            ch_id = json_dict['channel_id']
            ch_url = 'https://www.youtube.com/channel/'+ch_id
            c = Channel(ch_url)
            dict_data = {}
            d = []
            for r in c.videos[:20]:
                dict_data['video_id'] = r.video_id
                dict_data['thumbnail_url'] = 'https://i.ytimg.com/vi/' + r.video_id + '/mqdefault.jpg'
                dict_data['title'] = r.title
                d.append(dict_data.copy())
        except:
            d.append('error')
        d = json.dumps(d, ensure_ascii=False)
        return JsonResponse(d, safe=False)
