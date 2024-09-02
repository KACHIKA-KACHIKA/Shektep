from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.html import mark_safe
import os

class Section(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subsection(models.Model):
    name = models.CharField(max_length=100)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)  # Связь с секцией

    def __str__(self):
        return self.name

class Pack(models.Model):
    text_field = models.TextField()
    subsection = models.ForeignKey(Subsection, on_delete=models.CASCADE)  # Связь с подразделом

    def __str__(self):
        return f"Pack: {self.subsection} № {self.id}"  # Показывать первые 50 символов текста

class Task(models.Model):
    task_image = models.ImageField(upload_to='task_images/')
    
    ANSWER_CHOICES = [
        ('А', 'А'),
        ('Б', 'Б'),
        ('В', 'В'),
        ('Г', 'Г'),
        ('Д', 'Д'),
    ]
    
    answer = models.TextField(choices=ANSWER_CHOICES)
    pack_id = models.ForeignKey(Pack, on_delete=models.CASCADE)  # Связь с Pack

    def __str__(self):
        return f"Task {self.task_image}"
    def task_image_preview(self):
        if self.task_image:
            return mark_safe(f'<img src="{self.task_image.url}" width="376" height="120" />')
        return "(No image)"

    task_image_preview.short_description = "Task Image Preview"

@receiver(pre_delete, sender=Task)
def delete_task_images(sender, instance, **kwargs):
    # Удаление файла задания
    if instance.task_image:
        if os.path.isfile(instance.task_image.path):
            os.remove(instance.task_image.path)
            print("Удалил " + instance.task_image.path)

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
        return f"Пользователь: {self.user.username}, Задание: {self.task.task_number}"

    class Meta:
        verbose_name = 'SolvedTasks'
        verbose_name_plural = verbose_name
