from django.test import TestCase, Client
from django.shortcuts import reverse
from .models import *
# Create your tests here.

class TestViews(TestCase): 
    """Test all the views for this app."""
    def test_login(self): 
        """Test the login view and return a boolean."""
        c = Client() 
        response = c.get(reverse('users:login'))

        return self.assertEqual(response.status_code, 200)
    
    def test_register(self): 
        """Test the register view and return a boolean."""
        c = Client()
        response = c.get(reverse('users:register'))

        return self.assertEqual(response.status_code, 200)



class TestUsers(TestCase): 
    # Test all the users models
    def setUp(): 
        base_user = User(email='tester@testing.com', password="test123")
        doctor_user = User(email='doctor@doctor.com', password="doctor123")
        clinic_user = User(email='clinic@clinic.com', password="clinic123")
        patient_user = User(email='patient@patient.com', password="patient123")
    





        

