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
        dataset = get_object_or_404(Dataset, pk=self.kwargs['pk'])
        row_from, row_to = self.get_rows_range(request)

        return JsonResponse({
            'success': 200,
            'rows': list(petl.fromcsv(dataset.file).rowslice(row_from, row_to))[1:]
        })

    def get_rows_range(self, request):
        try:
            page = int(request.GET.get('page', 1))
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
