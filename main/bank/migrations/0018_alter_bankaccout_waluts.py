# Generated by Django 4.0.1 on 2022-01-23 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0017_alter_bankaccout_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccout',
            name='waluts',
            field=models.CharField(choices=[('PLN', 'PLN'), ('EUR', 'EUR'), ('USD', 'USD')], default='PL', max_length=3),
        ),
    ]