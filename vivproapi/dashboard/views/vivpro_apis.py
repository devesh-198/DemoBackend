from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from vivproapi.dashboard.models import DanceProfile

class DanceProfileListView(APIView):
    per_page_count = 10
    default_sort_by = 'danceability'

    table_headers = [
        {'unique_name': 'id', 'name': 'Ids', 'type': 'string'},
        {'unique_name': 'title', 'name': 'Title', 'type': 'string'},
        {'unique_name': 'danceability', 'name': 'Danceability', 'type': 'number'},
        {'unique_name': 'energy', 'name': 'Energy', 'type': 'number'},
        {'unique_name': 'mode', 'name': 'Mode', 'type': 'number'},
        {'unique_name': 'acousticness', 'name': 'Acousticness', 'type': 'number'},
        {'unique_name': 'tempo', 'name': 'Tempo', 'type': 'number'},
        {'unique_name': 'duration_ms', 'name': 'Duration', 'type': 'number'},
        {'unique_name': 'num_sections', 'name': 'Num Sections', 'type': 'number'},
        {'unique_name': 'num_segments', 'name': 'Num Segments', 'type': 'number'},
        {'unique_name': 'rating', 'name': 'Rating', 'type': 'rating'},
    ]

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.status = status.HTTP_200_OK
        self.head = {'status': 200, 'statusDescription': 'Success'}
        self.body = {'isNextPage': False}
        self.context_dict = {'head': self.head, 'body': self.body}

        return super(DanceProfileListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.make_context_dict()

        return Response(self.context_dict, status=self.status)

    def make_context_dict(self):
        """Building the table data"""
        try:
            self.parse_input()
            dance_profile_list = self.get_qs()
            table_data = []

            for song in dance_profile_list:
                data = []

                for header in self.table_headers:
                    unique_name = header.get('unique_name')
                    data.append(getattr(song, unique_name, None))

                table_data.append(data)

            self.body['tableHeaders'] = self.table_headers
            self.body['tableData'] = table_data

            self.body['scatteredChart'] = self.build_scatter_chart_data()
            self.body['histogramChart'] = self.build_histogram_chart_data()
            self.body['barchart'] = self.build_barchart_data()
        except Exception as e:
            self.head['status'] = 500
            self.head['statusDescription'] = str(e)
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def parse_input(self):
        """Read the input from request"""
        self.page_number = int(self.request.GET.get('pageNumber', 0))
        self.per_page_count = int(self.request.GET.get('perPageCount', self.per_page_count))
        self.sort_by = self.request.GET.get('sortBy', self.default_sort_by)
        self.order = self.request.GET.get('order', 'DESC')
        self.song_title = self.request.GET.get('songTitle', None)

    def get_qs(self):
        """
            #### Build the queryset.
            * handle pagination and sorting
        """
        _start = 0
        _end = 10

        if self.per_page_count and self.page_number is not None:
            _start = self.per_page_count * self.page_number
            _end = self.per_page_count * (self.page_number + 1)

            # Fetching 1 extra entry to decide if nextPage is there.
            _end = _end + 1

        _sort_by = self.sort_by

        if self.order == 'DESC':
            _sort_by = f'-{self.sort_by}'

        qs = DanceProfile.objects.all()

        if self.song_title:
            qs = DanceProfile.objects.filter(title__icontains=self.song_title)

        dance_profiles = list(qs.order_by(_sort_by)[_start:_end])

        # import ipdb; ipdb.set_trace()

        if len(dance_profiles) > self.per_page_count:
            dance_profiles.pop()
            self.body['isNextPage'] = True

        self.body['pageNumber'] = self.page_number
        self.body['perPageCount'] = self.per_page_count
        self.body['sortBy'] = self.sort_by
        self.body['sortOrder'] = self.order

        return dance_profiles

    def build_scatter_chart_data(self):
        """Building scattered chart data."""

        _sort_by = self.sort_by

        if self.order == 'DESC':
            _sort_by = f'-{self.sort_by}'

        danceability_list = list(DanceProfile.objects.all().order_by(_sort_by).values("danceability"))

        scattered_chart = []

        for danceability in danceability_list:
            val = danceability.get("danceability", 0)
            scattered_chart.append([val, val])

        return scattered_chart

    def build_histogram_chart_data(self):
        """Building the histogram chart data using duration_ms"""

        _sort_by = self.sort_by

        if self.order == 'DESC':
            _sort_by = f'-{self.sort_by}'

        duration_ms_list = list(DanceProfile.objects.all().order_by(_sort_by).values("duration_ms"))

        histogram_chart = []

        for duration in duration_ms_list:
            histogram_chart.append(duration.get("duration_ms", 0)/1000)

        return histogram_chart

    def build_barchart_data(self):
        """Building the barchart data for the acousticness and tempo value"""

        _sort_by = self.sort_by

        if self.order == 'DESC':
            _sort_by = f'-{self.sort_by}'

        barchart_list = list(DanceProfile.objects.all().order_by(_sort_by).values("title", "acousticness", "tempo"))

        categories = []
        acousticness = []
        tempo = []

        for data in barchart_list:
            categories.append(data.get("title", ''))
            acousticness.append(data.get("acousticness", ''))
            tempo.append(data.get("tempo", ''))

        barchart_data = {
            "categories": categories,
            "acousticness": acousticness,
            "tempo": tempo,
        }

        return barchart_data


@api_view(["POST"])
def setStarRating(request, *args, **kwargs):
    """Seting the rating of songs"""

    head = {'status': 200, 'statusDescription': 'Success'}
    # body = {'isNextPage': False}
    context_dict = {'head': head}

    rating = request.data.get('rating')
    song_id = request.data.get('songId')

    try:
        DanceProfile.objects.filter(id=song_id).update(rating=rating)
    except Exception as e:
        head['status'] = 500
        head['statusDescription'] = str(e)

        return Response(context_dict, status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(context_dict, status=status.HTTP_200_OK)

