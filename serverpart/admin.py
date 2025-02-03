from django.contrib import admin
from .models import *


class TaskAdmin(admin.ModelAdmin):
    # Добавляем превью изображения в список полей
    list_display = ('id', 'answer', 'task_image_preview', 'pack_id')


admin.site.register(Task, TaskAdmin)
admin.site.register(Pack)
admin.site.register(SolvedPacks)
admin.site.register(Section)
admin.site.register(Subsection)
admin.site.register(SolvedTasks)
admin.site.register(ReadingImage)
