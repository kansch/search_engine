import json
import os

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class CamperTestCase(TestCase):

    fixtures = [
        'initial_data',
    ]

    def setUp(self):
        super().setUp()
        self.client = APIClient()

    def test_list(self):
        request = self.client.get(reverse('camper-list'))
        self.assertEqual(request.status_code, 200)
        response = request.json()
        self.assertEqual(len(response), 3)

    def test_filter_location(self):
        # Load searches and check API expected_results
        directory = os.path.join(os.path.dirname(__file__), 'tests')
        searches_data = json.load(open(os.path.join(directory, 'level_1_searches.json')))
        expected_results_data = json.load(open(os.path.join(directory, 'level_1_expected_results.json')))

        for index, search in enumerate(searches_data['searches']):
            location_filter = '%s,%s' % (search['longitude'], search['latitude'])
            request = self.client.get(reverse('camper-list'), {'location': location_filter})
            self.assertEqual(request.status_code, 200)
            response = request.json()
            a = json.dumps(expected_results_data['results'][index]['search_results'], sort_keys=True)
            b = json.dumps(response, sort_keys=True)
            self.assertEqual(a, b)

        # Test location format bad request
        request = self.client.get(reverse('camper-list'), {'location': 'nan,nan'})
        self.assertEqual(request.status_code, 400)
        response = request.json()
        self.assertEqual(response, {'location': ['Format should be lon,lat']})
