# Generated by Django 4.0.1 on 2022-01-12 19:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0003_bankaccout_account_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccout',
            name='account_no',
            field=models.PositiveIntegerField(unique=True, validators=[django.core.validators.MinValueValidator(10000000), django.core.validators.MaxValueValidator(99999999)]),
        ),
    ]
