from django.utils import timezone
from rest_framework.permissions import BasePermission
from django.db import models
from django.db.models import F
from .models import AccessRight, SubscriptionList

def get_user_active_access_rights(user):
    now = timezone.now()
    return AccessRight.objects.filter(
        subscription__subscriptionlist__user=user,
        subscription__subscriptionlist__timestamp__lte=now,
        subscription__subscriptionlist__timestamp__gte=now - F('subscription__duration')
    ).distinct()
