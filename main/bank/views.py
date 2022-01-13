from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from register.models import CustomUser
from .models import BankAccout
from .forms import CreateBankAccForm
# Create your views here.


def welcome(request):
    return render(request, 'bank/welcome.html', {})

def info(request):
    bankAcc = BankAccout.objects.get_queryset()
    print(str(bankAcc))

    return render(request, 'bank/info.html', {"bankAcc":bankAcc})

def createBankAcc(request):

    if request.method == "POST":
        form = CreateBankAccForm(request.POST)
        if form.is_valid():
            balance = 1000
            user = request.user
            waluts = form.cleaned_data["waluts"]
            print(str(balance) + str(user) + str(waluts))
            obj = BankAccout(balance=balance, user=user, waluts=waluts)
            obj.save()
            return HttpResponseRedirect("/info")


    form = CreateBankAccForm()

    print(form)

    return render(request, 'bank/form.html', {"form":form})


