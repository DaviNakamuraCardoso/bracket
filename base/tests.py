from django.test import TestCase, Client, SimpleTestCase 
from django.shortcuts import reverse 
from base.time import intftimedelta, strfdelta
from datetime import timedelta, date

# Create your tests here.
class IndexTestCase(SimpleTestCase):
    """Test the index page."""

    def test_index(self):
        """
            Test if it's possible to access the index page 
        """
        pass


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

class IntftimedeltaTestCase(SimpleTestCase): 
    """Test the base time module."""

    def test_45_seconds(self): 
        delta = timedelta(seconds=45)

        result = intftimedelta(delta)

        self.assertEqual(result['seconds'], 45)

    def test_50_minutes(self): 
        delta = timedelta(minutes=50)

        result = intftimedelta(delta)
        
        self.assertEqual(result['minutes'], 50)

    def test_4_hours(self): 
        delta = timedelta(hours=4)

        result = intftimedelta(delta)

        self.assertEqual(result['hours'], 4)
    

    def test_20_days(self): 
        delta = timedelta(days=20)

        result = intftimedelta(delta)

        self.assertEqual(result['days'], 20)


    def test_3_months(self): 
        delta = timedelta(days=30.4375 * 3 + 1)

        result = intftimedelta(delta)
        
        self.assertEqual(result['months'], 3)


    def test_2_years(self): 
        delta = timedelta(days=2*365.25 + 1)

        result = intftimedelta(delta)

        self.assertEqual(result['years'], 2)


class StrfdeltaTestCase(SimpleTestCase): 

    def test_3_seconds(self): 
        delta = timedelta(seconds=3)

        result = strfdelta(delta)

        self.assertEqual(result, '3 seconds ago')

    def test_6_minutes(self): 
        delta = timedelta(minutes=6)

        result = strfdelta(delta)

        self.assertEqual(result, '6 minutes ago')

    def test_4_hours(self): 
        delta = timedelta(hours=4)

        result = strfdelta(delta)

        self.assertEqual(result, '4 hours ago')

    def test_8_days(self): 
        delta = timedelta(days=8)

        result = strfdelta(delta)

        self.assertEqual(result, '8 days ago')

    def test_9_months(self): 
        delta = timedelta(days=9*30.4375 + 1)

        result = strfdelta(delta)

        self.assertEqual(result, '9 months ago')

