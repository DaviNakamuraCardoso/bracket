from django.test import TestCase, Client, SimpleTestCase 
from django.shortcuts import reverse 

# Create your tests here.
class IndexTestCase(SimpleTestCase):

    def test_index(self):
        """
            Test if it's possible to access the index page 
        """
        # Create the client 
        c = Client()

        # Get the response
        response = c.get('')

        # Make sure the request is successful 
        self.assertEqual(response.status_code, 200)


class ErrorTestCase(SimpleTestCase): 
    """Test the error page."""
    def test_error(self): 
        """Send a get request to the error page, expecting 200 as status code."""
        # Create a client 
        c = Client()

        # Get the response 
        response = c.get(reverse('base:error'))

        # Make sure the response is successful 
        self.assertEqual(response.status_code, 200)
    