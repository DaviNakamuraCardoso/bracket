from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from clinics.models import Clinic
from doctors.models import Area, Doctor
from users.forms import FORMS_CONTEXT
from base.models import Notification
from users.models import User, City
from background_task import background

# Create your views here.
def index(request):
    """Render all the clinics in the same city as the user."""

    clinics = Clinic.objects.all()
    doctors = Doctor.objects.all()
    areas = Area.objects.all()
    if search := request.GET.get('query'):
        vector = SearchVector('name')
        query = SearchQuery(search)

        clinics = Clinic.objects.annotate(
            rank=SearchRank(vector, query)
        ).order_by('-rank')


    local_context = {'user': request.user, 'clinics': clinics,
    'doctors': doctors, 'areas': areas}
    context = {**local_context, **FORMS_CONTEXT}


    return render(request, 'base/index.html', context=context)

def notifications(request, user_name):
    user = User.objects.get(name=user_name)
    notifications = user.notifications.all().order_by('-timestamp')
    context = {'notifications': [notification.serialize() for notification in notifications]}

    return JsonResponse(context)


def city(request):
    if search := request.GET.get('query'):
        cities = City.objects.annotate(
            similarity=TrigramSimilarity('city', search)
        ).all().order_by('-similarity')[:20]
        return render(request, 'base/cities.html', {'cities': cities})

    return render(request, 'base/cities.html')


def areas(request):

    return render(request, )


def area(request, area):
    area = Area.objects.annotate(
        similarity=TrigramSimilarity('area', area)
    ).order_by('-similarity')[0]

    context = {'area': area}

    return render(request, 'doctors/area.html', context)


def error(request):
    """Return an error page for bad requests."""
    return render(request, 'base/error.html')
