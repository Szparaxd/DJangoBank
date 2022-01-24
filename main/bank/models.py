from os import access
from django.db import models
from datetime import datetime
import requests


from django.db.models.deletion import CASCADE
from django.http import request
from register.models import CustomUser

from .const import WALUTS

# Create your models here.

def get_Curs(waluta):
    if waluta == 'PLN':
        return 1
    url = 'http://api.nbp.pl/api/exchangerates/rates/a/' + waluta + '/'
    response = requests.get(url)
    #print(response.status_code)
    data = response.json()
    print(data)
    currency = data['rates']
    przewalutowane = currency[0]['mid']
    return przewalutowane



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

class Kredyt(models.Model):
    start = models.DateTimeField(default=datetime.now, blank=True)
    kwota = models.FloatField()
    iloscMiesiecy = models.IntegerField()
    konto = models.ForeignKey(BankAccout, on_delete=CASCADE, related_name='bankAcc')
    kosztMiesieczny = models.FloatField()

class CyklicznePrzelewy(models.Model):
    zJakiegoKonta = models.ForeignKey(BankAccout, on_delete=CASCADE, related_name='fromBankAcc')
    ile = models.FloatField()
    naJakieKonto = models.ForeignKey(BankAccout, on_delete=CASCADE, related_name='toBankAcc')

    def execute(self):
        self.zJakiegoKonta.withDrawnBalance(self.ile)
        self.naJakieKonto.addBalance(self.ile)


class transaction(models.Model):
    fromBank = models.ForeignKey(BankAccout, on_delete=CASCADE, related_name="fromBank") 
    toBank = models.ForeignKey(BankAccout, on_delete=CASCADE, related_name="toBank")
    amount = models.FloatField()
    currency = models.CharField(max_length=3)
    description = models.CharField(max_length=200)
    data = models.DateTimeField(default=datetime.now, blank=True)

    def runOperation(self):
        print("#### RUNOPERATION ####")
        print(self.amount)
        print(self.fromBank.balance)
        self.fromBank.withDrawnBalance(self.amount)
        self.fromBank.save()

        print(self.fromBank.waluts)
        if self.fromBank.waluts == 'PLN':
            print("#############################################")
            print(self.toBank.waluts)
            kurs = get_Curs(self.toBank.waluts)
            finishMoney = self.amount/kurs
            self.toBank.addBalance(finishMoney)
            self.currency = 'PLN'
        
        else:
            kursFrom = get_Curs(self.fromBank.waluts)
            kwotaNaPLN = self.amount * kursFrom
            kursTo = get_Curs(self.toBank.waluts)
            finishMoney = kwotaNaPLN*kursTo
            print("kwota przelesu: "+str(float(finishMoney)))
            self.toBank.addBalance(finishMoney)
            self.currency = self.fromBank.waluts

        self.toBank.save()
    
    def __str__(self):
        return str(self.fromBank) + " - " + str(self.amount) + " -> " + str(self.toBank)

    def sendMoney(self):
        pass


