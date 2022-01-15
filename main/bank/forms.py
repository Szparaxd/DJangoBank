from django import forms
from django.db.models import fields
from django.forms import models


from .models import BankAccout, transaction
from .const import WALUTS

class CreateBankAccForm(forms.Form):
    accName = forms.CharField(label="Nazwa Konta ", max_length=300)
    waluts = forms.ChoiceField(label="Waluta", choices=WALUTS)

    class Meta:
        model = BankAccout
        fields = ('balance')

class TransactionForm(forms.Form):
    fromBank = forms.IntegerField(label="Nr konta nadawcy", required=True) 
    toBank = forms.IntegerField(label="Nr konta odbiorcy", required=True)
    amount = forms.FloatField(label="Kwota", required=True)
    description = forms.CharField(label="Opis",max_length=200, required=False)

    class Meta:
        model = transaction
        fields = []

    def clean(self):
        print("-------------START WALIDACJI!-------------")

        #super(TransactionForm, self).clean
        cleaned_data = super().clean()
        fromBank = cleaned_data.get('fromBank')
        toBank = cleaned_data.get("toBank")
        amount = cleaned_data.get('amount')
        description = cleaned_data.get('description')

        if not amount and not description and not toBank:
            print('IF NOT?????')
            self.errors.clear()
            return self.cleaned_data

        
        print(cleaned_data)
        banki = BankAccout.objects.all()
        myBank = BankAccout.objects.get(accNumber=fromBank)

        balanseMyBank = myBank.balance
        if balanseMyBank - amount < -100:
            self.errors["amount"] = ["Przekraczasz dopuszczalny limit debetu(-100)"]
        elif amount < 1:
            self.errors["amount"] = ["Niezła próba cwaniaczku"]

        if toBank:
            validBankTo = True
            for bankItem in banki:
                if bankItem.accNumber == toBank:
                        validBankTo = False
            if validBankTo:
              self._errors["toBank"] = ["Sprawdź numer konta"] 

        
        
     
            
        #self.errors.clear()
        print("PRINT ERRORS")
        print(self.errors)

        print("-------------KONIEC WALIDACJI-------------")
        return self.cleaned_data