from django.test import SimpleTestCase
from django.shortcuts import reverse
from .models import *
from users.data.geolocation import locate


# Create your tests here.
class TestLocation(SimpleTestCase): 
    """Test the location algorithm, giving the coordinates of a 
    city and expecting it as the first result in the set of cities."""

    
    def test_ny(self): 
        """Test the Geolocation of New York, New York, the largest city in US by population."""
        cities = locate(40.69, -73.92)
        ny = cities[0]['city'] + ', ' + cities[0]['state_id']
        self.assertEqual(ny, "New York, NY")


    def test_sitka(self): 
        """Test the Geolocation of Sitka, Alaska, the largest city in the US by area."""
        cities = locate(57.24, -135)
        sitka = cities[0]['city'] + ', ' + cities[0]['state_id']
        self.assertEqual(sitka, "Sitka, AK")


    def test_monowi(self): 
        """Test the location of Monowi, Nebraska, the smallest city in the US by population."""
        cities = locate(42.83, -98.32)
        monowi = cities[0]['city'] + ', ' + cities[0]['state_id']
        self.assertEqual(monowi, "Monowi, NE")


    def test_lost_springs(self): 
        """Test the Geolocation of Lost Springs, Wyoming, the smallest city in the US by area."""
        cities = locate(42.76, -104.96)
        lost_springs = cities[0]['city'] + ', ' + cities[0]['state_id']
        self.assertEqual(lost_springs, "Lost Springs, WY")


    def test_phoenix(self): 
        """Test the Geolocation of Phoenix, Arizona, the largest capital in the US by population"""
        cities = locate(33.54, -112.06)
        phoenix = cities[0]['city'] + ', ' + cities[0]['state_id']
        self.assertEqual(phoenix, "Phoenix, AZ")
    

    def test_montpelier(self): 
        """Test the Geolocation of Montpelier, Vermont, the smallest capital in the US by population."""
        cities = locate(44.24, -72.55)
        montpelier = cities[0]['city'] + ', ' + cities[0]['state_id']
        self.assertEqual(montpelier, "Montpelier, VT")
    
    def test_sao_paulo(self): 
        """Test the Geolocation of São Paulo, São Paulo, the larger city in Brazil by population."""
        cities = locate(-23.55, -46.65)
        sp = cities[0]['city'] + ', ' + cities[0]['state_id']
        self.assertEqual(sp, "São Paulo, SP")
    
    def test_serra_da_saudade(self): 
        """Test the Geolocation of Serra da Saudade, Minas Gerais, the smallest city in Brazil by population."""
        cities = locate(-19.44, -45.79)
        serra_da_saudade = cities[0]['city'] + ', ' + cities[0]['state_id']
        self.assertEqual(serra_da_saudade, "Serra da Saudade, MG")
    
    def test_altamira(self): 
        """Test the Geolocation of Altamira, Pará, the largest city in Brazil by area"""
        cities = locate(-3.22, -52.23)
        altamira = cities[0]['city'] + ', ' + cities[0]['state_id']
        self.assertEqual(altamira, "Altamira, PA")
    
    def test_santa_cruz(self): 
        """Test the Geolocation of Santa Cruz de Minas, Minas Gerais, the smallest city in Brazil by area."""
        cities = locate(-21.12, -44.22)
        santa_cruz = cities[0]['city'] + ', ' + cities[0]['state_id']
        self.assertEqual(santa_cruz, "Santa Cruz de Minas, MG")

    def test_sjc(self): 
        cities = locate(-23.19, -45.90)
        sjc = cities[0]['city'] + ', ' + cities[0]['state_id']
        self.assertEqual(sjc, "São José dos Campos, SP")
