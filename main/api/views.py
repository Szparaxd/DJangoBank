import json
from unittest import result
from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Group
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from rest_framework import viewsets, status 
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth.models import User

from bank.models import BankAccout, transaction
from .serializers import BankAccountSerializer, UserSerializer, GroupSerializer, CustomUserSerializer
from register.models import CustomUser

from rest_framework.authtoken.models import Token
from bank.scripts import create_new_ref_number




User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    #permission_classes = [permissions.IsAuthenticated]

class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccout.objects.all()
    serializer_class = BankAccountSerializer


class CustomUserViewSet(viewsets.ViewSet):
    queryset = CustomUser.objects.all()
    serlializer_class = CustomUserSerializer()
 

@api_view(('POST',))
def login(response):

    if(response.method == 'POST'):
      
        username = response.POST.get("username")
        password = response.POST.get("password")
        user = authenticate(username=username,password=password)       
        # print("TEST") tu też
        
        if user is not None:
            
            # A backend authenticated the credentials
            try:
                token = Token.objects.get(user_id=user.id)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            print("TEST")
            
            bankacc = BankAccout.objects.filter(user=user)
            print("TEST po bankach czytaniu")
           
            xd = serializers.serialize('json', BankAccout.objects.filter(user=user))
            serializers_obj = serializers.serialize('json', [user,token])
            
            return HttpResponse(serializers_obj,status=status.HTTP_200_OK)
   
    return Response(status=status.HTTP_412_PRECONDITION_FAILED)

@api_view(('POST',))
def NumbersBankAccount(response):
    if(response.method == 'POST'):
        tokenKey = response.POST['token']
        token = Token.objects.get(key = tokenKey )
        user = token.user
        listBankAccoutn = BankAccout.objects.filter(user=user)     
        serializers_obj = serializers.serialize('json', listBankAccoutn)
        return HttpResponse(serializers_obj,status=status.HTTP_200_OK)
    return HttpResponse(status=status.HTTP_404_NOT_FOUND)


@api_view(('POST',))
def infoBankAcc(response):
    if(response.method == 'POST'):
        bankNumber = response.POST['bankNumber']
        token = response.POST['token']
        try:
            bankAcc = BankAccout.objects.get(accNumber = bankNumber)
            acc = CustomUser.objects.get(auth_token = token)          
            if bankAcc.user == acc:               
                result = bankAcc.returnParams()
                print(result)
                return Response(result,status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)        
        except:
            print("Except")
            return Response(status=status.HTTP_404_NOT_FOUND)     
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(('POST',))
def createUser(response):
    # print("CreateUser")
    # print(response.POST)
    # wykomentowałem bo sraka na testach była
    if(response.method == 'POST'):
        username = response.POST.get('username')
        email = response.POST.get('email')
        password = response.POST.get('password')

        obj = CustomUser.objects.create_user(username=username,
                                                email=email,
                                                password=password)
        obj.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST )


@api_view(('POST',))
def przelew(response):
    print("API: Przelew")
    print(response.POST)
    
    if(response.method == 'POST'):
        fToBank = BankAccout.objects.get(accNumber = response.POST.get("toBank"))
        fFromBank = BankAccout.objects.get(accNumber = response.POST.get("fromBank"))
        famount = float(response.POST.get("amount"))
        fdescription = response.POST.get("description")

        obj = transaction(fromBank=fFromBank, toBank=fToBank, amount=famount, description=fdescription)
        obj.runOperation()
        obj.save()
        return Response(status=status.HTTP_200_OK)
        
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(('POST',))
def history(response):
    print("TEST history ")

    accNumber = response.POST.get("accNumber")
    print(accNumber)
    
    bank = BankAccout.objects.get(accNumber=accNumber)        

    elements1 = transaction.objects.filter(fromBank=bank)
    elements2 = transaction.objects.filter(toBank=bank)
        
    listBankow = []

    for i in elements1:
        listBankow.append(i)

    for i in elements2:
        listBankow.append(i)

    listBankow.sort(key=lambda x: x.data)
    listBankow.reverse()
    serializers_obj = serializers.serialize('json', listBankow)
    return HttpResponse(serializers_obj,status=status.HTTP_200_OK)

@api_view(('POST',))
def createBankAcc(response):
        balance = 1000 #ToDo zmienić żeby było domyślnie 0
        token = response.POST.get("token")
        user = CustomUser.objects.get(auth_token = token) 

        waluts = response.POST.get("waluts")
        accName = response.POST.get("name")
        print(str(balance) + str(user) + str(waluts))
        obj = BankAccout(accName = accName,balance=balance, user=user, waluts=waluts, accNumber=create_new_ref_number())
        obj.save()
        return Response(status=status.HTTP_200_OK)


    


    




        

        
