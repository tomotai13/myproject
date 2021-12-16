from django.test import TestCase

# Create your tests here.
"""
if request.method == 'POST':
        try:
            url = request.POST.get('url2')
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

            video_url = format2['url']
            video_title = result['title']
            d ={
            'video_url': video_url,
            'video_title': video_title,
            }
        except:

            d ={
                'error':'エラーが発生しました',
            }
"""