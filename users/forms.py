from django.contrib.auth.forms import UserCreationForm 
from .models import User, Patient, Doctor, Clinic  
from django.db import models 
from django import forms
from django.forms import ModelForm, Textarea
from django.contrib.postgres.forms import SimpleArrayField

class DateInput(forms.DateInput): 
    input_type = 'date'

class RegisterForm(UserCreationForm): 
    class Meta: 
        model = User 
        fields = ['email', 'first_name', 'last_name', 'user_type', 'password1', 'password2']

class LoginForm(forms.Form): 
    username = forms.CharField(max_length=64)
    password = forms.CharField(max_length=64, widget=forms.PasswordInput())


class PatientForm(ModelForm): 
    class Meta: 
        model = Patient 
        exclude = ['user']
        widgets = {
            'allergies': Textarea(attrs={'id': 'allergies'}), 
            'birth': DateInput, 
            'current_medications': Textarea(attrs={'id': 'medications'}), 
            'medical_conditions': Textarea(attrs={'id': 'conditions'})
        }
    



class DoctorForm(ModelForm): 
    class Meta: 
        model = Doctor 
        fields = ['number', 'degree']
    
class ClinicForm(ModelForm): 
    class Meta: 
        model = Clinic 
        fields = ['name', 'email', 'city']