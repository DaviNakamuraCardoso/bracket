from django.test import TestCase, Client, SimpleTestCase
from django.shortcuts import reverse
import unittest
from .models import *

# Create your tests here.

class TestViews(SimpleTestCase): 
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



class TestUsers(SimpleTestCase): 
    pass






        

