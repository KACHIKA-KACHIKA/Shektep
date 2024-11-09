from django.contrib import admin
from .models import Exam, Difficulty, SolvedExam, ReadingBlock
# Register your models here.
admin.site.register(Exam)
admin.site.register(SolvedExam)
admin.site.register(Difficulty)
admin.site.register(ReadingBlock)