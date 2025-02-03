from django.db import models
from django.contrib.auth.models import User
from videoplayer.models import Video
from serverpart.models import Pack
from exam.models import Exam


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    is_published = models.BooleanField(default=False)
    video = models.ForeignKey(
        Video, on_delete=models.SET_NULL, null=True, blank=True)
    pack = models.ForeignKey(
        Pack, on_delete=models.SET_NULL, null=True, blank=True)  # Обычный тест
    exam = models.ForeignKey(
        Exam, on_delete=models.SET_NULL, null=True, blank=True)  # Спидран
    practice = models.FileField(upload_to="practices/", null=True, blank=True)
    theory = models.FileField(upload_to="theories/", null=True, blank=True)
    upload_date = models.DateField(null=True, blank=True)  

    def __str__(self):
        return f"Урок {self.title}"

class UserLessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    video_rating = models.PositiveIntegerField(
        null=True, blank=True)  # Оценка видео (например, 1-5)

    downloaded_practice = models.BooleanField(
        default=False)  # Скачал практический материал
    downloaded_theory = models.BooleanField(default=False)  # Скачал теорию


class AccessRight(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Subscription(models.Model):
    type_name = models.CharField(max_length=50)
    duration = models.DurationField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    access_rights = models.ManyToManyField(
        AccessRight, blank=True)  # Подписка включает доступы

    def __str__(self):
        return f"{self.type_name} - {self.price} за {self.duration.days} дней"


class SubscriptionList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def end_date(self):
        return self.timestamp + self.subscription.duration

    def __str__(self):
        return f"{self.user.username} - {self.subscription.type_name}, до {self.end_date}"
