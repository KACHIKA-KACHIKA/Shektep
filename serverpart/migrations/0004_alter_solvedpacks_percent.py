# Generated by Django 4.2.5 on 2024-10-15 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serverpart', '0003_solvedpacks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solvedpacks',
            name='percent',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
