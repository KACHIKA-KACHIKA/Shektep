from django.contrib import admin
from .models import Video, VideoTiming
from serverpart.admin_utils import make_assign_access_action, make_remove_access_action


class VideoTimingInline(admin.TabularInline):
    model = VideoTiming
    extra = 1


class VideoAdmin(admin.ModelAdmin):
    inlines = [VideoTimingInline]
    actions = [
        make_assign_access_action(),
        make_remove_access_action()
    ]



admin.site.register(Video, VideoAdmin)
