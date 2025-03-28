from django.contrib import admin
from .models import Video, VideoTiming


class VideoTimingInline(admin.TabularInline):
    model = VideoTiming
    extra = 1


class VideoAdmin(admin.ModelAdmin):
    inlines = [VideoTimingInline]


admin.site.register(Video, VideoAdmin)
# admin.site.register(VideoTiming)
