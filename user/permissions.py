from django.utils import timezone
from rest_framework.permissions import BasePermission
from django.db import models
from .models import AccessRight, SubscriptionList


class HasAccessToBlock(BasePermission):
    access_name = None

    def has_permission(self, request, view):
        if not self.access_name:
            raise ValueError("Необходимо задать access_name для доступа")

        user = request.user
        if user.is_authenticated:
            required_access = AccessRight.objects.filter(
                name=self.access_name).first()
            if not required_access:
                return False

            active_subscriptions = SubscriptionList.objects.filter(
                user=user,
                timestamp__lte=timezone.now(),
                timestamp__gte=timezone.now()
                - models.F('subscription__duration')
            )

            for sub in active_subscriptions:
                if required_access in sub.subscription.access_rights.all():
                    return True
        return False


class HasAccessToVideo(HasAccessToBlock):
    access_name = "Доступ к видео"


class HasAccessToTestResults(HasAccessToBlock):
    access_name = "Доступ к результатам"


class HasAccessToExams(HasAccessToBlock):
    access_name = "Доступ к экзаменам"


class HasAccessToCourse(HasAccessToBlock):
    access_name = "Доступ к курсу"
