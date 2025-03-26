from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='video_preview/', null=True)
    file_url = models.URLField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class VideoTiming(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    time = models.TimeField()
    label = models.CharField(max_length=255)

    def __str__(self):
        return f"Точка {self.time} - {self.label}"
