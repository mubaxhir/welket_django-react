# Generated by Django 2.2.4 on 2020-07-08 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0012_auto_20200703_2246'),
        ('users', '0006_auto_20200702_0031'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='friends',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trading.Friend_List'),
        ),
    ]
