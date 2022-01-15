from django.urls import include, path
from rest_framework import routers

from register.models import CustomUser
from .views import (GroupViewSet,UserViewSet, BankAccountViewSet, CustomUserViewSet,
createUser, 
login,
NumbersBankAccount,
infoBankAcc, przelew)

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
    path('bankNumbers/', NumbersBankAccount),
    path('infoBankAcc/', infoBankAcc),
    path('createUser/', createUser),
    path('przelew/', przelew),
]