from django import forms
from webapp.models import Food, Order, OrderFoods


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        exclude = []


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['operator']


class OrdersFoodForm(forms.ModelForm):
    class Meta:
        model = OrderFoods
        exclude = ['order']

