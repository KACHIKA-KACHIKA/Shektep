from django.contrib import admin

# Register your models here.
from .models import Section, Subsection, Theme, Task, Test

admin.site.register(Task)
admin.site.register(Test)
admin.site.register(Section)
admin.site.register(Subsection)
admin.site.register(Theme)