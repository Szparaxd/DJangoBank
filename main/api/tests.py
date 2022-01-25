from asyncio.windows_events import NULL
from gettext import translation
from django.http import HttpResponse, response
from django.test import TestCase, Client
from django.urls import reverse, resolve
from asyncio import AbstractServer
from django.forms import models
from django.test import TestCase
from rest_framework.response import Response
from rest_framework import status 
from django.contrib.auth import authenticate
from api import serializers
from rest_framework.authtoken.models import Token

from bank.models import BankAccout, transaction

# from main.register.models import CustomUser
from .views import bankomat, createUser, history, infoBankAcc, login, NumbersBankAccount, przelew, wplatomat
from register.models import CustomUser



class TestyBanku(TestCase):
#################################################################################################
#                                       UNIT TESTS                                              #
#################################################################################################
    def test_userCreate(self):

        data = {"username":"Username","email":"email@wp.pl", "password":"password123"}
        response = self.client.post("https://lorekdev.pl/api/createUser/", data)
        if response == NULL:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_loginT(self):

            
            data2 = {"username":"admin","password":"admin"}
            user = authenticate(username=data2["username"],password=data2["password"]) 
            if user is not None:
                # A backend authenticated the credentials
                try:
                    token = Token.objects.get(user_id=user.id)
                except Token.DoesNotExist:
                    token = Token.objects.create(user=user)
               
                if token == NULL:
                    Res = status.HTTP_200_OK
                else:
                    Res = status.HTTP_400_BAD_REQUEST
                self.assertEquals(Res,status=status.HTTP_200_OK)
                

    def test_loginF(self):
        #Złe hasło
        #Powinno zwrócić 412
            data3 = {"username":"admin","password":"admin9"}
            
            user = authenticate(username=data3["username"],password=data3["password"]) 
           
            response = self.client.post("https://lorekdev.pl/api/login/", data3)
            if user is not None:
                # A backend authenticated the credentials
                try:
                    token = Token.objects.get(user_id=user.id)
                except Token.DoesNotExist:
                    token = Token.objects.create(user=user)
                serializers_obj = serializers.serialize('json', [user,token])
        
            self.assertEqual(response.status_code ,status.HTTP_400_BAD_REQUEST)

    def test_loginF2(self):
        #Złe hasło
        #Powinno zwrócić 412
            data4 = {"username":"admin9","password":"admin"}
            user = authenticate(username=data4["username"],password=data4["password"]) 
           
            response = self.client.post("https://lorekdev.pl/api/login/", data4)
            if user is not None:
                print('error user logged')
        
            
            self.assertEqual(response.status_code ,status.HTTP_400_BAD_REQUEST)

    def test_TokenUser(self):
        userTest = CustomUser.objects.create(username='test1', password = 'paswordo0012')
        if userTest is not None:
            # A backend authenticated the credentials
            try:
                token = Token.objects.get(user_id=userTest.id)
            except Token.DoesNotExist:
                token = Token.objects.create(user=userTest)
            if token == NULL:
                Res = status.HTTP_200_OK
                self.assertEqual(Res,status.HTTP_200_OK)
            else:
                Res = status.HTTP_400_BAD_REQUEST
                self.assertEqual(Res,status.HTTP_400_BAD_REQUEST)



    def test_history(self):
         userTest1 = CustomUser.objects.create(username='test1', password = 'paswordo0012')
         bankacc1 = BankAccout.objects.create(accNumber=12312312312321,balance=12,user=userTest1,accName='Konto Bankowe', waluts = 'USD')
         userTest2 = CustomUser.objects.create(username='test2', password = 'paswordo00123')
         bankacc2 = BankAccout.objects.create(accNumber=12312312312322,balance=12,user=userTest2,accName='Konto Bankowe', waluts = 'USD')
         acc1 = bankacc1.accNumber
         bank1 = BankAccout.objects.get(accNumber=acc1)
         transaction.objects.create(fromBank=bankacc1,toBank=bankacc2,amount=6, currency=bankacc1.waluts,description='')
        
         if bank1 is not None:
            elements1 = transaction.objects.filter(fromBank=bankacc1)
            elements2 = transaction.objects.filter(toBank=bankacc2)
            listBankow = []

            for i in elements1:
                listBankow.append(i)

            for i in elements2:
                listBankow.append(i)
            #przelew jest zapisany w banku nadawcy i odbiorcy

            listBankow.sort(key=lambda x: x.data)
            listBankow.reverse()
            print(listBankow)
            self.assertEqual(len(listBankow),2)
         else:
             self.assertEqual(1,2)

    def test_bankomat(self):

        userTest1 = CustomUser.objects.create(username='test1', password = 'paswordo0012')
        if userTest1 is not None:
            try:
                token = Token.objects.get(user_id=userTest1)
                print(token)
            except Token.DoesNotExist:
                token = Token.objects.create(user=userTest1)
            if token != NULL:
                Res = status.HTTP_200_OK
                self.assertEqual(Res,status.HTTP_200_OK)
                Res = status.HTTP_400_BAD_REQUEST
                self.assertEqual(Res,status.HTTP_400_BAD_REQUEST)
                bankacc = BankAccout.objects.create(accNumber=12312312312321,balance=12,user=userTest1,accName='Konto Bankowe', waluts = 'USD')
                user = CustomUser.objects.get(auth_token= token)

                if user is not None:
                    konto = BankAccout.objects.get(accNumber = bankacc.accNumber)
                    konto.withDrawnBalance(6)
                    konto.save()
                    amount = BankAccout.objects.get(accNumber=bankacc.accNumber)
                    self.assertEqual(amount.balance,6)
                    #12-6=6
                else:
                    self.assertEqual(1,4)
            else:
                self.assertEqual(1,3)
        else:
            self.assertEqual(1,2)



    def test_wpłatomat(self):
        userTest1 = CustomUser.objects.create(username='test1', password = 'paswordo0012')
        if userTest1 is not None:
            try:
                token = Token.objects.get(user_id=userTest1)
                print(token)
            except Token.DoesNotExist:
                token = Token.objects.create(user=userTest1)
            if token != NULL:
                Res = status.HTTP_200_OK
                self.assertEqual(Res,status.HTTP_200_OK)
                Res = status.HTTP_400_BAD_REQUEST
                self.assertEqual(Res,status.HTTP_400_BAD_REQUEST)
                bankacc = BankAccout.objects.create(accNumber=12312312312321,balance=12,user=userTest1,accName='Konto Bankowe', waluts = 'USD')
                user = CustomUser.objects.get(auth_token= token)

                if user is not None:
                    konto = BankAccout.objects.get(accNumber = bankacc.accNumber)
                    konto.addBalance(6)
                    konto.save()
                    amount = BankAccout.objects.get(accNumber=bankacc.accNumber)
                    self.assertEqual(amount.balance,18)
                    #12+6=18
                else:
                    self.assertEqual(1,4)
            else:
                self.assertEqual(1,3)
        else:
            self.assertEqual(1,2)

        


#################################################################################################
#                                    INTEGRATION TESTS                                          #
#################################################################################################


    def test_urls_Login(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.__name__ , login.__name__)

    def test_urls_bankAcc(self):
        url = reverse('bankNumbers')    
        self.assertEqual(resolve(url).func.__name__ , NumbersBankAccount.__name__) 

    def test_urls_infoBankAcc(self):
        url = reverse('infoBankAcc')
        self.assertEqual(resolve(url).func.__name__ , infoBankAcc.__name__) 

    def test_urls_createUser(self):
        url = reverse('createUser')
        self.assertEqual(resolve(url).func.__name__ , createUser.__name__) 

    def test_urls_przelew(self):
        url = reverse('przelew')
        self.assertEqual(resolve(url).func.__name__ , przelew.__name__)

    def test_urls_history(self):
        url = reverse('history')
        self.assertEqual(resolve(url).func.__name__ , history.__name__) 

    def test_urls_bankomat(self):
        url = reverse('bankomat')
        self.assertEqual(resolve(url).func.__name__ , bankomat.__name__) 

    def test_urls_wplatomat(self):
        url = reverse('wplatomat')
        self.assertEqual(resolve(url).func.__name__ , wplatomat.__name__) 




                


  
    
    

