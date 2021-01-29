from django.test import TestCase, Client, SimpleTestCase
from django.shortcuts import reverse
import unittest
from .models import *
from users.data.geolocation import locate

# Create your tests here.
class TestLocation(SimpleTestCase): 
    """Test the location algorithm, giving the coordinates of a 
    city and expecting it as the first result in the set of cities."""

    
    def test_ny(self): 
        """Test the Geolocation of New York, New York, the largest city in US by population."""
        cities = locate(40.69, -73.92)
        ny = cities[0][0] + ', ' + 'NY'
        self.assertEqual(ny, "New York, NY")


    def test_sitka(self): 
        """Test the Geolocation of Sitka, Alaska, the largest city in the US by area."""
        cities = locate(57.24, -135)
        sitka = cities[0][0] + ', ' + cities[0][2]
        self.assertEqual(sitka, "Sitka, AK")


    def test_monowi(self): 
        """Test the location of Monowi, Nebraska, the smallest city in the US by population."""
        cities = locate(42.83, -98.32)
        monowi = cities[0][0] + ', ' + cities[0][2]
        self.assertEqual(monowi, "Monowi, NE")


    def test_lost_springs(self): 
        """Test the Geolocation of Lost Springs, Wyoming, the smallest city in the US by area."""
        cities = locate(42.7, -104.96)
        lost_springs = cities[0][0] + ', ' + cities[0][2]
        self.assertEqual(lost_springs, "Lost Springs, WY")


    def test_phoenix(self): 
        """Test the Geolocation of Phoenix, Arizona, the largest capital in the US by population"""
        cities = locate(33.54, -112.06)
        phoenix = cities[0][0] + ', ' + cities[0][2]
        self.assertEqual(phoenix, "Phoenix, AZ")
    

    def test_montpelier(self): 
        """Test the Geolocation of Montpelier, Vermont, the smallest capital in the US by population."""
        cities = locate(44.24, -72.55)
        montpelier = cities[0][0] + ', ' + cities[0][2]
        self.assertEqual(montpelier, "Montpelier, VT")
