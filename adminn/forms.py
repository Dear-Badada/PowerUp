from django import forms

from powerbank.models import Station, Pricing


class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = ["name", "location"]

class PricingForm(forms.ModelForm):
    class Meta:
        model = Pricing
        fields = ["hourly_rate", "deposit_amount"]  # 允许管理员修改的字段
        widgets = {
            "hourly_rate": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "deposit_amount": forms.NumberInput(attrs={"step": "0.01", "min": "0"})
        }