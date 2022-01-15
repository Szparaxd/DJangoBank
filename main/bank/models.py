from django.db import models
from datetime import datetime


from django.db.models.deletion import CASCADE
from register.models import CustomUser

from .const import WALUTS

# Create your models here.


class BankAccout(models.Model):
    accNumber = models.IntegerField()
    balance = models.FloatField()
    user = models.ForeignKey(CustomUser, on_delete=CASCADE, related_name='BankAccout')
    accName = models.CharField(max_length=50)
    waluts = models.CharField(max_length=3 ,choices=WALUTS, default='PL')

    
    def __str__(self):
        return str(self.accNumber)
    def __unicode__(self):
        return '%d: %s' %(self.accNumber, self.waluts)
    
    def addBalance(self,money):
        self.balance += money

    def withDrawnBalance(self,moeny):
        self.balance -= moeny
    
    class Meta:
        default_related_name = 'bankAccount'



    def returnParams(self):
        dict = {
            'accNumber':self.accNumber,
            'balance':self.balance,
            'user':self.user.id,
            'accName':self.accName,
            'waluts':self.waluts,
        }
        return dict

class transaction(models.Model):
    fromBank = models.ForeignKey(BankAccout, on_delete=CASCADE, related_name="fromBank") 
    toBank = models.ForeignKey(BankAccout, on_delete=CASCADE, related_name="toBank")
    amount = models.FloatField()
    description = models.CharField(max_length=200)
    data = models.DateTimeField(default=datetime.now, blank=True)

    def runOperation(self):
        print("#### RUNOPERATION ####")
        print(self.amount)
        print(self.fromBank.balance)
        self.fromBank.withDrawnBalance(self.amount)
        self.fromBank.save()

        print(self.fromBank.balance)
        self.toBank.addBalance(self.amount)
        self.toBank.save()
    
    def __str__(self):
        return str(self.fromBank) + " - " + str(self.amount) + " -> " + str(self.toBank)
