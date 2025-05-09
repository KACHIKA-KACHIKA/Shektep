from django.contrib import admin
from serverpart.admin_utils import make_assign_access_action, make_remove_access_action
from .models import (Pack, Task, SolvedPacks, Section,
                     Subsection, SolvedTasks, ReadingImage)



class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer', 'task_image_preview', 'pack_id')

    def get_changeform_initial_data(self, request):
        last_pack = Pack.objects.order_by('-id').first()
        return {'pack_id': last_pack.id if last_pack else None}

@admin.register(Pack)
class PackAdmin(admin.ModelAdmin):
    list_display = ('id', 'subsection', 'is_published')
    actions = [
        make_assign_access_action(),
        make_remove_access_action()
    ]


admin.site.register(Task, TaskAdmin)
admin.site.register(SolvedPacks)
admin.site.register(Section)
admin.site.register(Subsection)
admin.site.register(SolvedTasks)
admin.site.register(ReadingImage)
