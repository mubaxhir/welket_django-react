# Generated by Django 3.0.7 on 2021-01-28 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0032_post_shared_post_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='first_name',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='last_name',
            field=models.TextField(blank=True),
        ),
    ]