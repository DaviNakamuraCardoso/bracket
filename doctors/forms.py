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
            'duration': forms.TimeInput(attrs={'type': 'time', 'class': 'time'}), 
            'break_time': forms.TimeInput(attrs={'type': 'time', 'class':'time'}) 
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
    