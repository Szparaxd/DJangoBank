# Generated by Django 4.0.1 on 2022-01-12 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccout',
            name='balance',
            field=models.FloatField(),
        ),
    ]