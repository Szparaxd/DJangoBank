from django import forms
from django.forms import models
from .models import BankAccout
from .const import WALUTS

class CreateBankAccForm(forms.Form):
    name = forms.CharField(label="Name ", max_length=300)
    waluts = forms.ChoiceField(label="Waluta", choices=WALUTS)

    class Meta:
        model = BankAccout
        fields = ('balance')