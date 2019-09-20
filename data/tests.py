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
        directory = os.path.dirname(__file__)
        searches_data = json.load(open(os.path.join(directory, 'searches.json')))
        searches = searches_data['searches']
        expected_results = searches_data['results']

        for index, search in enumerate(searches):
            location_filter = '%s,%s' % (search['longitude'], search['latitude'])
            request = self.client.get(reverse('camper-list'), {'location': location_filter})
            self.assertEqual(request.status_code, 200)
            self.assertJSONEqual(request.content, expected_results[index]['search_results'])

        # Test location format bad request
        request = self.client.get(reverse('camper-list'), {'location': 'nan,nan'})
        self.assertEqual(request.status_code, 400)
        response = request.json()
        self.assertEqual(response, {'location': ['Format should be lon,lat']})
