from django import forms
from .models import User, Invoice

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['user', 'amount', 'description', 'status']
