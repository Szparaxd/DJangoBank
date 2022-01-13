from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm

# Create your views here.

def SignUpViev(response):
    if response.method == 'POST':
        form = CustomUserCreationForm(response.POST)

        if form.is_valid():
            form.save()
            return redirect("/")

    else:
        form = UserCreationForm()

        return render(response,'registration/signup.html', {"form":form})
