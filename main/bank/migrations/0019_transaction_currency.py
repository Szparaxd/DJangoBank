# Generated by Django 4.0.1 on 2022-01-23 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0018_alter_bankaccout_waluts'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='currency',
            field=models.CharField(default=1, max_length=3),
            preserve_default=False,
        ),
    ]
