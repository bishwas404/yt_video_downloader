from django.shortcuts import render
from .forms import URLForm
from pytubefix import YouTube
import os,uuid
from django.conf import settings
from django.http import HttpResponse, FileResponse, Http404
from .models import DownloadedVideo



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

        safe_file_name=f'{uuid.uuid4()}.mp4'

        video_file_path=os.path.join(download_folder,safe_file_name)

        stream.download(output_path=download_folder,filename=safe_file_name)

        video=DownloadedVideo.objects.create(
          original_title=yt.title,
          stored_filename=safe_file_name
        )

        return render(request,'downloader/url_success.html',{
          'video_title': yt.title,
          'video_id': video.video_id,
          'website_url': website_url})

      except Exception as e:
        return render(request,'downloader/url_failure.html',{'error_message':str(e)})

    else:
      return render(request,'downloader/home.html',{'form':form})
  else:
    form=URLForm()
    return render(request,'downloader/home.html',{'form':form})


def download(request,video_id):
  video=DownloadedVideo.objects.get(pk=video_id)
  file_path=os.path.join(settings.MEDIA_ROOT,'downloads',video.stored_filename)
  if os.path.exists(file_path):
    with open(file_path, 'rb') as video_file:
      response = HttpResponse(video_file, content_type='video/mp4')
      response['Content-Disposition'] = f'attachment; filename="{video.original_title}"'
      return response
  else:
      return HttpResponse("Video not found.",status=404)
