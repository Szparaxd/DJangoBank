# Generated by Django 4.0.1 on 2022-01-14 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_id',
            field=models.IntegerField(default=0),
        ),
    ]
