from user.models import SubscriptionList
from datetime import timedelta

def subscription_data(request):
	active_subscription = None
	end_date = None

	if request.user.is_authenticated:
		active_subscription = SubscriptionList.objects.filter(user=request.user).order_by('-timestamp').first()

		if active_subscription:
			start_date = active_subscription.timestamp
			end_date = start_date + active_subscription.subscription.duration

	return {
		'active_subscription': active_subscription,
		'end_date': end_date,
	}
