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

    def test_filters(self):
        # Load searches and check API expected_results
        directory = os.path.dirname(__file__)
        searches_data = json.load(open(os.path.join(directory, 'searches.json')))
        searches = searches_data['searches']
        expected_results = searches_data['results']

        for index, search in enumerate(searches):
            location_filter = '%s,%s' % (search['longitude'], search['latitude'])
            filters = {'location': location_filter}
            if 'start_date' in search:
                filters['start_date'] = search['start_date']
            if 'end_date' in search:
                filters['end_date'] = search['end_date']
            request = self.client.get(reverse('camper-list'), filters)
            self.assertEqual(request.status_code, 200)
            self.assertJSONEqual(request.content, expected_results[index]['search_results'])

        # Test location format bad request
        request = self.client.get(reverse('camper-list'), {'location': 'nan,nan'})
        self.assertEqual(request.status_code, 400)
        response = request.json()
        self.assertEqual(response, {'location': ['Format should be lon,lat']})

        # Test date format bad request
        request = self.client.get(reverse('camper-list'), {'start_date': 'bad date format',
                                                           'end_date': 'bad date format'})
        self.assertEqual(request.status_code, 400)
        response = request.json()
        self.assertEqual(response, {'start_date': ['Enter a valid date.'], 'end_date': ['Enter a valid date.']})

        # Test missing date
        request = self.client.get(reverse('camper-list'), {'start_date': '2019-08-01'})
        self.assertEqual(request.status_code, 400)
        response = request.json()
        self.assertEqual(response, {'date_range': ['You should provide both start_date and end_date']})

        # Test end lower than start
        request = self.client.get(reverse('camper-list'), {'start_date': '2019-08-01',
                                                           'end_date': '2019-07-31'})
        self.assertEqual(request.status_code, 400)
        response = request.json()
        self.assertEqual(response, {'end_date': ['end_date shoud be greater than start_date']})
