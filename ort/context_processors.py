from django.utils.timezone import now
from user.models import SubscriptionList

def subscription_data(request):
    active_subscription = None
    end_date = None

    if request.user.is_authenticated:
        subscriptions = SubscriptionList.objects.filter(
            user=request.user
        ).select_related('subscription').prefetch_related('subscription__access_rights').order_by('-timestamp')
        print(subscriptions)
        for sub in subscriptions:
            try:
                access_names = {access.name for access in sub.subscription.access_rights.all()}
                print(access_names)
                if 'Подписка' in access_names:
                    start = sub.timestamp
                    end = start + sub.subscription.duration
                    if now() <= end:
                        active_subscription = sub
                        end_date = end.date()
                        break
            except AttributeError:
                continue

    return {
        'active_subscription': active_subscription,
        'end_date': end_date,
        'today': now().date(),
    }
