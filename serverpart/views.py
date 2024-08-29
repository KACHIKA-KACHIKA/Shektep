import json
from django.shortcuts import get_object_or_404, render, redirect
from django.db import IntegrityError
from django.http import JsonResponse
from .models import Section, Task, Subsection, Pack, Test
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# Возвращает тесты
def get_tests(request):
		tests = Test.objects.all()
		test_info_list = []
		for test in tests:
				# Получаем первое задание из теста и определяем его раздел
				first_task = test.tasks.first()
				section_name = first_task.section.name if first_task else "Неопределенный раздел"
				# Собираем информацию о тесте
				test_info = {
						'test_name': test.name,
						'section': section_name,
						'tasks': [task.id for task in test.tasks.all()]
				}
				test_info_list.append(test_info)
		return JsonResponse({'tests': test_info_list})


# Отправляет на страницу с тестом
def test_page(request):
		return render(request, 'test.html')

# Отправляет на страницу с тест
def tests_page(request):
		tests = Test.objects.all()
		return render(request, 'tests.html', {'tests': tests})

# Возвращает список заданий
def get_selected_tasks(request):
		if request.method == 'POST':
				fetchParams = json.loads(request.body)
				task_list = []
				
				if 'test_name' in fetchParams:
						# Если присутствует test_name, используем его для получения заданий по имени теста
						test_name = fetchParams['test_name']
						tasks = Test.objects.get(name=test_name).tasks.all()
				else:
						# Иначе, используем выбранные темы для получения заданий
						all_tasks = Task.objects.none()  # Создаем пустой QuerySet

						if fetchParams:  # Проверка на пустой тест
								for section_id, themes_ids in fetchParams.items():
										if themes_ids:  # Проверяем, выбрана ли хотя бы одна тема для данного раздела
												tasks = Task.objects.filter(theme__id__in=themes_ids, section__id=section_id)
												all_tasks |= tasks  # Добавляем найденные задания к общему QuerySet
										else:  # Если для данного раздела не выбрано ни одной темы, добавляем все задания из этого раздела
												tasks = Task.objects.filter(section__id=section_id)
												all_tasks |= tasks  # Добавляем найденные задания к общему QuerySet

						if not all_tasks:  # Если общий QuerySet пустой, значит ни одна тема не была выбрана
								all_tasks = Task.objects.all()  # Получаем все задания

				for task in tasks:
						section_name = task.section.name if task.section else "Неопределенный раздел"
						task_info = {
								'task_number': task.task_number,
								# 'task_image_url': task.task_image.url.replace('task_images/', 'ort/media/task_images/'),
								# 'solution_image_url': task.solution_image.url.replace('solution_images/', 'ort/media/solution_images/') if task.solution_image else None,
								'task_image_url': task.task_image.url.replace('task_images/', 'task_images/'),
								'solution_image_url': task.solution_image.url.replace('solution_images/', 'solution_images/') if task.solution_image else None,
								'section': section_name,
						}
						task_list.append(task_info)

				return JsonResponse({'tasks': task_list})
		else:
				return JsonResponse({'error': 'Invalid request method'})

# Возвращает ответы на решеные задачи 
def get_correct_answers(request):
		if request.method == 'POST':
				data = json.loads(request.body) # Получаем в запросе массив из ls
				selected_answers = data.get('selectedAnswers', [])
				correct_answers = {}

				for answer in selected_answers: # Получаем правильные ответы на задания
						task_id = answer['task_id']
						task = Task.objects.filter(id=task_id).first()
						if task:
								correct_answer = task.answer
								correct_answers[task_id] = correct_answer

				return JsonResponse({'correctAnswers': correct_answers})
		else:
				return JsonResponse({'error': 'Invalid request method'})

# Возвращает разделы и предметы
def test_creation_page(request):
		sections = Section.objects.all()
		subsections = Subsection.objects.all()
		return render(request, 'testcreation.html', {'sections': sections, 'subsections': subsections})

def get_packs(request, subsection_id):
    packs = Pack.objects.filter(subsection_id=subsection_id)
    packs_data = [{'id': pack.id} for pack in packs]
    return JsonResponse(packs_data, safe=False)

def get_tasks_for_pack(request, pack_id):
    # Получаем все задания для выбранного пака
    tasks = Task.objects.filter(pack_id=pack_id)
    pack = Pack.objects.get(id=pack_id)
    subsection = Subsection.objects.filter(id=pack.subsection_id).values('name').first()
    print(subsection)
    # Формируем данные для шаблона
    tasks_data = [
        {
            'id': task.id,
            'task_number': index + 1,  # Номер задания в паке
            'task_image_url': task.task_image.url,  # URL изображения задания
						'subsection': subsection,
        }
        for index, task in enumerate(tasks)
    ]
    
    # Получаем текст из пака (если такой есть)
    pack_text = Pack.objects.filter(id=pack_id).values('text_field').first()
    
    # Передаем данные в шаблон для рендеринга
    return render(request, 'test.html', { 'pack_text': pack_text, 'tasks_data': tasks_data })

# def get_tasks_for_pack(request, pack_id):
#     tasks = Task.objects.filter(pack_id=pack_id)
#     tasks_data = [{'id': task.id} for task in tasks]
#     pack_text = Pack.objects.filter(id=pack_id).values('text_field').first()
#     return render(request, 'test.html', { 'pack_text': pack_text, 'tasks_data': tasks_data})
    # return JsonResponse({'tasks': tasks_data})

# Возвращает предметы в зависимости от раздела
def get_subsections(request, section_id):
		if request.method == 'POST':
				subsections = Subsection.objects.filter(section_id=section_id).values('id', 'name')
				subsections_data = list(subsections)
				return JsonResponse(subsections_data, safe=False)
		else:
				return JsonResponse({'error': 'Invalid request method'})

def signupuser(request):
	if request.method == 'GET':
			return render(request, './signup.html', {'form': UserCreationForm()})
	else:
			if request.POST['password1'] == request.POST['password2']: 
					try:
							_user = User.objects.create_user(request.POST['username'],password=request.POST['password2'])
							_user.save()
							login(request, _user)
							return redirect('home')
					except IntegrityError:
							return render(request, './signup.html', {'form': UserCreationForm(), 'error': 'That username has already been taken. Please choose a new username'})

			else:
					return render(request, './signup.html', {'form': UserCreationForm(), 'error': 'Passwords did not match'})

def logoutuser(request):
		if request.method == 'POST':
				logout(request)
				return redirect('home')

def loginuser(request):
		if request.method == 'GET':
				return render(request, './login.html',{'form': AuthenticationForm()})
		else:
				user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
				if user is None:
						return render(request, './login.html', {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
				else:
						login(request, user)
						return redirect('home')