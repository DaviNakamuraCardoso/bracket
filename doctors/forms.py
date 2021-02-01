from django import forms  
from doctors.models import Shift, Area, Doctor
from users.models import Day


class ShiftForm(forms.ModelForm): 
    class Meta: 
        model = Shift  
        exclude = ['doctor']
        widgets = {
            'start': forms.TimeInput(format="%H:%M", attrs={'type': 'time'}), 
            'end': forms.TimeInput(format="%H:%M", attrs={'type': 'time'}), 
            'duration': forms.TimeInput(format="%H:%M"), 
            'break_time': forms.TimeInput(format="%H:%M") 
        }
    
    
    days = forms.ModelMultipleChoiceField(
        queryset=Day.objects.all(), 
        widget=forms.CheckboxSelectMultiple
    )
    
    areas = forms.ModelMultipleChoiceField(
        queryset=None, 
        widget=forms.CheckboxSelectMultiple
    )
    
    clinic = forms.ModelChoiceField(
        queryset=None 
    )

    def __init__(self, *args, **kwargs): 
        self.user = kwargs.pop('user')
        super(ShiftForm, self).__init__(*args, **kwargs)
        self.fields['areas'].queryset = Doctor.objects.get(user=self.user).areas.all()
        self.fields['clinic'].queryset = Doctor.objects.get(user=self.user).clinics.all()
    