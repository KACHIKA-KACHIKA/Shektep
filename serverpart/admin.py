from django.contrib import admin

# Register your models here.
from .models import Section, Subsection, Pack, Task, SolvedTasks, SolvedPacks

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer', 'task_image_preview', 'pack_id')  # Добавляем превью изображения в список полей
admin.site.register(Task, TaskAdmin)
admin.site.register(Pack)
admin.site.register(SolvedPacks)
admin.site.register(Section)
admin.site.register(Subsection)
admin.site.register(SolvedTasks)