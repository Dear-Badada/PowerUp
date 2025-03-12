from django import forms
from .models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password']


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(widget=forms.PasswordInput, label="Password", required=True)


class RechargeForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,  # Ensure the recharge amount is greater than 0.01
        label="Amount"
    )