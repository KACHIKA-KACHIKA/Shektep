from django.db import models
from django.contrib.auth.models import User
from serverpart.models import Pack

class Exam(models.Model):
	name = models.CharField(max_length=20)
	is_published = models.BooleanField(default=False)
	difficulty = models.ForeignKey('Difficulty', on_delete=models.SET_NULL, null=True, blank=True)
	fk_math_1 = models.ForeignKey(Pack, on_delete=models.SET_NULL, null=True, blank=True, related_name="math_1")
	fk_math_2 = models.ForeignKey(Pack, on_delete=models.SET_NULL, null=True, blank=True, related_name="math_2")
	fk_analogy = models.ForeignKey(Pack, on_delete=models.SET_NULL, null=True, blank=True, related_name="analogy")
	fk_addition = models.ForeignKey(Pack, on_delete=models.SET_NULL, null=True, blank=True, related_name="addition")
	fk_reading = models.ForeignKey('ReadingBlock', on_delete=models.SET_NULL, null=True, blank=True, related_name="reading_block")
	fk_practical_rus = models.ForeignKey(Pack, on_delete=models.SET_NULL, null=True, blank=True, related_name="practical_rus")
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Экзамен {self.name}"

class Difficulty(models.Model):
	name = models.CharField(max_length=20)

	goal_math_1 = models.PositiveIntegerField(default=0)
	goal_math_2 = models.PositiveIntegerField(default=0)
	goal_analogy = models.PositiveIntegerField(default=0)
	goal_addition = models.PositiveIntegerField(default=0)
	goal_reading = models.PositiveIntegerField(default=0)
	goal_practical_rus = models.PositiveIntegerField(default=0)

	def __str__(self):
		return f"{self.name} сложность"

class ReadingBlock(models.Model):
	name = models.CharField(max_length=20)
	fk_reading_1 = models.ForeignKey(Pack, on_delete=models.SET_NULL, blank=True, null=True, related_name="reading_1")
	fk_reading_2 = models.ForeignKey(Pack, on_delete=models.SET_NULL, blank=True, null=True, related_name="reading_2")
	fk_reading_3 = models.ForeignKey(Pack, on_delete=models.SET_NULL, blank=True, null=True, related_name="reading_3")

	def __str__(self):
			return f"Блок из {self.fk_reading_1.pk}, {self.fk_reading_2.pk}, {self.fk_reading_3.pk}"

class SolvedExam(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

	def __str__(self):
			return f"Пользователь: {self.user.username}, Вариант: {self.exam.pk}"