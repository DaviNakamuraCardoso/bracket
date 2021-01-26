from django.test import TestCase, SimpleTestCase, Client 
from django.shortcuts import reverse

# Create your tests here.

class IndexTestCase(SimpleTestCase):
    """Tests the index page."""
    
    def test_index(self):
        """Sends a get request to index, expecting 200 as the status code"""
        pass




