# Generated by Django 4.0.1 on 2022-01-12 19:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0005_alter_bankaccout_account_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankaccout',
            name='id',
        ),
        migrations.AlterField(
            model_name='bankaccout',
            name='account_no',
            field=models.PositiveIntegerField(primary_key=True, serialize=False, unique=True, validators=[django.core.validators.MinValueValidator(10000000), django.core.validators.MaxValueValidator(99999999)]),
        ),
    ]