from django.test import TestCase, Client, SimpleTestCase 
from django.shortcuts import reverse 
from base.time import intftimedelta, strfdelta
from datetime import timedelta, date, datetime, timezone 
from time import mktime 

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
        """From a 20 days input, we expect a 2 weeks and 6 days output"""
        delta = timedelta(days=20)

        result = intftimedelta(delta)

        self.assertEqual(result['days'], 6)

    def test_2_weeks(self): 
        delta = timedelta(days=15)

        result = intftimedelta(delta)

        self.assertEqual(result['weeks'], 2)


    def test_3_months(self): 
        delta = timedelta(days=30.4375 * 3 + 1)

        result = intftimedelta(delta)
        
        self.assertEqual(result['months'], 3)


    def test_2_years(self): 
        delta = timedelta(days=2*365.25 + 1)

        result = intftimedelta(delta)

        self.assertEqual(result['years'], 2)

    def test_2_seconds_from_timestamp(self): 
        delta = timedelta(seconds=2)

        timestamp = datetime.now(timezone.utc) - delta 

        result = intftimedelta(timestamp=timestamp)

        self.assertEqual(result['seconds'], 2)

    def test_3_minutes_from_timestamp(self): 
        delta = timedelta(minutes=3)

        timestamp = datetime.now(timezone.utc) - delta 

        result = intftimedelta(timestamp=timestamp)

        self.assertEqual(result['minutes'], 3)


    def test_5_hours_from_timestamp(self): 
        delta = timedelta(hours=5)

        timestamp = datetime.now(timezone.utc) - delta 

        result = intftimedelta(timestamp=timestamp)

        self.assertEqual(result['hours'], 5)

    def test_6_days_from_timestamp(self): 
        delta = timedelta(days=6)

        timestamp = datetime.now(timezone.utc) - delta 

        result = intftimedelta(timestamp=timestamp)

        self.assertEqual(result['days'], 6)


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

    def test_3_days(self): 
        delta = timedelta(days=3)

        result = strfdelta(delta)

        self.assertEqual(result, '3 days ago')

    def test_4_weeks(self): 
        delta = timedelta(days=28)

        result = strfdelta(delta)

        self.assertEqual(result, '4 weeks ago')
    
    def test_9_months(self): 
        delta = timedelta(days=9*30.4375 + 1)

        result = strfdelta(delta)

        self.assertEqual(result, '9 months ago')

    def test_1_week(self): 
        delta = timedelta(days=7)

        result = strfdelta(delta)

        self.assertEqual(result, '1 week ago')

    def test_1_month(self): 
        delta = timedelta(days=30.4375)

        result = strfdelta(delta)

        self.assertEqual(result, '1 month ago')
    
    def test_1_year(self): 
        delta = timedelta(days=370)

        result = strfdelta(delta)

        self.assertEqual(result, '1 year ago')
    
    

