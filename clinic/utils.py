from .models import User 

def register_user(cleaned_data):
    password = cleaned_data['password']
    confirmation = cleaned_data['confirmation']

    if password != confirmation: 
        return False 
    else: 
        try: 
            user = User.objects.create_user(
                username=cleaned_data['username'], 
                first_name=cleaned_data['first_name'], 
                last_name=cleaned_data['last_name'], 
                password=password, 
                email=cleaned_data['email'], 
                birth=cleaned_data['birth'], 
                trade_number=cleaned_data['trade_number']
            )
            user.save()
            return True 
        except IntegrityError:
            return False 

    return True  

        


    