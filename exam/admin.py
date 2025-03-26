from django.contrib import admin
from .models import Exam, Difficulty, SolvedExam, ReadingBlock
admin.site.register(Exam)
admin.site.register(SolvedExam)
admin.site.register(Difficulty)
admin.site.register(ReadingBlock)
