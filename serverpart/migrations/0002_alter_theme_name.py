# Generated by Django 4.2.5 on 2024-02-13 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serverpart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
