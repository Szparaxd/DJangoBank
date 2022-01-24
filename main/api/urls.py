from django.http import response
from django.urls import include, path
from rest_framework import routers
from register.models import CustomUser
from .views import (GroupViewSet,UserViewSet, BankAccountViewSet,
createUser, 
login,
NumbersBankAccount,
infoBankAcc, 
przelew,
history,createBankAcc, przelewyCykliczne, bankomat, wplatomat)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'bankaccount',BankAccountViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('test/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', login),
<<<<<<< HEAD
    path('bankNumbers/', NumbersBankAccount, name='bankNumbers'),
    path('infoBankAcc/', infoBankAcc, name='infoBankAcc'),
    path('createUser/', createUser, name='createUser'),
    path('createBankAcc/', createBankAcc, name='createBankAcc'),
    path('przelew/', przelew, name='przelew'),
    path('history/', history, name='history'),
=======
    path('bankNumbers/', NumbersBankAccount),
    path('infoBankAcc/', infoBankAcc),
    path('createUser/', createUser),
    path('createBankAcc/', createBankAcc),
    path('przelew/', przelew),
    path('history/', history),
    path('cyklicznyPrzelew/', przelewyCykliczne),
    path('bankomat/',bankomat ),
    path('wplatomat', wplatomat)
>>>>>>> e0e457b9bf309681b00cdf834fcc55598246dc26
]