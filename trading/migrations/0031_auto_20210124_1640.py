# Generated by Django 3.0.7 on 2021-01-24 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0030_auto_20210124_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharedpost',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trading.Post', verbose_name='Shared Post'),
        ),
    ]