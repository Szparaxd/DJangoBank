"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

#views app
from bank import views as vBank
from register import views as vRegister

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('register/',vRegister.SignUpViev, name="register"),
    path('', include("django.contrib.auth.urls")),

    #bank
    path('', vBank.welcome, name="welcome"),
    path('info/', vBank.info, name="info"),
    path('createBankAcc/', vBank.createBankAcc, name="createBankAcc"),

    path('choice/', vBank.choice, name="choice"),
    path('przelew/', vBank.przelew, name="przelewa"),
    path('historia/', vBank.historia, name="historia"),

    path('ReadMe/', vBank.readMe, name="readMe"),
    path('test/', vBank.test, name='test'),

    

  
]
