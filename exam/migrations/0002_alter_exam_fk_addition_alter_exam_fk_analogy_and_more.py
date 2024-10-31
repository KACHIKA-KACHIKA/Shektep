# Generated by Django 4.2.5 on 2024-09-18 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('serverpart', '0002_pack_video'),
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='fk_addition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='addition', to='serverpart.pack'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='fk_analogy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='analogy', to='serverpart.pack'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='fk_math_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='math_1', to='serverpart.pack'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='fk_math_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='math_2', to='serverpart.pack'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='fk_practical_rus',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='practical_rus', to='serverpart.pack'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='fk_reading',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reading_block', to='exam.readingblock'),
        ),
    ]