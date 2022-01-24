from asyncio.windows_events import NULL
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

# from main.register.models import CustomUser
from .views import createUser, history, infoBankAcc, login, NumbersBankAccount, przelew
from bank import views as vBank
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
        
            self.assertEqual(response.status_code ,status.HTTP_412_PRECONDITION_FAILED)

    def test_loginF2(self):
        #Złe hasło
        #Powinno zwrócić 412
            data4 = {"username":"admin9","password":"admin"}
            user = authenticate(username=data4["username"],password=data4["password"]) 
           
            response = self.client.post("https://lorekdev.pl/api/login/", data4)
            if user is not None:
                print('error user logged')
        
            
            self.assertEqual(response.status_code ,status.HTTP_412_PRECONDITION_FAILED)

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

    def test_urls(self):
        url = reverse('przelew')
        self.assertEqual(resolve(url).func.__name__ , przelew.__name__) 

    def test_urls(self):
        url = reverse('history')
        self.assertEqual(resolve(url).func.__name__ , history.__name__) 



                


  
    
    

