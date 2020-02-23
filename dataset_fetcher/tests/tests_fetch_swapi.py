import json
from unittest import mock

from django.test import TestCase

from dataset_fetcher.fetch_swapi import FetchSwapi
from dataset_fetcher.tests import (
    PEOPLE_SWAPI_RESPONSE_PAGE1_PATH, PEOPLE_SWAPI_RESPONSE_PAGE2_PATH,
    PLANETS_SWAPI_RESPONSE_PAGE1_PATH, PLANETS_SWAPI_RESPONSE_PAGE2_PATH
)


@mock.patch('dataset_fetcher.fetch_swapi.requests.get')
class FetchSwapiTest(TestCase):
    def test_get_resolved_people(self, mocked_requests):
        fp_people_response_page_1 = open(PEOPLE_SWAPI_RESPONSE_PAGE1_PATH, 'r', )
        fp_people_response_page_2 = open(PEOPLE_SWAPI_RESPONSE_PAGE2_PATH, 'r', )
        fp_planets_response_page_1 = open(PLANETS_SWAPI_RESPONSE_PAGE1_PATH, 'r', )
        fp_planets_response_page_2 = open(PLANETS_SWAPI_RESPONSE_PAGE2_PATH, 'r', )

        mocked_requests.return_value.json.side_effect = [
            json.load(fp_people_response_page_1),
            json.load(fp_people_response_page_2),
            json.load(fp_planets_response_page_1),
            json.load(fp_planets_response_page_2),
        ]
        fp_people_response_page_1.close()
        fp_people_response_page_2.close()

        peoples = FetchSwapi().get_resolved_peoples()

        self.assertEqual(len(peoples), 20)
        self.assertDictEqual(
            peoples[0],
            {
                "name": "Luke Skywalker",
                "height": "172",
                "mass": "77",
                "hair_color": "blond",
                "skin_color": "fair",
                "eye_color": "blue",
                "birth_year": "19BBY",
                "gender": "male",
                "homeworld": "Utapau",
                "films": [
                    "https://swapi.co/api/films/2/",
                    "https://swapi.co/api/films/6/",
                    "https://swapi.co/api/films/3/",
                    "https://swapi.co/api/films/1/",
                    "https://swapi.co/api/films/7/"
                ],
                "species": [
                    "https://swapi.co/api/species/1/"
                ],
                "vehicles": [
                    "https://swapi.co/api/vehicles/14/",
                    "https://swapi.co/api/vehicles/30/"
                ],
                "starships": [
                    "https://swapi.co/api/starships/12/",
                    "https://swapi.co/api/starships/22/"
                ],
                "created": "2014-12-09T13:50:51.644000Z",
                "edited": "2014-12-20T21:17:56.891000Z",
                "url": "https://swapi.co/api/people/1/"
            }
        )
        self.assertEqual(mocked_requests.call_count, 4)

    def test_get_peoples(self, mocked_requests):
        fp_people_response_page_1 = open(PEOPLE_SWAPI_RESPONSE_PAGE1_PATH, 'r', )
        fp_people_response_page_2 = open(PEOPLE_SWAPI_RESPONSE_PAGE2_PATH, 'r', )

        mocked_requests.return_value.json.side_effect = [
            json.load(fp_people_response_page_1),
            json.load(fp_people_response_page_2),
        ]
        fp_people_response_page_1.close()
        fp_people_response_page_2.close()

        peoples = FetchSwapi().get_peoples()

        self.assertEqual(len(peoples), 20)
        self.assertDictEqual(
            peoples[0],
            {
                "name": "Luke Skywalker",
                "height": "172",
                "mass": "77",
                "hair_color": "blond",
                "skin_color": "fair",
                "eye_color": "blue",
                "birth_year": "19BBY",
                "gender": "male",
                "homeworld": "https://swapi.co/api/planets/1/",
                "films": [
                    "https://swapi.co/api/films/2/",
                    "https://swapi.co/api/films/6/",
                    "https://swapi.co/api/films/3/",
                    "https://swapi.co/api/films/1/",
                    "https://swapi.co/api/films/7/"
                ],
                "species": [
                    "https://swapi.co/api/species/1/"
                ],
                "vehicles": [
                    "https://swapi.co/api/vehicles/14/",
                    "https://swapi.co/api/vehicles/30/"
                ],
                "starships": [
                    "https://swapi.co/api/starships/12/",
                    "https://swapi.co/api/starships/22/"
                ],
                "created": "2014-12-09T13:50:51.644000Z",
                "edited": "2014-12-20T21:17:56.891000Z",
                "url": "https://swapi.co/api/people/1/"
            }
        )
        self.assertEqual(mocked_requests.call_count, 2)

    def test_get_planets(self, mocked_requests):
        fp_people_response_page_1 = open(PLANETS_SWAPI_RESPONSE_PAGE1_PATH, 'r')
        fp_people_response_page_2 = open(PLANETS_SWAPI_RESPONSE_PAGE2_PATH, 'r')

        mocked_requests.return_value.json.side_effect = [
            json.load(fp_people_response_page_1),
            json.load(fp_people_response_page_2),
        ]
        fp_people_response_page_1.close()
        fp_people_response_page_2.close()

        planets = FetchSwapi().get_planets()

        self.assertEqual(len(planets), 20)
        self.assertDictEqual(
            planets[0],
            {
                "name": "Alderaan",
                "rotation_period": "24",
                "orbital_period": "364",
                "diameter": "12500",
                "climate": "temperate",
                "gravity": "1 standard",
                "terrain": "grasslands, mountains",
                "surface_water": "40",
                "population": "2000000000",
                "residents": [
                    "https://swapi.co/api/people/5/",
                    "https://swapi.co/api/people/68/",
                    "https://swapi.co/api/people/81/"
                ],
                "films": [
                    "https://swapi.co/api/films/6/",
                    "https://swapi.co/api/films/1/"
                ],
                "created": "2014-12-10T11:35:48.479000Z",
                "edited": "2014-12-20T20:58:18.420000Z",
                "url": "https://swapi.co/api/planets/2/"
            }
        )
        self.assertEqual(mocked_requests.call_count, 2)
