from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from exam.views import *
from user.views import *
from serverpart.views import *
from videoplayer.views import *
urlpatterns = [
	path('api/subsection/', SubsectionAPI.as_view(), name="subsection"),
	path('api/pack/', PackAPI.as_view(), name="pack"),
	path('api/task/', TaskAPI.as_view(), name="task"),

	path('api/task_answer/', TaskAnswerAPI.as_view(), name="task_answer"),

	path('api/exams/', ExamsAPI.as_view(), name='exams'),

	path('api/exam/', ExamAPI.as_view(), name='exam'),
	path('api/difficulty/', DifficultyAPI.as_view(), name='difficulty'),
	# path('api/reading_block/', ReadingBlockAPI.as_view(), name='reading_block'),

	path('api/solve_exam/', CorrectExamAPI.as_view(), name='solve_exam'), # Записать результат решенного экзамена
	path('api/solved_exam/', SolvedExamAPI.as_view(), name='solved_exam'), # Узнать какие экзамены решены, для открытия доступа к другим

	path('api/solve_pack/', SolvePackAPI.as_view(), name='solve_task'), # Записать результат теста

	path('api/video/', VideoDetailAPIView.as_view(), name='video-detail'),
	# path('api/video-stream/', VideoStreamingAPIView.as_view(), name='video-stream'),
	path('api/video_timing/', VideoTimingAPIView.as_view(), name='video-timings'),

	path('', home, name='home'),
	path('tests/', include('serverpart.urls')),
	path('user/', include('user.urls')),
	path('vp/', include('videoplayer.urls')),
	path('exams/', include('exam.urls')),
	path('admin/', admin.site.urls),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)