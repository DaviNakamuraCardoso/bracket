from django import forms 
from datetime import datetime
from patients.data import allergies, conditions, drugs
from doctors.data import areas 
from clinics.models import Clinic
from floppyforms.widgets import Input


class PatientForm(forms.Form): 
    day = forms.IntegerField(min_value=1, max_value=31)
    month = forms.IntegerField(min_value=1, max_value=12)
    year = forms.IntegerField(min_value=1900, max_value=datetime.now().year)

    weight = forms.FloatField(min_value=0, max_value=300)
    height = forms.FloatField(min_value=0, max_value=3)

    choices_conditions = forms.CharField(max_length=64, widget=Input(datalist=conditions.conditions), required=False)  
    conditions = forms.CharField(max_length=256, widget=forms.HiddenInput, required=False)

    choices_medications = forms.CharField(max_length=64, widget=Input(datalist=drugs.drugs), required=False) 
    medications = forms.CharField(max_length=256, widget=forms.HiddenInput, required=False)

    choices_allergies = forms.CharField(max_length=64, widget=Input(datalist=allergies.allergies), required=False)
    allergies = forms.CharField(max_length=256, widget=forms.HiddenInput, required=False)



class UserForm(forms.Form): 
    email = forms.EmailField(max_length=64)
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    password = forms.CharField(max_length=64, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(max_length=64, widget=forms.PasswordInput)
    city = forms.ChoiceField(widget=forms.Select(attrs={'class': 'city-field'}))


class DoctorForm(forms.Form):
    degree = forms.CharField(max_length=128)
    number = forms.IntegerField(max_value=99999999999)
    choices_areas = forms.CharField(max_length=128, widget=Input(datalist=areas.areas), required=False)
    areas = forms.CharField(max_length=2000, widget=forms.HiddenInput)


class ClinicForm(forms.Form): 
    clinic_email = forms.EmailField(max_length=64, required=False)
    clinic_name = forms.CharField(max_length=64)
    clinic_city = forms.ChoiceField(widget=forms.Select(attrs={'class': 'city-field'}))
    

class LoginForm(forms.Form): 
    username = forms.EmailField(max_length=128)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)


class CheckBox(forms.Form): 
    types = forms.CharField(max_length=128, widget=forms.HiddenInput)
    checkbox = forms.ChoiceField(choices=[('Patient', 'patient'), ('Doctor', 'doctor'), ('Clinic', 'clinic')], required=False)


FORMS_CONTEXT = {
    'form': PatientForm(), 
    'user_form': UserForm(), 
    'doctor_form': DoctorForm(), 
    'clinic_form': ClinicForm(), 
    'checkbox': CheckBox()
}