from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from users.utils import new_clinic, new_doctor, new_patient, new_user
from users.data.geolocation import locate
from users.data.time import get_calendar
from users.models import City
from users.forms import FORMS_CONTEXT, LoginForm, ClinicForm
from users.data.sorted_cities import latitude_sorted
# Create your views here.

def register_view(request):
    if request.method == "POST":
        data = request.POST
        # Create the user object
        user = new_user(request)

        # Attempt to create all the different types of users
        doctor = new_doctor(request, user)
        patient = new_patient(request, user)

        login(request, user)
        if 'clinic' in data['types'].split(','):
            return HttpResponseRedirect(reverse('users:clinic'))

        return HttpResponseRedirect(reverse('base:index'))



    return render(request, 'users/register.html', FORMS_CONTEXT)



def register_clinic(request):
    form = ClinicForm()
    if request.method == "POST":
        clinic = new_clinic(request, request.user)
        if request.user.is_doctor:
            clinic.doctors.add(request.user.doctor)

        return HttpResponseRedirect(reverse('base:index'))

    return render(request, 'users/clinic.html', {'form': form})




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

    for city in latitude_sorted[:6000]:
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


def calendar(request, month, year):

    return JsonResponse(get_calendar(month+1, year))


def user_info(request, name):
    user = User.objects.get(name=name)
    return JsonResponse({"user": user.serialize()})
