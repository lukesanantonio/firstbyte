# Generated by Django 2.0.5 on 2018-05-31 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0007_auto_20180531_0310'),
    ]

    operations = [
        migrations.AddField(
            model_name='websitefeedback',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]