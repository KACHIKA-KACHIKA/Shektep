# Generated by Django 4.2.5 on 2024-03-08 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('serverpart', '0002_alter_theme_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subsection',
            name='section',
        ),
    ]
