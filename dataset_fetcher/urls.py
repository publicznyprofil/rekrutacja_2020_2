from django.urls import path

from dataset_fetcher.views import (
    DatasetListView, DatasetCreateView, DatasetDetailView,
    DatasetDownloadView, DatasetRowsView,
)

app_name = 'dataset_fetcher'

urlpatterns = [
    path('', DatasetListView.as_view(), name='dataset-list'),
    path('create/dataset', DatasetCreateView.as_view(), name='dataset-create'),
    path('dataset/<int:pk>', DatasetDetailView.as_view(), name='dataset-detail'),
    path('dataset/<int:pk>/download', DatasetDownloadView.as_view(), name='dataset-download'),
    path('dataset/<int:pk>/rows', DatasetRowsView.as_view(), name='dataset-rows'),
]
