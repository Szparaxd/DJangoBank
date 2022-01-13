import uuid
from django.db import models
import random

from .scripts import create_new_ref_number

from django.db.models.deletion import CASCADE
from django.utils import translation
from register.models import CustomUser

from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    RegexValidator,)

from .const import WALUTS

# Create your models here.


class BankAccout(models.Model):
    accNumber = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance = models.FloatField()
    user = models.ForeignKey(CustomUser, on_delete=CASCADE)
    
    waluts = models.CharField(max_length=3 ,choices=WALUTS, default='PL')

    
    def __str__(self):
        return str(self.accNumber)
