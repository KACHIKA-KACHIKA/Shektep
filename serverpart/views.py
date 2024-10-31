from django.shortcuts import get_object_or_404, render

from user.models import SubscriptionList
from .models import Section, Task, Subsection, Pack, SolvedTasks, SolvedPacks

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from user.permissions import HasAccessToTestResults


class TaskAPI(APIView):
	def get(self, request):
		pack_id = request.GET.get('pack_id')
		if pack_id:
			try:
				pack = Pack.objects.get(id=pack_id)
				tasks = Task.objects.filter(pack_id=pack_id)
				subsection = Subsection.objects.filter(id=pack.subsection_id).values('name').first()
				tasks_data = [
					{
						'id': task.id,
						'task_answer': task.answer,  # Номер задания в паке
						'task_image_url': task.task_image.url,  # URL изображения задания
						'subsection': subsection['name'] if subsection else None,
					}
					for index, task in enumerate(tasks)
				]
				pack_text = Pack.objects.filter(id=pack_id).values('text_field').first()
				return Response({
					'pack_text': pack_text['text_field'] if pack_text else '',
					'tasks_data': tasks_data
				}, status=status.HTTP_200_OK)

			except Pack.DoesNotExist:
				return Response({'error': 'Pack not found'}, status=status.HTTP_404_NOT_FOUND)

		return Response({'error': 'pack_id is required'}, status=status.HTTP_400_BAD_REQUEST)

class PackAPI(APIView):
	def get(self, request):
		subsection_id = request.GET.get('subsection_id')
		user = request.user

		packs_data = Pack.objects.filter(subsection_id=subsection_id, is_published=True).values('id')

		if HasAccessToTestResults().has_permission(request, self):
			solved_packs = SolvedPacks.objects.filter(user=user, pack__in=[pack['id'] for pack in packs_data])
			solved_dict = {solved.pack_id: solved.percent for solved in solved_packs}
			for pack in packs_data:
				pack['solved_percent'] = solved_dict.get(pack['id'], 0)
		else:
			for pack in packs_data:
				pack['solved_percent'] = 0
		
		return Response(list(packs_data))

class SolvePackAPI(APIView):
	permission_classes = [HasAccessToTestResults]

	def post(self, request):
		user = request.user
		pack_id = request.data.get('pack_id')
		solved_percent = request.data.get('solved_percent')

		if not pack_id or solved_percent is None:
			return Response({"error": "Необходимо указать pack_id и solved_percent."}, status=status.HTTP_400_BAD_REQUEST)

		pack = get_object_or_404(Pack, id=pack_id)

		solved_pack, created = SolvedPacks.objects.get_or_create(
			user=user,
			pack=pack,
			defaults={'percent': solved_percent}
		)

		if not created:
			solved_pack.percent = solved_percent
			solved_pack.save()

		return Response({"message": "Процент решенных задач успешно сохранен."}, status=status.HTTP_200_OK)

class TaskAnswerAPI(APIView):
	def get(self, request):
		pack_id = request.GET.get('pack_id')
		if pack_id:
			try:
				tasks_data = Task.objects.filter(pack_id=pack_id).values('id', 'answer')
				return Response({'tasks_data': list(tasks_data)}, status=status.HTTP_200_OK)

			except Pack.DoesNotExist:
				return Response({'error': 'Pack not found'}, status=status.HTTP_404_NOT_FOUND)

		return Response({'error': 'pack_id is required'}, status=status.HTTP_400_BAD_REQUEST)

class SubsectionAPI(APIView):
	def get(self, requset):
		if requset:
			section_id = requset.GET.get('section_id')
			subsections = Subsection.objects.filter(section_id=section_id).values('id', 'name')
			subsections_data = list(subsections)
			return Response(subsections_data)


def home(request):
	return render(request, 'home.html')
# def home(request):
# 	active_subscription = None
# 	end_date = None

# 	if request.user.is_authenticated:
# 			# Найти самую последнюю подписку
# 			active_subscription = SubscriptionList.objects.filter(user=request.user).order_by('-timestamp').first()

# 			# Вычисляем дату окончания подписки, если она активна
# 			if active_subscription:
# 					start_date = active_subscription.timestamp
# 					end_date = start_date + active_subscription.subscription.duration

# 	context = {
# 			'active_subscription': active_subscription,
# 			'end_date': end_date,
# 	}
# 	return render(request, 'home.html', context)

def test(request):
	return render(request, 'test.html')

def test_creation_page(request):
	sections = Section.objects.all()
	subsections = Subsection.objects.all()
	return render(request, 'testcreation.html', {'sections': sections, 'subsections': subsections})


#Don't use
class CorrectTaskAPI(APIView):
	permission_classes = [HasAccessToTestResults]

	def post(self, request):
		user = request.user
		task_id = request.data.get('task_id')

		if not task_id:
			return Response({"error": "task_id not provided"}, status=status.HTTP_400_BAD_REQUEST)

		try:
			task = Task.objects.get(pk=task_id)
			solved_task, created = SolvedTasks.objects.get_or_create(user=user, task=task)
			
			if created:
				return Response({"success": "Task marked as solved"}, status=status.HTTP_201_CREATED)
			else:
				return Response({"info": "Task already marked as solved"}, status=status.HTTP_200_OK)

		except Task.DoesNotExist:
			return Response({"error": "Invalid task_id"}, status=status.HTTP_404_NOT_FOUND)

		except Exception as e:
			return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def delete(self, request):
		user = request.user
		task_id = request.data.get('task_id')

		if not task_id:
			return Response({"error": "task_id not provided"}, status=status.HTTP_400_BAD_REQUEST)

		solved_task = SolvedTasks.objects.filter(user=user, task__id=task_id).first()

		if not solved_task:
			return Response({"success": "Solved task already deleted or never existed"}, status=status.HTTP_204_NO_CONTENT)

		solved_task.delete()
		return Response({"success": "Solved task deleted"}, status=status.HTTP_204_NO_CONTENT)