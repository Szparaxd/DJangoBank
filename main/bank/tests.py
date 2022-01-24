from audioop import reverse
from django.test import TestCase, Client
from rest_framework import status 
from bank.models import BankAccout,Kredyt,transaction
import json


#################################################################################################
#                                       INTEGRATION TESTS                                       #
#################################################################################################
# class test_models(TestCase):
#     def test_Views(self):
#         c = Client()
#         response = c.get(reverse('list'))
#         self.assertEqual(response.status_code, status=status.HTTP_200_OK)
#         self.assertTemplateUsed()
