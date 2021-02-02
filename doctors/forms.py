from django import forms  
from doctors.models import Shift, Area, Doctor
from users.models import Day


class ShiftForm(forms.ModelForm): 
    class Meta: 
        model = Shift  
        exclude = ['doctor']
        widgets = {
            'start': forms.TimeInput(attrs={'type': 'time', 'class': 'time'}), 
            'end': forms.TimeInput(attrs={'type': 'time', 'class':'time'}), 
            'break_time': forms.TimeInput(attrs={'type': 'time', 'class':'time'}), 
            'break_end': forms.TimeInput(attrs={'type': 'time', 'class':'time'}), 
            'duration': forms.HiddenInput()
        }
        labels = {
            'start': "From: ", 
            'end': "to: ", 
            'break_time': "Lunch/Break from:", 
            'break_end': "to: ", 
            'duration': "Appointment duration: "
        }

    duration_hours = forms.IntegerField(max_value=23, min_value=0, initial=0, label='h')
    duration_minutes = forms.IntegerField(max_value=59, min_value=0, initial=30, label='min', widget=forms.NumberInput(attrs={'step': 5}))

    days = forms.ModelMultipleChoiceField(
        queryset=Day.objects.all(), 
        widget=forms.CheckboxSelectMultiple
    )
    
    areas = forms.ModelMultipleChoiceField(
        queryset=None, 
        widget=forms.CheckboxSelectMultiple, 
        label='With: '
    )
    
    clinic = forms.ModelChoiceField(
        queryset=None, 
        label="Working in: " 
    )

    def __init__(self, *args, **kwargs): 
        self.user = kwargs.pop('user')
        super(ShiftForm, self).__init__(*args, **kwargs)
        self.fields['areas'].queryset = Doctor.objects.get(user=self.user).areas.all()
        self.fields['clinic'].queryset = Doctor.objects.get(user=self.user).clinics.all()
    