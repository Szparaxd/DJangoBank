# Generated by Django 4.0.1 on 2022-01-13 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0011_remove_bankaccout_referrence_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccout',
            name='accName',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]
