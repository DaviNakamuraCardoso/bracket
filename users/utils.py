from users.models import User, City
from clinics.models import Clinic
from doctors.models import Doctor, Area
from patients.models import Patient
from django.conf import settings
import os
import datetime


def get_name(first, last): 

    """Gets first and last name and returns an username."""
    n = len(User.objects.filter(first_name=first, last_name=last))
    sufix = f".{(n)}" if n >= 1 else ''
    sep = ''
    f = sep.join(first.split(" ")).lower()
    l = sep.join(last.split(" ")).lower()

    return f"{f}.{l}" + sufix


def get_clinic_name(request):
    """Get the name for the url."""
    name = request.POST['clinic_name'].split(' ')
    sep = ''
    base = sep.join(name).lower()
    l = len(Clinic.objects.filter(base_name=base))
    appendix = f".{l}" if l > 0 else ''
    

    return {'base': base, 'name': f"{base}{appendix}"}


def new_user(request): 
    """Handles the user register."""
    data = request.POST 

    # Create the basic user model 
    types = data['types'].split(',')
    user = User.objects.create_user(
        password=data['password'], 
        email=data['email'], 
        is_doctor='doctor' in types, 
        is_patient='patient' in types, 
        city=City.objects.get(pk=data['city']), 
        first_name=data['first_name'], 
        last_name=data['last_name'], 
        name=get_name(data['first_name'], data['last_name'])

    )

    if picture := request.FILES['picture']: 

        user.picture = handle_uploaded_file(picture, user)
    
    user.save()
    
    return user 


def new_patient(request, user): 
    if 'patient' in request.POST['types'].split(','): 
    
        data = request.POST
        
        day, month, year = (data['day'], data['month'], data['year'])
        strbirth = f"{day}/{month}/{year}"
        date = datetime.datetime.strptime(strbirth, "%d/%m/%Y")

        patient = Patient.objects.create(
            user=user, 
            weight=request.POST['weight'], 
            height=request.POST['height'], 
            birth=date
        )
        allergies = data['allergies'].split(',')
        conditions = data['conditions'].split(',')
        medications = data['medications'].split(',')

        if data['allergies'] != '': 
            for allergy in allergies:
                patient.allergies.add(Allergy.objects.get(allergy=allergy))
        
        if data['medications'] != '': 
            for medication in medications: 
                patient.medications.add(Medication.objects.get(medication=medication))

        if data['conditions'] != '': 
            for condition in conditions: 
                patient.conditions.add(Condition.objects.get(condition=condition))
        
        return patient
        
    return None
    


def new_doctor(request, user): 
    if 'doctor' in request.POST['types'].split(','):
        data = request.POST 
        doctor = Doctor.objects.create(
            user=user, 
            number=data['number'], 
            degree=data['degree']
        )
        if data['areas'] != '':

            for area in data['areas'].split(','):
                doctor.areas.add(Area.objects.get(area=area))
            
        return doctor
    return None


def new_clinic(request, user): 
    if 'clinic' in request.POST['types'].split(','): 

        data = request.POST 
        clinic = Clinic.objects.create(
            admin=user, 
            name=data['clinic_name'], 
            clinic_name=get_clinic_name(request)['name'], 
            base_name=get_clinic_name(request)['base'], 
            email=data['clinic_email'], 
            city=City.objects.get(pk=data['clinic_city']), 
            address=data['clinic_address'] 
            
        )
        clinic.picture = handle_uploaded_file(request.FILES['clinic_picture'], clinic)
        clinic.save()

        return clinic
    return None


def handle_uploaded_file(file, model):
    extension = file.__str__().split('.')[-1]
    filename = f"{model.identifier()}_picture.{extension}"
    
    
    with open(os.path.join(settings.MEDIA_ROOT, filename), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    


    return filename 