# Generated by Django 2.2.4 on 2020-07-31 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0014_auto_20200729_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='advert',
            name='clicks',
            field=models.IntegerField(default=0),
        ),
    ]