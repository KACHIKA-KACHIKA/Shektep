from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from user.permissions import HasAccessToExams

class ExamAPI(APIView):
	permission_classes = [HasAccessToExams]

	def get(self, request):
		exam_id = request.GET.get('exam_id')
		if not exam_id:
			return Response({'error': 'exam_id is required'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			exam = Exam.objects.get(id=exam_id)
		except Exam.DoesNotExist:
			return Response({'error': 'Exam not found'}, status=status.HTTP_404_NOT_FOUND)

		exam_data = {
			'id': exam.id,
			'name': exam.name,
			'fk_math_1_id': exam.fk_math_1_id,
			'fk_math_2_id': exam.fk_math_2_id,
			'fk_analogy_id': exam.fk_analogy_id,
			'fk_addition_id': exam.fk_addition_id,
			'fk_reading_id': exam.fk_reading_id,
			'fk_practical_rus_id': exam.fk_practical_rus_id,
			'created_at': exam.created_at,
			}
		return Response(exam_data, status=status.HTTP_200_OK)

class SolvedExamAPI(APIView):
	permission_classes = [HasAccessToExams]

	def get(self, request):
		try:
			exams = SolvedExam.objects.filter(user=request.user)
		except SolvedExam.DoesNotExist:
			return Response({'error': 'Exam not found'}, status=status.HTTP_404_NOT_FOUND)
		
		solved_exams = exams.values_list('exam_id', flat=True)
		return Response({ "solved_exams" : solved_exams}, status=status.HTTP_200_OK)

class CorrectExamAPI(APIView):
	permission_classes = [HasAccessToExams]

	def post(self, request):
		user = request.user
		exam_id = request.data.get('exam_id')

		if not exam_id:
			return Response({"error": "exam_id not provided"}, status=status.HTTP_400_BAD_REQUEST)

		try:
			exam = Exam.objects.get(pk=exam_id)
			solved_exam, created = SolvedExam.objects.get_or_create(user=user, exam=exam)
			
			if created:
				return Response({"success": "Exam marked as solved"}, status=status.HTTP_201_CREATED)
			else:
				return Response({"info": "Exam already marked as solved"}, status=status.HTTP_200_OK)

		except Exam.DoesNotExist:
			return Response({"error": "Invalid exam_id"}, status=status.HTTP_404_NOT_FOUND)

		except Exception as e:
			return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def delete(self, request):
		user = request.user
		exam_id = request.data.get('exam_id')

		if not exam_id:
			return Response({"error": "exam_id not provided"}, status=status.HTTP_400_BAD_REQUEST)

		try:
			solved_exam = SolvedExam.objects.get(user=user, exam__id=exam_id)
			solved_exam.delete()
			return Response({"success": "Solved exam deleted"}, status=status.HTTP_204_NO_CONTENT)

		except SolvedExam.DoesNotExist:
			return Response({"error": "Solved exam not found"}, status=status.HTTP_404_NOT_FOUND)

		except Exception as e:
			return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DifficultyAPI(APIView):
	permission_classes = [HasAccessToExams]

	def get(self, request):
			exam_id = request.GET.get('exam_id')
			if not exam_id:
					return Response({'error': 'exam_id is required'}, status=status.HTTP_400_BAD_REQUEST)

			try:
					difficulty_id = Exam.objects.filter(pk=exam_id).values('difficulty').first()['difficulty']
					exam_difficulty = Difficulty.objects.filter(pk=difficulty_id).values().first()
			except (Exam.DoesNotExist, KeyError, IndexError):
					return Response({'error': 'Difficulty data not found'}, status=status.HTTP_404_NOT_FOUND)

			difficulty_data = {
					"goal_math_1": exam_difficulty['goal_math_1'],
					"goal_math_2": exam_difficulty['goal_math_2'],
					"goal_analogy": exam_difficulty['goal_analogy'],
					"goal_addition": exam_difficulty['goal_addition'],
					"goal_reading": exam_difficulty['goal_reading'],
					"goal_practical_rus": exam_difficulty['goal_practical_rus'],
			}
			return Response({'difficulty_data': difficulty_data}, status=status.HTTP_200_OK)

class ExamsAPI(APIView):
	permission_classes = [HasAccessToExams]

	def get(self, request):
			exams = Exam.objects.filter(is_published=True).values('id', 'difficulty_id', 'name', 'created_at')
			
			if not exams.exists():
					return Response({'error': 'No exams available at the moment'}, status=status.HTTP_404_NOT_FOUND)
			
			if not request.user.has_perm('view_exam'):
					return Response({'error': 'Access denied. Subscription required.'}, status=status.HTTP_403_FORBIDDEN)

			return Response({'exams': exams}, status=status.HTTP_200_OK)
	
def exams(request):
	return render(request, 'exams.html')

def result(request):
	return render(request, 'exam_results.html')

def examing(request):
	return render(request, 'exam.html')

#Don't use
class ReadingBlockAPI(APIView):
	def get(self, request):
		reading_block_id = request.GET.get('reading_block_id')
		reading_block = ReadingBlock.objects.get(id=reading_block_id)
		reading_block_data = {
				'fk_reading_1': reading_block.fk_reading_1.id,
				'fk_reading_2': reading_block.fk_reading_2.id,
				'fk_reading_3': reading_block.fk_reading_3.id
		}
		return Response(reading_block_data, status=status.HTTP_200_OK)
