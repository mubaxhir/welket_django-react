# Generated by Django 3.0.7 on 2021-01-25 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0031_auto_20210124_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='shared_post_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
