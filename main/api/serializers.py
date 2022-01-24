from asyncore import write
from dataclasses import field
from operator import truediv
from urllib import request
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

from register.models import CustomUser
from bank.models import BankAccout, transaction 

User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','password']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class BankAccountSerializer(serializers.HyperlinkedModelSerializer):
    accNumber = serializers.IntegerField()
    balance = serializers.FloatField()
    user = serializers.CharField()
    accName = serializers.CharField(max_length=50)
    waluts = serializers.CharField()

    class Meta:
        model = BankAccout
        fields = '__all__'


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = transaction
        field = ['id','fromBank', 'toBank', 'amount', 'currency']
        