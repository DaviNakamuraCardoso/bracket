from django.test import TestCase, Client, SimpleTestCase
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

# Test the login and authentication 
class LoginTestCase(SimpleTestCase): 
    pass 


    
    

        