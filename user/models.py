from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class AccessRight(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()

	def __str__(self):
		return self.name


class Subscription(models.Model):
	type_name = models.CharField(max_length=50)
	duration = models.DurationField()
	price = models.DecimalField(max_digits=6, decimal_places=2)
	access_rights = models.ManyToManyField(AccessRight, blank=True)  # Подписка включает доступы

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