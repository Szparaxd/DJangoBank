from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class CustomUser(AbstractUser):
    
    #tu moge dac klucz obcy do konta bankowego 
    #ale wtedy jedno konto do kilku userow

    def __str__(self):
        return self.username

