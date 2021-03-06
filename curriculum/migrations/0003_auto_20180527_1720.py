# Generated by Django 2.1a1 on 2018-05-27 17:20

import curriculum.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('curriculum', '0002_auto_20180527_1715'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overall_rating', curriculum.models.FiveStarRatingField(choices=[(1, 'One star'), (2, 'Two stars'), (3, 'Three stars'), (4, 'Four stars'), (5, 'Five stars')])),
                ('strengths', models.TextField(max_length=2500)),
                ('weaknesses', models.TextField(max_length=2500)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WebsiteFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overall_rating', curriculum.models.FiveStarRatingField(choices=[(1, 'One star'), (2, 'Two stars'), (3, 'Three stars'), (4, 'Four stars'), (5, 'Five stars')])),
                ('strengths', models.TextField(max_length=2500)),
                ('weaknesses', models.TextField(max_length=2500)),
            ],
        ),
        migrations.AddField(
            model_name='lessonplan',
            name='feedback_enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='lessonfeedback',
            name='lesson',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='curriculum.LessonPlan'),
        ),
    ]
