from users.models import User 
from clinics.models import Clinic


def get_name(first, last): 

    """Gets first and last name and returns an username."""
    n = len(User.objects.filter(first_name=first, last_name=last))
    sep = ''
    f = sep.join(first.split(" ")).lower()
    l = sep.join(last.split(" ")).lower()

    return f"{f}.{l}.{n}"


def get_clinic_name(request):
    """Get the name for the url."""
    name = request.POST['name'].split(' ')
    sep = ''
    base = sep.join(name).lower()
    l = len(Clinic.objects.filter(base_name=base))
    appendix = f".{l}" if l > 0 else ''
    

    return [base, f"{base}{appendix}"]

