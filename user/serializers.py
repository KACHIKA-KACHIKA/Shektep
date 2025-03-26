from rest_framework import serializers
from .models import Lesson, UserLessonProgress
from serverpart.models import Task, SolvedTasks


class LessonsSerializer(serializers.ModelSerializer):
    upload_date = serializers.DateField(
        format="%d.%m")
    total_tasks = serializers.SerializerMethodField()
    solved_tasks = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'upload_date', 'total_tasks', 'solved_tasks']

    def get_total_tasks(self, obj):
        tasks_from_pack = 0
        if obj.pack:
            tasks_from_pack = Task.objects.filter(pack_id=obj.pack).count()

        tasks_from_exam = 0
        if obj.exam:
            exam_packs = [
                obj.exam.fk_math_1, obj.exam.fk_math_2, obj.exam.fk_analogy,
                obj.exam.fk_addition, obj.exam.fk_practical_rus
            ]
            tasks_from_exam = sum([Task.objects.filter(
                pack_id=pack).count() for pack in exam_packs if pack])

            tasks_from_reading_block = 0
            if obj.exam.fk_reading:
                reading_packs = [
                    obj.exam.fk_reading.fk_reading_1,
                    obj.exam.fk_reading.fk_reading_2,
                    obj.exam.fk_reading.fk_reading_3
                ]
                tasks_from_reading_block = sum([Task.objects.filter(
                    pack_id=pack).count() for pack in reading_packs if pack])
            tasks_from_exam += tasks_from_reading_block

        total_tasks = tasks_from_pack + tasks_from_exam
        if obj.practice:
            total_tasks += 15
        return total_tasks

    def get_solved_tasks(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return 0

        user = request.user
        pack_ids = []
        if obj.pack:
            pack_ids.append(obj.pack)

        if obj.exam:
            exam_packs = [
                obj.exam.fk_math_1, obj.exam.fk_math_2, obj.exam.fk_analogy,
                obj.exam.fk_addition, obj.exam.fk_practical_rus
            ]
            pack_ids.extend(filter(None, exam_packs))

            if obj.exam.fk_reading:
                reading_packs = [
                    obj.exam.fk_reading.fk_reading_1,
                    obj.exam.fk_reading.fk_reading_2,
                    obj.exam.fk_reading.fk_reading_3
                ]
                pack_ids.extend(filter(None, reading_packs))

        solved_tasks = SolvedTasks.objects.filter(
            user=user, task__pack_id__in=pack_ids).count()

        user_progress = UserLessonProgress.objects.filter(
            user=user, lesson=obj).first()
        if user_progress and user_progress.downloaded_practice:
            solved_tasks += 15
        return solved_tasks
