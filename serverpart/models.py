import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.html import mark_safe

from videoplayer.models import Video


class Section(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subsection(models.Model):
    name = models.CharField(max_length=100)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Pack(models.Model):
    subsection = models.ForeignKey(Subsection, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=True)
    # Закоментить перед первой миграцией
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True,
                              blank=True, related_name='pack_video')

    def __str__(self):
        return f"Pack: {self.subsection} № {self.id}"


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
    pack_id = models.ForeignKey(Pack, on_delete=models.CASCADE)

    def __str__(self):
        return f"Task {self.task_image}"

    def task_image_preview(self):
        if self.task_image:
            return mark_safe(
                f'< img src="{self.task_image.url}" \
                width="376" height="120" / >')
        return "(No image)"

    task_image_preview.short_description = "Task Image Preview"


@receiver(pre_delete, sender=Task)
def delete_task_images(sender, instance, **kwargs):
    # Удаление файла задания
    if instance.task_image:
        if os.path.isfile(instance.task_image.path):
            os.remove(instance.task_image.path)
            print("Удалил " + instance.task_image.path)


class ReadingImage(models.Model):
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE,
                             related_name='reading_images',
                             null=True, blank=True)
    image = models.ImageField(upload_to='reading_texts/')


class SolvedTasks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"Пользователь: {self.user.username}, Задание: {self.task.pk}"

    class Meta:
        verbose_name = 'SolvedTasks'
        verbose_name_plural = verbose_name


class SolvedPacks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE)
    percent = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Пользователь {self.user.username} \
                      решил тест {self.pack.pk} на {self.percent}%"

    class Meta:
        verbose_name = 'SolvedPacks'
        verbose_name_plural = verbose_name
