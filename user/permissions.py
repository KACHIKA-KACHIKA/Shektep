from django.utils import timezone
from rest_framework.permissions import BasePermission
from .models import *


class HasAccessToVideo(BasePermission):
    """
    Проверяет, есть ли у пользователя доступ к видео через его активную подписку.
    """
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            required_access = AccessRight.objects.get(name="Доступ к видео")
            active_subscriptions = SubscriptionList.objects.filter(
                user=user,
                timestamp__lte=timezone.now(),
                timestamp__gte=timezone.now() - models.F('subscription__duration')
            )

            for sub in active_subscriptions:
                if required_access in sub.subscription.access_rights.all():
                    return True
        return False
class HasAccessToTestResults(BasePermission):
    """
    Проверяет, есть ли у пользователя доступ к результатам теста через его активную подписку.
    """
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            required_access = AccessRight.objects.get(name="Доступ к результатам")
            active_subscriptions = SubscriptionList.objects.filter(
                user=user,
                timestamp__lte=timezone.now(),
                timestamp__gte=timezone.now() - models.F('subscription__duration')
            )

            for sub in active_subscriptions:
                if required_access in sub.subscription.access_rights.all():
                    return True
        return False
class HasAccessToExams(BasePermission):
    """
    Проверяет, есть ли у пользователя доступ к экзаменам через его активную подписку.
    """
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            required_access = AccessRight.objects.get(name="Доступ к экзаменам")
            active_subscriptions = SubscriptionList.objects.filter(
                user=user,
                timestamp__lte=timezone.now(),
                timestamp__gte=timezone.now() - models.F('subscription__duration')
            )

            for sub in active_subscriptions:
                if required_access in sub.subscription.access_rights.all():
                    return True
        return False

