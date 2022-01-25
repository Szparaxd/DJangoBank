from audioop import reverse
from django.test import TestCase, Client
from rest_framework import status 
from bank.models import BankAccout,Kredyt,transaction
import json

