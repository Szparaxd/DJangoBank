# Generated by Django 4.0.1 on 2022-01-14 23:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bank', '0015_alter_transaction_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccout',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='BankAccout', to=settings.AUTH_USER_MODEL),
        ),
    ]
