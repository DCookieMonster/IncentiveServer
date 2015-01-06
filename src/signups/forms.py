from django import forms

from .models import SignUp,Incentive,Tag

class SignUpForm(forms.ModelForm):
    class Meta:
        model = SignUp
    
class IncentiveFrom(forms.ModelForm):
    class Meta:
        model=Incentive
