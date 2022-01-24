import json
from unittest import result
from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Group
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView

from bank.models import BankAccout, transaction, Kredyt, CyklicznePrzelewy
from .serializers import BankAccountSerializer, UserSerializer, GroupSerializer, CustomUserSerializer
from register.models import CustomUser

from rest_framework.authtoken.models import Token
from bank.scripts import create_new_ref_number

from register.forms import CustomUserCreationForm

import logging, traceback

logger = logging.getLogger('django')



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
 

@api_view(('POST',))
def login(response):
    logger.info('api_view: login')
    logger.info(response.POST)

    if(response.method == 'POST'):  
        username = response.POST.get("username")
        password = response.POST.get("password")
        user = authenticate(username=username,password=password)       
    
        if user is not None:
            
            # A backend authenticated the credentials
            try:
                token = Token.objects.get(user_id=user.id)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            
            bankacc = BankAccout.objects.filter(user=user)
           
            xd = serializers.serialize('json', BankAccout.objects.filter(user=user))
            serializers_obj = serializers.serialize('json', [user,token])
            
            return HttpResponse(serializers_obj,status=status.HTTP_200_OK)

    errorMess = {'error':'Niepoprawne dane lub taki uzytkownik nie istnieje'}        
    return Response(errorMess,status=status.HTTP_400_BAD_REQUEST)

@api_view(('POST',))
def NumbersBankAccount(response):
    logger.info('api_view: NumbersBankAccount')
    logger.info(response.POST)

    if(response.method == 'POST'):
        tokenKey = response.POST['token']
        token = Token.objects.get(key = tokenKey )
        user = token.user
        listBankAccoutn = BankAccout.objects.filter(user=user)     
        serializers_obj = serializers.serialize('json', listBankAccoutn)
        return HttpResponse(serializers_obj,status=status.HTTP_200_OK)

    errorMess = {'error':'Nie znaleziono użytkownika z takim tokenem'}
    return Response(errorMess,status=status.HTTP_400_BAD_REQUEST)


@api_view(('POST',))
def infoBankAcc(response):
    logger.info('api_view: infoBankAcc')
    logger.info(response.POST)

    if(response.method == 'POST'):
        bankNumber = response.POST['bankNumber']
        token = response.POST['token']
        try:
            bankAcc = BankAccout.objects.get(accNumber = bankNumber)
            acc = CustomUser.objects.get(auth_token = token)          
            if bankAcc.user == acc:               
                result = bankAcc.returnParams()
                return Response(result,status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)        
        except:
            logger.fatal("Except")
            return Response(status=status.HTTP_404_NOT_FOUND)

    errorMess = {'error':'Nie znaleziono użytkownika z takim tokenem'}
    return Response(errorMess,status=status.HTTP_400_BAD_REQUEST)


@api_view(('POST',))
def createUser(response):
    logger.info('api_view: createUser')
    logger.info(response.POST)

    if(response.method == 'POST'):
        username = response.POST.get('username')
        email = response.POST.get('email')
        password = response.POST.get('password')

        obj = User.objects.create_user(username=username, password=password)
        obj.save()
        return Response(status=status.HTTP_200_OK)

    errorMess = {'error':'Nie mozna stworzyc uzytkownika o podanych parametrach'}
    return Response(errorMess,status=status.HTTP_400_BAD_REQUEST)


@api_view(('POST',))
def przelew(response):
    logger.info('api_view: przelew')
    logger.info(response.POST)


    if(response.method == 'POST'):
        fToBank = BankAccout.objects.get(accNumber = response.POST.get("toBank"))
        fFromBank = BankAccout.objects.get(accNumber = response.POST.get("fromBank"))
        famount = float(response.POST.get("amount"))
        fdescription = response.POST.get("description")

        obj = transaction(fromBank=fFromBank, toBank=fToBank, amount=famount, description=fdescription)
        obj.runOperation()
        obj.save()
        return Response(status=status.HTTP_200_OK)
        
    errorMess = {'error':'Nie udalo sie dokonac przelewu'}
    return Response(errorMess,status=status.HTTP_400_BAD_REQUEST)

@api_view(('POST',))
def history(response):
    logger.info('api_view: history')
    logger.info(response.POST)

    accNumber = response.POST.get("accNumber")
    bank = BankAccout.objects.get(accNumber=accNumber)        
    if bank is not None:
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

    errorMess = {'error':'Nie znaleziono konta z takim numerem'}
    return Response(errorMess,status=status.HTTP_400_BAD_REQUEST)

@api_view(('POST',))
def createBankAcc(response):
    logger.info('api_view: createBankAcc')
    logger.info(response.POST)

    balance = 1000 #ToDo zmienić żeby było domyślnie 0
    token = response.POST.get("token")
    user = CustomUser.objects.get(auth_token = token) 

    if user is not None:
        waluts = response.POST.get("waluts")
        accName = response.POST.get("name")
        obj = BankAccout(accName = accName,balance=balance, user=user, waluts=waluts, accNumber=create_new_ref_number())
        obj.save()
        return Response(status=status.HTTP_200_OK)
    
    errorMess = {'error':'Nie znaleziono użytkownika z takim tokenem'}
    return Response(errorMess,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(('POST',))
def przelewyCykliczne(response):
    logger.info('api_view: przelewyCykliczne')
    logger.info(response.POST)

    _ile = response.POST.get("amount")
    _doKonta = response.POST.get("toNumberAcc")
    _zKonta = response.POST.Get("fromNumberAcc")
    _token = response.POST.get("token")

    user = CustomUser.objects.get(auth_token = _token)
    if user is not None:
        fromKonto = BankAccout.objects.get(accNumber = _zKonta)
        toKonto = BankAccout.objects.get(accNumber = _doKonta)

        obj = CyklicznePrzelewy.objects.create(
            zJakiegoKonta = fromKonto,
            ile = _ile,
            naJakieKonto = _doKonta
        )

        obj.save()
        return Response(status=status.HTTP_200_OK)
    
    errorMess = {'error':'Nie znaleziono użytkownika z takim tokenem'}
    return Response(errorMess,status=status.HTTP_400_BAD_REQUEST)


@api_view(('POST',))
def bankomat(response):
    logger.info('api_view: bankomat')
    logger.info(response.POST)

    _token = response.POST.get("token")
    _nrKonta = response.POST.get("numberAcc")
    _amount = response.POST.get("amount")

    user = CustomUser.objects.get(auth_token= _token)

    if user is not None:
        konto = BankAccout.objects.get(accNumber = _nrKonta)
        konto.withDrawnBalance(_amount)
        konto.save()
        return Response(status=status.HTTP_200_OK)

    errorMess = {'error':'Nie znaleziono użytkownika z takim tokenem'}
    return Response(errorMess,status=status.HTTP_400_BAD_REQUEST)


@api_view(('POST',))
def wplatomat(response):
    logger.info('api_view: wplatomat')
    logger.info(response.POST)

    _token = response.POST.get("token")
    _nrKonta = response.POST.get("numberAcc")
    _amount = response.POST.get("amount")

    user = CustomUser.objects.get(auth_token= _token)

    if user is not None:
        konto = BankAccout.objects.get(accNumber = _nrKonta)
        konto.addBalance(_amount)
        konto.save()
        return Response(status=status.HTTP_200_OK)

    errorMess = {'error':'Nie znaleziono użytkownika z takim tokenem'}
    return Response(errorMess,status=status.HTTP_400_BAD_REQUEST)


@api_view(('POST',))
def kredyt(response):
    
    listakredytow = Kredyt.objects.all()
    print(listakredytow)
    logger.info('api_view: kredyt')
    logger.info(response.POST)

    _token = response.POST.get("token")
    _nrKonta = response.POST.get("numberAcc")
    _amount = response.POST.get("amount")
    _iloscMiesiecy = response.POST.get("months")
    _kosztMisieczny = response.POST.get('amountMonth')

    user = CustomUser.objects.get(auth_token= _token)

    if user is not None:
        kontoBankowe= BankAccout.objects.get(accNumber = _nrKonta)
        kredyt = Kredyt(
            kwota=_amount,
            iloscMiesiecy=_iloscMiesiecy,
            konto = kontoBankowe,
            kosztMiesieczny= _kosztMisieczny
            )
        kredyt.save()
        
        kontoBankowe.addBalance(int(_amount))
        kontoBankowe.save()
        return Response(status=status.HTTP_200_OK)
    
    errorMess = {'error':'Nie znaleziono użytkownika z takim tokenem'}
    return Response(errorMess,status=status.HTTP_400_BAD_REQUEST)




        
        
        
    






    




        

        
