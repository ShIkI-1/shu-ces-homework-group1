from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'product_id', 'amount']

class promptform(forms.Form):
    title = forms.CharField(max_length=200)
    intro = forms.CharField(max_length=200)
    flexibility = forms.FloatField()
    randomness = forms.FloatField()
    text = forms.CharField(min_length=0)
