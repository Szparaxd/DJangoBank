from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from .models import CustomUser
from .forms import CustomUserCreationForm

# Create your views here.

def SignUpViev(response):
    if response.method == 'POST':
        print(response.POST)
        form = CustomUserCreationForm(response.POST)
        print("CLEANED DATA----------------------------------:")
        if form.is_valid():
            form.save()

            return HttpResponseRedirect("/")
        return render(response,'registration/signup.html', {"form":form})

    else:
        form = UserCreationForm()
        return render(response,'registration/signup.html', {"form":form})
