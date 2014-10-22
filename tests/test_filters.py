import unittest
from application.frontend.frontend import country_lookup_filter


class FiltersTestCase(unittest.TestCase):

    def test_country_filter(self):
        self.assertEquals(country_lookup_filter('GB'), 'United Kingdom')
        try:
            country_lookup_filter('NN')
            self.fail("Expected Key error")
        except KeyError:
            self.assertTrue(1, 1)




