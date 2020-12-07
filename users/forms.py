from django.contrib.auth.forms import UserCreationForm 
from .models import User, Patient, Doctor, Clinic  
from django import forms


class RegisterForm(UserCreationForm): 
    class Meta: 
        model = User 
        fields = ['email', 'first_name', 'last_name','password1', 'password2']

class LoginForm(forms.Form): 
    username = forms.CharField(max_length=64)
    password = forms.CharField(max_length=64, widget=forms.PasswordInput())


class PatientForm(forms.Form): 
    class Meta: 
        model = Patient 
        fields = ['weight', 'height'] 
    

class DoctorForm(forms.Form): 
    class Meta: 
        model = Doctor 
        fields = ['number', 'degree']
    
class ClinicForm(forms.Form): 
    class Meta: 
        model = Clinic 
        fields = ['name', 'email', 'city']