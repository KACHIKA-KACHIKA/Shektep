from django.contrib import admin
from .models import *


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer', 'task_image_preview', 'pack_id')

    def get_changeform_initial_data(self, request):
        """Автоматически подставляет последний созданный Pack в поле pack_id."""
        last_pack = Pack.objects.order_by('-id').first()
        return {'pack_id': last_pack.id if last_pack else None}


admin.site.register(Task, TaskAdmin)
admin.site.register(Pack)
admin.site.register(SolvedPacks)
admin.site.register(Section)
admin.site.register(Subsection)
admin.site.register(SolvedTasks)
admin.site.register(ReadingImage)
