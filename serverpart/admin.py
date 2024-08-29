from django.contrib import admin

# Register your models here.
from .models import Section, Subsection, Pack, Task, Test

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer', 'task_image_preview')  # Добавляем превью изображения в список полей
admin.site.register(Task, TaskAdmin)
admin.site.register(Pack)
admin.site.register(Test)
admin.site.register(Section)
admin.site.register(Subsection)