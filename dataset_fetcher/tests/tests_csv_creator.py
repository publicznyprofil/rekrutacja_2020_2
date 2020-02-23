import json
import shutil
import tempfile

from django.test import TestCase, override_settings

from dataset_fetcher.csv_creator import create_csv_based_on_peoples
from dataset_fetcher.models import Dataset
from dataset_fetcher.tests import PEOPLE_SWAPI_RESPONSE_PAGE1_PATH

CSV_FILES_DIRECTORY = tempfile.mkdtemp()


class CSVCreatorTest(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(CSV_FILES_DIRECTORY, ignore_errors=True)
        super().tearDownClass()

    @override_settings(CSV_FILES_DIRECTORY=CSV_FILES_DIRECTORY)
    def test_create_csv_based_on_peoples(self):
        fp_people_response_page_1 = open(PEOPLE_SWAPI_RESPONSE_PAGE1_PATH, 'r', )
        peoples = json.load(fp_people_response_page_1)['results']

        create_csv_based_on_peoples(peoples)

        self.assertEqual(Dataset.objects.all().count(), 1)
