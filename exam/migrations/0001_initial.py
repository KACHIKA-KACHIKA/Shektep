# Generated by Django 4.2.5 on 2024-09-17 17:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('serverpart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Difficulty',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('goal_math_1', models.PositiveIntegerField(default=0)),
                ('goal_math_2', models.PositiveIntegerField(default=0)),
                ('goal_analogy', models.PositiveIntegerField(default=0)),
                ('goal_addition', models.PositiveIntegerField(default=0)),
                ('goal_reading', models.PositiveIntegerField(default=0)),
                ('goal_practical_rus', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('is_published', models.BooleanField(default=False)),
                ('difficulty', models.ForeignKey(blank=True, null=True,
                 on_delete=django.db.models.deletion.SET_NULL, to='exam.difficulty')),
                ('fk_addition', models.ForeignKey(null=True,
                                                  on_delete=django.db.models.deletion.SET_NULL,
                 related_name='addition', to='serverpart.pack')),
                ('fk_analogy', models.ForeignKey(null=True,
                                                 on_delete=django.db.models.deletion.SET_NULL,
                 related_name='analogy', to='serverpart.pack')),
                ('fk_math_1', models.ForeignKey(null=True,
                                                on_delete=django.db.models.deletion.SET_NULL,
                 related_name='math_1', to='serverpart.pack')),
                ('fk_math_2', models.ForeignKey(null=True,
                                                on_delete=django.db.models.deletion.SET_NULL,
                 related_name='math_2', to='serverpart.pack')),
                ('fk_practical_rus', models.ForeignKey(null=True,
                                                       on_delete=django.db.models.deletion.SET_NULL,
                 related_name='practical_rus', to='serverpart.pack')),
            ],
        ),
        migrations.CreateModel(
            name='SolvedExam',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('exam', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='exam.exam')),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReadingBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('fk_reading_1', models.ForeignKey(blank=True, null=True,
                 on_delete=django.db.models.deletion.SET_NULL, related_name='reading_1', to='serverpart.pack')),
                ('fk_reading_2', models.ForeignKey(blank=True, null=True,
                 on_delete=django.db.models.deletion.SET_NULL, related_name='reading_2', to='serverpart.pack')),
                ('fk_reading_3', models.ForeignKey(blank=True, null=True,
                 on_delete=django.db.models.deletion.SET_NULL, related_name='reading_3', to='serverpart.pack')),
            ],
        ),
        migrations.AddField(
            model_name='exam',
            name='fk_reading',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='reading_block', to='exam.readingblock'),
        ),
    ]
