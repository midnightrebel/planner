from django.db.models import Q
from django.utils.timezone import localtime
from django_filters import rest_framework as filters


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass



class DataFilter(filters.FilterSet):
    code = CharFilterInFilter(field_name='meeting_id__code', lookup_expr='in')