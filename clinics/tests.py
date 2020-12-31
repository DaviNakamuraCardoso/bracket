from django.test import TestCase, SimpleTestCase, Client 
from django.shortcuts import reverse 
from clinics.models import Clinic 

# Create your tests here.


class IndexTestCase(SimpleTestCase): 
    """Test the profile page."""

    def get_index(self): 
        """Send a get request to the index page, expecting 200 as the status code."""
        # Client 
        c = Client()

        # Response 
        response = c.get(reverse('clinics:index'))

        # Make sure the request is successful 
        self.assertEqual(response.status_code, 200)
        

class ProfileTestCase(SimpleTestCase): 
    """Test the clinics profile page."""

    def test_profile(self): 
        """Send a request to an example profile page."""
        pass 
        