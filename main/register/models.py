from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class CustomUser(AbstractUser):
    
    user_id = models.IntegerField(default=0)
    #tu moge dac klucz obcy do konta bankowego 
    #ale wtedy jedno konto do kilku userow

    def __str__(self):
        return self.username

