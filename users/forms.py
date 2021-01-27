from django import forms 
from datetime import datetime
from patients.data import allergies, conditions, drugs

class PatientForm(forms.Form): 
    day = forms.IntegerField(min_value=1, max_value=31)
    month = forms.IntegerField(min_value=1, max_value=12)
    year = forms.IntegerField(min_value=1900, max_value=datetime.now().year)

    weight = forms.FloatField(min_value=0, max_value=300)
    height = forms.FloatField(min_value=0, max_value=3)

    choices_conditions = forms.ChoiceField(choices=[('1', '1'), ('2', '2')])
    conditions = forms.HiddenInput()

    choices_medications = forms.ChoiceField(choices=[('1', '1')])
    medications = forms.HiddenInput()

    choices_allergies = forms.ChoiceField(choices=[('1', '1')])
    allergies = forms.HiddenInput()



class BaseForm(forms.Form): 
    email = forms.EmailField(max_length=64)
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    password = forms.CharField(max_length=64, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(max_length=64, widget=forms.PasswordInput)
