from django.contrib import admin
from .models import Exam, Difficulty, SolvedExam, ReadingBlock
from serverpart.admin_utils import make_assign_access_action, make_remove_access_action

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    actions = [
        make_assign_access_action(),
        make_remove_access_action()
    ]

admin.site.register(SolvedExam)
admin.site.register(Difficulty)
admin.site.register(ReadingBlock)
