from django.contrib.auth.forms import UserCreationForm 
from .models import User, Patient, Doctor, Clinic  
from django import forms
from django.forms import ModelForm


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
        fields = ['weight', 'height']
    

class DoctorForm(ModelForm): 
    class Meta: 
        model = Doctor 
        fields = ['number', 'degree']
    
class ClinicForm(ModelForm): 
    class Meta: 
        model = Clinic 
        fields = ['name', 'email', 'city']