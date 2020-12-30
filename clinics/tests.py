from django.test import TestCase, SimpleTestCase, Client 
from django.shortcuts import reverse 
from clinics.models import Clinic 

# Create your tests here.
class ProfileTestCase(SimpleTestCase): 
    """Test the clinics profile page."""

    def test_profile(self): 
        """Send a request to an example profile page."""
        pass 
        

