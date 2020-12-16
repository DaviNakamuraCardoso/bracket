from django.test import TestCase, SimpleTestCase, Client 
from django.shortcuts import reverse

# Create your tests here.

class TestPages(SimpleTestCase):
    """Tests the pages"""
    
    def test_index(self):
        """Sends a get request to index, expecting 200 as the status code"""
        c = Client()

        response = c.get(reverse('doctors:index'))

        self.assertEqual(response.status_code, 200)

    def test_profile(self): 
        """Sends a get request to profile page, expecting 200 as the status code"""
        c = Client 

        response = c.get(reverse('doctors:profile'))

        self.assertEqual(response.status_code, 200)


