from django.contrib.auth.forms import UserCreationForm 
from patients.data import drugs, allergies, conditions
from doctors.data import areas 
from users.models import User  
from users.data.cities import cities
from doctors.models import Doctor 
from clinics.models import Clinic
from patients.models import Patient
from django.db import models 
from django import forms
from django.forms import ModelForm, Textarea
from django.contrib.postgres.forms import SimpleArrayField
from floppyforms.widgets import Input 


class DateInput(forms.DateInput): 
    input_type = 'date'


class RegisterForm(UserCreationForm): 
    class Meta: 
        model = User 
        fields = ['email', 'first_name', 'last_name', 'city', 'user_type', 'password1', 'password2']


class LoginForm(forms.Form): 
    username = forms.CharField(max_length=64)
    password = forms.CharField(max_length=64, widget=forms.PasswordInput())
    

class PatientForm(ModelForm): 
    
    temp_allergies = forms.ChoiceField(label="Allergies", required=False, widget=Input(datalist=allergies.allergies))
    temp_conditions = forms.ChoiceField(label="Conditions", required=False, widget=Input(datalist=conditions.conditions))
    temp_medications = forms.ChoiceField(choices=drugs.drugs, label="Medications", required=False, widget=Input(datalist=drugs.drugs))

    class Meta: 
        model = Patient 
        exclude = ['user']
        widgets = {
            'allergies': forms.HiddenInput(attrs={'id': 'allergies'}), 
            'birth': DateInput, 
            'current_medications': forms.HiddenInput(attrs={'id': 'medications'}), 
            'medical_conditions': forms.HiddenInput(attrs={'id': 'conditions'})
        }
    

class DoctorForm(ModelForm): 

    temp_areas = forms.ChoiceField(label="Areas", required=False, widget=Input(datalist=areas.areas))
    class Meta: 
        model = Doctor 
        exclude = ['user']
        widgets = {
            'areas': forms.HiddenInput(attrs={'id': 'areas'})
        }
        

class ClinicForm(ModelForm): 
    class Meta: 
        model = Clinic 
        fields = ['name', 'email', 'city']

        