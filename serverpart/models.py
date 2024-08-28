from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os
class Section(models.Model):
		name = models.CharField(max_length=100)
		def __str__(self):
				return self.name

class Subsection(models.Model):
		name = models.CharField(max_length=100)
		def __str__(self):
				return self.name

class Theme(models.Model):
		name = models.CharField(max_length=255)
		subsection = models.ForeignKey(Subsection, on_delete=models.CASCADE)
		def __str__(self):
				return self.name

class Task(models.Model):
		task_number = models.IntegerField(unique=True, editable=False)
		task_image = models.ImageField(upload_to='task_images/')
		solution_image = models.ImageField(upload_to='solution_images/', blank=True)
		ANSWER_CHOICES = [
				('А', 'А'),
				('Б', 'Б'),
				('В', 'В'),
				('Г', 'Г'),
				('Д', 'Д'),
		]
		section = models.ForeignKey(Section, on_delete=models.CASCADE)
		subsection = models.ForeignKey(Subsection, on_delete=models.CASCADE)
		theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
		answer = models.TextField(choices=ANSWER_CHOICES)
		

		def __str__(self):
				return f"Task {self.task_number}"
		def save(self, *args, **kwargs):
				existing_tasks_count = Task.objects.count()
				new_task_number = existing_tasks_count + 1
				while Task.objects.filter(task_number=new_task_number).exists():
						new_task_number += 1
				self.task_number = new_task_number
				super().save(*args, **kwargs)
@receiver(pre_delete, sender=Task)
def delete_task_images(sender, instance, **kwargs):
		# Удаление файла задания
		if instance.task_image:
				if os.path.isfile(instance.task_image.path):
						os.remove(instance.task_image.path)
						print("Удалил" + instance.task_image.path)
		# Удаление файла решения (если есть)
		if instance.solution_image:
				if os.path.isfile(instance.solution_image.path):
						os.remove(instance.solution_image.path)
						print("Удалил" + instance.solution_image.path)

class Test(models.Model):
		test_number = models.IntegerField(unique=True, editable=False)
		name = models.CharField(max_length=100)
		tasks = models.ManyToManyField(Task)
		def save(self, *args, **kwargs):
				existing_tests_count = Test.objects.count()
				new_test_number = existing_tests_count + 1
				while Test.objects.filter(test_number=new_test_number).exists():
						new_test_number += 1
				self.test_number = new_test_number
				super().save(*args, **kwargs)
		def __str__(self):
				return f"Тест {self.test_number}: {self.name}"

class SolvedTasks(models.Model):
		user = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с пользователем
		task = models.ForeignKey(Task, on_delete=models.CASCADE)  # Связь с заданием

		def __str__(self):
				return f"Пользователь: {self.user.username}, Задание: {self.task.topic} ({self.task.get_part_display()})"
		class Meta:
				verbose_name = 'SolvedTasks'
				verbose_name_plural = verbose_name