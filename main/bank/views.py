from audioop import reverse
from urllib import request
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
import bank

from register.models import CustomUser
from .models import BankAccout, transaction
from .forms import CreateBankAccForm,TransactionForm
from .scripts import create_new_ref_number
# Create your views here.


def welcome(request):
    return render(request, 'bank/welcome.html', {})

def info(request):
    if request.user.is_authenticated:
        user2 = request.user
        if BankAccout.objects.filter(user = user2):
            bankAcc = BankAccout.objects.filter(user = user2)
            return render(request, 'bank/info.html',{"bankAcc":bankAcc})
        return HttpResponseRedirect("/createBankAcc")
    else:
        print("Niezalogowany")
        return HttpResponseRedirect("/")

def createBankAcc(request):
    #Todo nie wpuszczaj jeśli nie zalogowany!!!!
    if not request.user.is_authenticated:
        print("Niezalogowany")
        return HttpResponseRedirect("/")

    if request.method == "POST":
        print("CreateBankACC / POST")
        form = CreateBankAccForm(request.POST)
        if form.is_valid():
            balance = 1000 #ToDo zmienić żeby było domyślnie 0
            user = request.user
            waluts = form.cleaned_data["waluts"]
            accName = form.cleaned_data["accName"]
            print(str(balance) + str(user) + str(waluts))
            obj = BankAccout(accName = accName,balance=balance, user=user, waluts=waluts, accNumber=create_new_ref_number())
            obj.save()
            return HttpResponseRedirect("/info")
    else:
        form = CreateBankAccForm()
        return render(request, 'bank/form.html', {"form":form})


def przelew(request):
    print(request.POST)

    if 'accNumber' in request.POST: #Sprawdzam czy formularz idzie z /info 
        print("TEST -> IF")
        dist = {"fromBank" : request.POST['accNumber']}
        form = TransactionForm(dist)
        
    else:
        print("TEST -> ELSE")
        print(request.POST)
        form = TransactionForm(request.POST)
        if form.is_valid():
            fToBank = BankAccout.objects.get(accNumber = form.cleaned_data["toBank"])
            fFromBank = BankAccout.objects.get(accNumber = form.cleaned_data["fromBank"])
            famount = form.cleaned_data["amount"]
            fdescription = form.cleaned_data["description"]

            obj = transaction(fromBank=fFromBank, toBank=fToBank, amount=famount, description=fdescription)
            obj.runOperation()
            obj.save()
            return HttpResponseRedirect('/info')

    form.fields['fromBank'].widget.attrs['readonly'] = True
    return render(request,'bank/przelew.html', {"form":form})


def choice(response):
    print("CHOICE?>>???????????")
    if response.method == 'POST':
        przelew = response.POST.get('przelew')
        historia = response.POST.get('historia')

        bakAcc = BankAccout.objects.get(pk=1)

        print(response.POST)
        if przelew:
            return HttpResponseRedirect(reverse(viewname=przelew,kwargs=response.POST))
        elif historia:
            return HttpResponseRedirect('/historia')

    return HttpResponseRedirect('/info')



def historia(response):
    print(response.POST)

    if 'accNumber' in response.POST: #Sprawdzam czy formularz idzie z /info 
        
        accNumber = response.POST['accNumber']
        print("all elements:")
        allElements = transaction.objects.all()
        print(allElements)
        print("------END-----")

        bank = BankAccout.objects.get(accNumber=accNumber)        

        elements1 = transaction.objects.filter(fromBank=bank)
        elements2 = transaction.objects.filter(toBank=bank)
        #elements = elements1 + elements2
        
        listBankow = []

        for i in elements1:
            listBankow.append(i)

        for i in elements2:
            listBankow.append(i)

        listBankow.sort(key=lambda x: x.data)
        listBankow.reverse()

        print("Lista przelewow:")
        print(listBankow)
   
    return render(response,'bank/historia.html', {"listaBankow":listBankow, 'accNumber':bank})

def readMe(response):
    return render(response,'bank/ReadMe.html', {})