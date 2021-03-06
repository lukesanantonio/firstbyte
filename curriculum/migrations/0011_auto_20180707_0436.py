# Generated by Django 2.0.6 on 2018-07-07 04:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0010_lessonplan_draft'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonfeedback',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lessonplan',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lessonplan',
            name='last_modified_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='lessonresource',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='websitefeedback',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
