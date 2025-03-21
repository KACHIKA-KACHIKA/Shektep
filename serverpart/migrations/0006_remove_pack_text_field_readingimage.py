# Generated by Django 4.2.5 on 2025-01-29 02:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('serverpart', '0005_alter_pack_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pack',
            name='text_field',
        ),
        migrations.CreateModel(
            name='ReadingImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='reading_texts/')),
                ('pack', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reading_images', to='serverpart.pack')),
            ],
        ),
    ]
