# Generated by Django 4.2.5 on 2024-04-05 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serverpart', '0003_remove_subsection_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='answer',
            field=models.TextField(choices=[('А', 'А'), ('Б', 'Б'), ('В', 'В'), ('Г', 'Г'), ('Д', 'Д')]),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_number',
            field=models.IntegerField(editable=False, unique=True),
        ),
    ]
