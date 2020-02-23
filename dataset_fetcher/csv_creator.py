import datetime
import os
import pathlib

import petl
from django.conf import settings
from django.utils import timezone

from dataset_fetcher.models import Dataset

HEADERS = [
    'name', 'height', 'mass',
    'hair_color', 'skin_color', 'eye_color',
    'birth_year', 'gender', 'homeworld',
    'date'
]


def convert_iso_datetime_string_to_string_date(iso_datetime):
    return datetime.datetime.strptime(iso_datetime, '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%Y-%m-%d')


def get_file_name():
    timestamp = int(timezone.now().timestamp() * 1000)  # timestamp without decimal places
    return f'{timestamp}.csv'


def create_csv_based_on_peoples(peoples):
    pathlib.Path(settings.CSV_FILES_DIRECTORY).mkdir(parents=True, exist_ok=True)
    file_path = os.path.join(settings.CSV_FILES_DIRECTORY, get_file_name())
    petl.fromdicts(
        peoples
    ).convert(
        'edited', convert_iso_datetime_string_to_string_date
    ).rename(
        'edited',
        'date'
    ).cut(
        HEADERS
    ).tocsv(
        file_path
    )

    return Dataset.objects.create(file=file_path)
