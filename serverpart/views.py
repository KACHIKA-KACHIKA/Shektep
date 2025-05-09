from django.shortcuts import get_object_or_404, render
from .models import Section, Task, Subsection, Pack, SolvedTasks, SolvedPacks

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from user.permissions import get_user_active_access_rights
from user.models import Lesson, UserLessonProgress
from user.serializers import LessonsSerializer


class TaskAPI(APIView):
    def get(self, request):
        pack_id = request.GET.get('pack_id')
        if not pack_id:
            return Response({'error': 'pack_id is required'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            pack = Pack.objects.get(id=pack_id)
            tasks = Task.objects.filter(pack_id=pack_id)
            subsection = Subsection.objects.filter(
                id=pack.subsection_id).values('name').first()
            subsection_name = subsection['name'] if subsection else None
            tasks_data = [
                {
                    'id': task.id,
                    'task_answer': task.answer,
                    'task_image_url': task.task_image.url if task.task_image else None,
                    'subsection': subsection_name,
                }
                for task in tasks
            ]
            reading_images = []
            if subsection_name == "Чтение и понимание текста":
                reading_images = [
                    image.image.url for image in pack.reading_images.all()
                ]

            return Response({
                'tasks_data': tasks_data,
                'reading_images': reading_images
            }, status=status.HTTP_200_OK)

        except Pack.DoesNotExist:
            return Response({'error': 'Pack not found'},
                            status=status.HTTP_404_NOT_FOUND)


class PackAPI(APIView):
    def get(self, request):
        subsection_id = request.GET.get('subsection_id')
        user = request.user

        if not subsection_id:
            return Response({'error': 'subsection_id is required'}, status=400)

        packs = Pack.objects.filter(
            subsection_id=subsection_id,
            is_published=True
        ).prefetch_related('access_rights')

        user_rights = set()
        solved_map = {}

        if user.is_authenticated:
            user_rights = set(get_user_active_access_rights(user))
            solved_packs = SolvedPacks.objects.filter(user=user)
            solved_map = {sp.pack_id: sp.percent for sp in solved_packs}

        result = []
        for pack in packs:
            has_access = bool(set(pack.access_rights.all()) & user_rights)
            result.append({
                'id': pack.id,
                'solved_percent': solved_map.get(pack.id, 0) if has_access else 0
            })

        return Response(result, status=200)


class SolvePackAPI(APIView):
    def get(self, request):
        pack_id = request.GET.get('pack_id')
        user = request.user

        if not pack_id:
            return Response({'error': 'pack_id is required'},
                            status=status.HTTP_400_BAD_REQUEST)
        if not user.is_authenticated:
            return Response({"error": "User is not authenticated"},
                            status=status.HTTP_403_FORBIDDEN)
        try:
            pack = Pack.objects.prefetch_related(
                'access_rights').get(id=pack_id)

            user_rights = set(get_user_active_access_rights(user))
            pack_rights = set(pack.access_rights.all())

            if not user_rights & pack_rights:
                return Response({'error': 'Access denied'},
                                status=status.HTTP_403_FORBIDDEN)
        except Pack.DoesNotExist:
            return Response({'error': 'Pack not found'},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            solved_pack = SolvedPacks.objects.get(user=user, pack=pack)
            return Response({"percent": solved_pack.percent},
                            status=status.HTTP_200_OK)
        except SolvedPacks.DoesNotExist:
            return Response({'error': 'Solved data not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user = request.user
        pack_id = request.data.get('pack_id')
        solved_percent = request.data.get('solved_percent')
        if not user.is_authenticated:
            return Response({"error": "User is not authenticated"},
                            status=status.HTTP_403_FORBIDDEN)

        if not pack_id or solved_percent is None:
            return Response({"error": "Нужен pack_id и solved_percent."},
                            status=status.HTTP_400_BAD_REQUEST)

        pack = get_object_or_404(
            Pack.objects.prefetch_related('access_rights'), id=pack_id)

        user_rights = set(get_user_active_access_rights(user))
        pack_rights = set(pack.access_rights.all())

        if not user_rights & pack_rights:
            return Response({'error': 'Access denied'},
                            status=status.HTTP_403_FORBIDDEN)

        solved_pack, created = SolvedPacks.objects.get_or_create(
            user=user,
            pack=pack,
            defaults={'percent': solved_percent}
        )

        if not created:
            solved_pack.percent = solved_percent
            solved_pack.save()

        return Response({"message": "Процент решенных задач сохранен."},
                        status=status.HTTP_200_OK)


class TaskAnswerAPI(APIView):
    def get(self, request):
        pack_id = request.GET.get('pack_id')
        if pack_id:
            try:
                tasks_data = Task.objects.filter(
                    pack_id=pack_id).values('id', 'answer')
                return Response({'tasks_data': list(tasks_data)},
                                status=status.HTTP_200_OK)

            except Pack.DoesNotExist:
                return Response({'error': 'Pack not found'},
                                status=status.HTTP_404_NOT_FOUND)

        return Response({'error': 'pack_id is required'},
                        status=status.HTTP_400_BAD_REQUEST)


class SubsectionAPI(APIView):
    def get(self, requset):
        if requset:
            section_id = requset.GET.get('section_id')
            subsections = Subsection.objects.filter(
                section_id=section_id).values('id', 'name')
            subsections_data = list(subsections)
            return Response(subsections_data)


class LessonsAPIView(APIView):
    def get(self, request):
        user = request.user
        user_rights = set(get_user_active_access_rights(user))

        lessons = Lesson.objects.filter(is_published=True).prefetch_related(
            'access_rights').order_by('-upload_date')
        accessible_lessons = [lesson for lesson in lessons if set(
            lesson.access_rights.all()) & user_rights]

        serializer = LessonsSerializer(
            accessible_lessons, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class LessonDetailAPIView(APIView):
    def get(self, request):
        lesson_id = request.GET.get("lesson_id")

        if not lesson_id:
            return Response({"error": "lesson_id is required"}, status=400)

        lesson = get_object_or_404(
            Lesson.objects.prefetch_related('access_rights'), id=lesson_id)

        user_rights = set(get_user_active_access_rights(request.user))
        lesson_rights = set(lesson.access_rights.all())

        if not user_rights & lesson_rights:
            return Response({"error": "Access denied"}, status=403)

        data = {
            "title": lesson.title,
            "video_url": lesson.video.file_url if lesson.video else None,
            "video_id": lesson.video.pk if lesson.video else None,
            "practice_url": lesson.practice.url if lesson.practice else None,
            "theory_url": lesson.theory.url if lesson.theory else None,
            "pack": lesson.pack.id if lesson.pack else None,
            "exam": lesson.exam.id if lesson.exam else None,
        }

        return Response(data, status=status.HTTP_200_OK)


class UserLessonProgressView(APIView):
    def post(self, request):
        user = request.user
        lesson_id = request.data.get('lesson')
        field = request.data.get('field')
        value = request.data.get('value')

        if not lesson_id or not field or value is None:
            return Response({'error': 'Некорректные данные'},
                            status=status.HTTP_400_BAD_REQUEST)

        lesson = get_object_or_404(
            Lesson.objects.prefetch_related('access_rights'), pk=lesson_id)
        user_rights = set(get_user_active_access_rights(user))
        lesson_rights = set(lesson.access_rights.all())

        if not user_rights & lesson_rights:
            return Response({"error": "Access denied"}, status=status.HTTP_403_FORBIDDEN)

        progress, created = UserLessonProgress.objects.update_or_create(
            user=user,
            lesson=lesson,
            defaults={field: value}
        )

        return Response({'status': 'success'}, status=status.HTTP_200_OK)


def lesson(request):
    if not request.user.is_authenticated:
        return render(request, 'lesson.html', {'access_rights': []})
    user_access = get_user_active_access_rights(request.user)
    access_rights = [ar.name for ar in user_access]
    return render(request, 'lesson.html', {'access_rights': access_rights})


def landing(request):
    return render(request, 'landing.html')


def home(request):
    if not request.user.is_authenticated:
        return render(request, 'home.html', {'access_rights': []})

    user_access = get_user_active_access_rights(request.user)
    access_rights = [ar.name for ar in user_access]
    return render(request, 'home.html', {
        'access_rights': access_rights,
    })


def test(request):
    context = {
        "user_is_authenticated": request.user.is_authenticated,
    }
    return render(request, 'test.html', context)


def test_creation_page(request):
    sections = Section.objects.all()
    subsections = Subsection.objects.all()
    return render(request, 'testcreation.html',
                  {'sections': sections, 'subsections': subsections})

class CorrectTaskAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        pack_id = request.query_params.get('pack_id')

        if not pack_id:
            return Response({"error": "pack_id not provided"},
                            status=status.HTTP_400_BAD_REQUEST)

        solved_tasks = SolvedTasks.objects.filter(
            user=user, task__pack_id=pack_id).values_list('task_id', flat=True)

        return Response({"solved_tasks": list(solved_tasks)},
                        status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        task_id = request.data.get('task_id')

        if not task_id:
            return Response({"error": "task_id not provided"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            task = Task.objects.get(pk=task_id)
            solved_task, created = SolvedTasks.objects.get_or_create(
                user=user, task=task)

            if created:
                return Response({"success": "Task marked as solved"},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({"info": "Task already marked as solved"},
                                status=status.HTTP_200_OK)

        except Task.DoesNotExist:
            return Response({"error": "Invalid task_id"},
                            status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        user = request.user
        task_id = request.data.get('task_id')

        if not task_id:
            return Response({"error": "task_id not provided"},
                            status=status.HTTP_400_BAD_REQUEST)

        solved_task = SolvedTasks.objects.filter(
            user=user, task__id=task_id).first()

        if not solved_task:
            return Response({"success": "Task doesn't existed"},
                            status=status.HTTP_204_NO_CONTENT)

        solved_task.delete()
        return Response({"success": "Solved task deleted"},
                        status=status.HTTP_204_NO_CONTENT)
