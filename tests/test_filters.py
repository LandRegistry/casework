import dateutil.parser
import unittest
from application.frontend.frontend import date_filter, country_lookup_filter


class FiltersTestCase(unittest.TestCase):

    def test_minute_date_filter(self):
        dt = '2014-10-10T14:34:47.217985+01'
        self.assertEquals(date_filter(dt, 'minute'), '10-10-2014 14:34')

    def test_day_date_filter(self):
        dt_str = '2014-10-10T14:34:47.217985+01'
        sample = dateutil.parser.parse(dt_str)
        dt= long(sample.strftime("%s"))
        self.assertEquals(date_filter(dt, 'day resolution'), '10-10-2014')


    def test_country_filter(self):
        self.assertEquals(country_lookup_filter('GB'), 'United Kingdom')
        try:
            country_lookup_filter('NN')
            self.fail("Expected Key error")
        except KeyError:
            self.assertTrue(1, 1)




