from datetime import timedelta
from django.utils.timezone import now
from user.models import SubscriptionList


def subscription_data(request):
    active_subscription = None
    end_date = None

    if request.user.is_authenticated:
        subscriptions = SubscriptionList.objects.filter(
            user=request.user).order_by('-timestamp')

        for sub in subscriptions:
            try:
                # Преобразуем duration в timedelta
                duration = timedelta(
                    seconds=sub.subscription.duration.total_seconds())

                # Ищем подписку ровно на 30 дней
                if duration == timedelta(days=30):
                    active_subscription = sub
                    start_date = sub.timestamp
                    end_date = (start_date + duration).date()
                    break  # Берем только первую найденную подписку
            except AttributeError:
                continue  # Если duration не преобразуется, пропускаем

    return {
        'active_subscription': active_subscription,
        'end_date': end_date,
        'today': now().date(),
    }
