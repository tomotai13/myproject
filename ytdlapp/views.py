from os import error
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.http import JsonResponse
import youtube_dl
from .forms import UrlForm

# Create your views here.
def helloworld(request):
    context={'form': UrlForm(),'video_url':'','video_title':'','video_title_ext':'','message':'',}

    if request.method == 'POST':
        try:
            url = request.POST.get('url')
            testUrl = url[0:33]
            if 'https://www.youtube.com/watch?v=' in testUrl or 'https://m.youtube.com/watch?v=' in testUrl:
                
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
                context['video_title_ext'] = result['title'] + '.' + format2['ext']
            else:
                context['message'] = '正しいURLを入力してください'
        except:
            context['message'] = 'エラーが発生しました'

    return render(request, 'ytdl/ytdl.html', context)
    

