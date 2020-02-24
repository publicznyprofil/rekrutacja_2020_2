import petl
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import View, ListView, DetailView

from dataset_fetcher.csv_creator import create_csv_based_on_peoples, HEADERS
from dataset_fetcher.fetch_swapi import FetchSwapi
from dataset_fetcher.models import Dataset


class DatasetListView(ListView):
    model = Dataset
    template_name = 'dataset_fetcher/dataset_list.html'


class DatasetCreateView(View):
    def post(self, request, *args, **kwargs):
        dataset = create_csv_based_on_peoples(
            FetchSwapi().get_resolved_peoples()
        )
        return HttpResponseRedirect(reverse('dataset_fetcher:dataset-download', kwargs={'pk': dataset.pk}))


class DatasetDetailView(DetailView):
    model = Dataset
    template_name = 'dataset_fetcher/dataset_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headers'] = HEADERS
        context['rows'] = petl.fromcsv(self.object.file).head(10)[1:]
        return context


class DatasetRowsView(View):
    def get(self, request, *args, **kwargs):
        self.request = request
        self.dataset = get_object_or_404(Dataset, pk=self.kwargs['pk'])

        return JsonResponse({
            'success': 200,
            'rows': self.get_rows_list()
        })

    def get_rows_list(self):
        table = petl.fromcsv(self.dataset.file)
        table = self.aggregate_table(table)
        table = self.slice_table(table)
        return list(table)

    def aggregate_table(self, table):
        key = self.get_aggregation_key()
        if key:
            return table.aggregate(key=key, aggregation=len)
        return table

    def get_aggregation_key(self):
        selected_headers = self.request.GET.getlist('headers[]')
        if len(selected_headers) > 1:
            return selected_headers
        elif selected_headers:
            return selected_headers[0]
        return None

    def slice_table(self, table):
        row_from, row_to = self.get_rows_range()
        return table.rowslice(row_from, row_to)

    def get_rows_range(self):
        try:
            page = int(self.request.GET.get('page', 1))
        except ValueError:
            page = 1
        row_from = page * 10
        row_to = row_from + 10
        return row_from, row_to


class DatasetDownloadView(View):
    def get(self, request, *args, **kwargs):
        dataset = get_object_or_404(Dataset, pk=self.kwargs['pk'])
        # We could use apache/nginx/etc for serve files
        response = HttpResponse(dataset.file, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{dataset.filename()}"'
        return response
