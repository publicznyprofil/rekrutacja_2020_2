import json
from unittest import mock

from django.test import TestCase
from django.urls import reverse

from dataset_fetcher.models import Dataset
from dataset_fetcher.tests import SAMPLE_CSV_FILE_PATH


class DatasetListViewTest(TestCase):
    url = reverse('dataset_fetcher:dataset-list')

    def test_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)


@mock.patch('dataset_fetcher.views.FetchSwapi')
@mock.patch('dataset_fetcher.views.create_csv_based_on_peoples')
class DatasetCreateViewTest(TestCase):
    def test_post(self, mocked_create_csv, mocked_fetch_swapi):
        mocked_create_csv.return_value = Dataset.objects.create(file=SAMPLE_CSV_FILE_PATH)
        url = reverse('dataset_fetcher:dataset-create')

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(mocked_create_csv.called)
        self.assertTrue(mocked_fetch_swapi.called)


class DatasetDetailViewTest(TestCase):
    def test_get(self):
        dataset = Dataset.objects.create(file=SAMPLE_CSV_FILE_PATH)
        url = reverse('dataset_fetcher:dataset-detail', kwargs={'pk': dataset.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


class DatasetRowsViewTest(TestCase):
    def test_get(self):
        dataset = Dataset.objects.create(file=SAMPLE_CSV_FILE_PATH)
        url = reverse('dataset_fetcher:dataset-rows', kwargs={'pk': dataset.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        json_response = json.loads(str(response.content, encoding='utf-8'))
        self.assertIn('success', json_response)
        self.assertIn('rows', json_response)
        self.assertEqual(len(json_response['rows']), 11)

    def test_aggregation_with_one_header(self):
        dataset = Dataset.objects.create(file=SAMPLE_CSV_FILE_PATH)
        url = reverse('dataset_fetcher:dataset-rows', kwargs={'pk': dataset.pk})

        response = self.client.get(url, {'headers[]': 'date', 'page': 0})

        self.assertEqual(response.status_code, 200)
        json_response = json.loads(str(response.content, encoding='utf-8'))
        self.assertIn('success', json_response)
        self.assertIn('rows', json_response)
        self.assertEqual(len(json_response['rows']), 2)

    def test_aggregation_with_two_headers(self):
        dataset = Dataset.objects.create(file=SAMPLE_CSV_FILE_PATH)
        url = reverse('dataset_fetcher:dataset-rows', kwargs={'pk': dataset.pk})

        response = self.client.get(url, {'headers[]': ['date', 'gender'], 'page': 0})

        self.assertEqual(response.status_code, 200)
        json_response = json.loads(str(response.content, encoding='utf-8'))
        self.assertIn('success', json_response)
        self.assertIn('rows', json_response)
        self.assertEqual(len(json_response['rows']), 5)
