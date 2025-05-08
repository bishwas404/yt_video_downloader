from django.shortcuts import render
from .forms import URLForm
from pytubefix import YouTube
import os
from django.conf import settings
from django.http import HttpResponse, FileResponse, Http404
import urllib



def url_view(request):
  if request.method=='POST':
    form=URLForm(request.POST)
    if form.is_valid():
      website_url=form.cleaned_data['website_url']

      try:
        yt=YouTube(website_url)
        stream=yt.streams.filter(progressive=True,file_extension='mp4').first()

        download_folder=os.path.join(settings.MEDIA_ROOT,'downloads')

        if not os.path.exists(download_folder):
          os.makedirs(download_folder)

        video_file_path=os.path.join(download_folder,f'{yt.title}.mp4')

        stream.download(output_path=download_folder,filename=f'{yt.title}.mp4')

        file_name = os.path.basename(video_file_path)

        return render(request,'downloader/url_success.html',{'website_url':website_url,'video_title':yt.title, 'video_path':video_file_path,'file_name':file_name})

      except Exception as e:
        return render(request,'downloader/url_failure.html',{'error_message':str(e)})

    else:
      return render(request,'downloader/home.html',{'form':form})
  else:
    form=URLForm()
    return render(request,'downloader/home.html',{'form':form})


def download(request,file_name):
  file_name = urllib.parse.unquote(file_name)
  file_name = file_name.replace('|', '')
  file_path=os.path.join(settings.MEDIA_ROOT,'downloads',file_name)
  if os.path.exists(file_path):
    with open(file_path, 'rb') as video_file:
      response = HttpResponse(video_file, content_type='video/mp4')
      response['Content-Disposition'] = f'attachment; filename="{file_name}"'
      return response
  else:
      return HttpResponse("Video not found.",status=404)