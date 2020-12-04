from django.test import TestCase, Client 

# Create your tests here.

class IndexTestCase(TestCase):

    
    def test_index(self):
        # Create the client 
        client = Client()

        # Send a simple get request 
        response = client.get("")

        # Check the status code 
        self.assertEqual(response.status_code, 200)
       