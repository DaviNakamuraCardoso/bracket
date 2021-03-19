from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.postgres.search import TrigramSimilarity
from users.utils import new_clinic, new_doctor, new_patient, new_user, get_name, handle_uploaded_file
from users.data.geolocation import locate
from users.data.time import get_calendar
from users.models import City
from users.forms import FORMS_CONTEXT, LoginForm, ClinicForm
from users.data.sorted_cities import latitude_sorted
from django.conf import settings
# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        user = new_user(request)

        login(request=request, user=user, backend=settings.AUTHENTICATION_BACKENDS[0])
        return HttpResponseRedirect(reverse('users:register'))

    return render(request, 'users/signup.html', FORMS_CONTEXT)


def register_view(request):
    user = request.user
    if user.name is None:
        user.name = get_name(user.first_name, user.last_name)
        user.save()

    if request.method == "POST":
        data = request.POST

        if user.city is None:
            user.city = City.objects.get(pk=data['city'])
            user.save()

        if files := request.FILES:
            user.picture = handle_uploaded_file(data, files['user-picture'], user, 'user-picture')
            user.save()

        # Attempt to create all the different types of users
        doctor = new_doctor(request, user)
        patient = new_patient(request, user)
        clinic = new_clinic(request, user)

        if doctor is not None and clinic is not None:
            clinic.doctors.add(doctor)


        return HttpResponseRedirect(reverse('base:index'))

    return render(request, 'users/register.html', FORMS_CONTEXT)


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
                if next := request.GET.get('next'):
                    return HttpResponseRedirect(next)
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


def find_location(request):

    if search := request.GET.get('city'):
        cities = City.objects.annotate(
            similarity=TrigramSimilarity('city', search)
        ).all().order_by('-similarity')[:30]

        return JsonResponse([city.serialize() for city in cities], safe=False)

    return JsonResponse([], safe=False)
