from django.db import models
class DownloadedVideo(models.Model):
    video_id = models.AutoField(primary_key=True)
    original_title = models.CharField(max_length=255)
    stored_filename = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)