from django.shortcuts import render
from django.http import HttpResponseRedirect
from clinics.models import Clinic
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from users.forms import FORMS_CONTEXT
from base.models import Notification
from users.models import User
from background_task import background

# Create your views here.
def index(request):
    """Render all the clinics in the same city as the user."""

    clinics = Clinic.objects.all()
    if search := request.GET.get('query'):
        vector = SearchVector('name')
        query = SearchQuery(search)

        clinics = Clinic.objects.annotate(
            rank=SearchRank(vector, query)
        ).order_by('-rank')


    local_context = {'user': request.user, 'clinics': [clinic.serialize() for clinic in clinics]}
    context = {**local_context, **FORMS_CONTEXT}


    return render(request, 'base/index.html', context=context)


def error(request):
    """Return an error page for bad requests."""
    return render(request, 'base/error.html')
