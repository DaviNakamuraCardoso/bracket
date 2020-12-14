from users.models import User 


def get_name(first, last): 
    """Gets first and last name and returns an username."""

    n = len(User.objects.filter(first_name=first, last_name=last))
    sep = ''
    f = sep.join(first.split(" ")).lower()
    l = sep.join(last.split(" ")).lower()

    return f"{f}.{l}.{n+1}"

