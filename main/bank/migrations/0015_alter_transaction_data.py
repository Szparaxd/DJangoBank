# Generated by Django 4.0.1 on 2022-01-13 18:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0014_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='data',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
