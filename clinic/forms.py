from django import forms 

class DateInput(forms.DateInput):
    input_type = "date"
    




class UserRegister(forms.Form):
    # Name 
    first_name = forms.CharField(max_length=64, label="First Name")
    last_name = forms.CharField(max_length=64, label="Last Name")
    username = forms.CharField(max_length=64, label="Username")

    # Email and useful info
    email = forms.EmailField(max_length=64, label="Email")
    birth = forms.DateField(widget=DateInput(format="%d-%m-%Y"), input_formats=('%d-%m-%Y'))
    trade_number = forms.IntegerField(label="CPF")

    # Password and confirmation
    password = forms.CharField(widget=forms.PasswordInput())
    confirmation = forms.CharField(widget=forms.PasswordInput()) 


    