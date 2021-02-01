from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from .models import User, City
from doctors.models import Doctor, Area
from patients.models import Patient, Allergy, Condition, Medication
from clinics.models import Clinic 
from users.utils import register, get_clinic_name
from users.data.cities import cities
from users.data.sorted_cities import latitude_sorted
from users.data.geolocation import locate
from patients.data import allergies, drugs, conditions
from doctors.data import areas 
import datetime
import json 
from users.forms import FORMS_CONTEXT, LoginForm
# Create your views here.

def patient(request): 
    if request.method == "POST": 
        user = register(request, 'patient')
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
        
        login(request=request, user=user)
        return HttpResponseRedirect(reverse('base:index'))
    
    return JsonResponse({"message": "Method must be POST."})


def doctor(request): 
    if request.method == "POST":
        user = register(request=request, user_type='doctor')
        data = request.POST 
        doctor_object = Doctor.objects.create(
            user=user, 
            number=data['number'], 
            degree=data['degree']
        )
        if data['areas'] != '':

            for area in data['areas'].split(','):
                doctor_object.areas.add(Area.objects.get(area=area))
            
        login(request, user)

    
    return HttpResponseRedirect(reverse('base:index'))
        

def clinic(request): 
    if request.method == "POST": 
        data = request.POST 
        user = User.objects.create_user(
            email=data['clinic_email'], 
            password=data['clinic_password'],
            is_clinic=True,
            user_type='clinic', 
            city=City.objects.get(pk=data['city'])
        )
        Clinic.objects.create(
            user=user, 
            name=data['clinic_name'], 
            clinic_name=get_clinic_name(request)['name'], 
            base_name=get_clinic_name(request)['base'], 
            email=user.email, 
            city=user.city
        )
        login(request, user)

    return HttpResponseRedirect(reverse('base:index'))
    


def login_view(request): 
    """Handles the user login."""
    form = LoginForm()
    if request.method == "POST": 
        form = LoginForm(request.POST)
        if form.is_valid(): 
            username = form.cleaned_data['username'] 
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None: 
                login(request, user)
                return redirect('base:index')
            else: 
                return render(request, 'users/login.html', {
                    'form': form, 
                    'message': 'Incorrect username/password'
                })
        else: 
            form = LoginForm()
    return render(request, 'users/login.html', {
        'form': form
    })

@login_required
def logout_view(request): 
    if request.user.is_authenticated: 
        logout(request)
    return redirect('base:index')


def create_cities(request): 
    global latitude_sorted 
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('base:error'))
    
    for city in latitude_sorted[5000:]: 
        try: 
            city_obj = City.objects.get(lat=city['lat'], lng=city['lng'])
            city_obj.timezone = city['timezone']
            city_obj.save()
            
        except City.DoesNotExist: 
            City.objects.create(
            city=city['city'], 
            state=city['state'], 
            state_id=city['state_id'], 
            lat=float(city['lat']), 
            lng=float(city['lng']), 
            timezone=city['timezone']
        )
        except City.MultipleObjectsReturned: 
            cities = City.objects.filter(lat=city['lat'], lng=city['lng'])
            for c in cities[1:]: 
                c.delete()
            cities[0].timezone = city['timezone']
            cities[0].save()


    return HttpResponseRedirect(reverse('doctors:index')) 

def eliminate(request): 
    global cities 
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('base:index'))
    
    for city in cities: 
        array = City.objects.filter(city=city[0], state=city[3])
        if len(array) > 1:
            for trash in array[:len(array)-1]:
                trash.delete()
    
    return HttpResponseRedirect(reverse('doctors:index'))




def create_patient(request): 
    global allergies, drugs, conditions 

    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('base:index'))
    
    for allergy in allergies.allergies:
        Allergy.objects.create(allergy=allergy)

    for drug in drugs.drugs: 
        Medication.objects.create(medication=drug) 
    
    for condition in conditions.conditions: 
        Condition.objects.create(condition=condition)
    
    return HttpResponseRedirect(reverse('patients:index'))


    
def create_doctor(request): 
    if not request.user.is_superuser: 
        return HttpResponseRedirect(reverse('base:index'))
    
    for area in areas.areas: 
        Area.objects.create(area=area)
        
    
    return HttpResponseRedirect(reverse('doctors:index'))


def location(request, lat, lng):
    lat = float(lat)
    lng = float(lng)

    city_names = locate(lat=lat, lng=lng)
    cities = []

    for city_name in city_names: 
        cities.append(City.objects.get(lat=city_name['lat'], lng=city_name['lng']).serialize())


    return JsonResponse({"cities":cities})
