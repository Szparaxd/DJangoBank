import random

import bank
from .models import BankAccout

def create_new_ref_number():
      print("Test: create_new_ref_number")
      banki = BankAccout.objects.all().values_list('accNumber',flat=True)
      print("Numery banków:")
      print(banki)
      wynik = True
      while wynik:
            liczba = random.randint(1000000000, 9999999999)
            if not liczba in banki:
                  wynik = False

      return str(liczba)

      