from django.http import response
from django.urls import include, path
from rest_framework import routers
from register.models import CustomUser
from .views import (GroupViewSet,UserViewSet, BankAccountViewSet, CustomUserViewSet,
createUser, 
login,
NumbersBankAccount,
infoBankAcc, 
przelew,
history,createBankAcc)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'bankaccount',BankAccountViewSet )
router.register(r'customuseres',CustomUserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('test/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', login),
    path('bankNumbers/', NumbersBankAccount, name='bankNumbers'),
    path('infoBankAcc/', infoBankAcc, name='infoBankAcc'),
    path('createUser/', createUser, name='createUser'),
    path('createBankAcc/', createBankAcc, name='createBankAcc'),
    path('przelew/', przelew, name='przelew'),
    path('history/', history, name='history'),
]