from django.contrib.postgres.forms import RangeWidget
from django.forms import SplitDateTimeWidget
from rest_framework import serializers
from .models import Meeting, UserDataRange
from drf_extra_fields.fields import DateTimeRangeField
from psycopg2._range import DateTimeTZRange



class MeetingListSerializer(serializers.ModelSerializer):
    ranges = serializers.ListField(child=DateTimeRangeField())


    class Meta:
        model = Meeting
        fields = ['ranges']


class CreateRangeSerializer(serializers.ModelSerializer):
    meeting_id = serializers.SlugRelatedField(queryset=Meeting.objects.all(), slug_field='code', read_only=False)
    user_ranges = DateTimeRangeField()
    def create(self, validated_data, *args, **kwargs):
        return UserDataRange.objects.create(**validated_data)

    class Meta:
        model = UserDataRange
        fields = ['meeting_id', 'username', 'user_ranges']


class ListRangeSerializer(serializers.ModelSerializer):
    meeting_id = serializers.SlugRelatedField(queryset=Meeting.objects.all(), slug_field='code', read_only=False)

    class Meta:
        model = UserDataRange
        fields = ['meeting_id', 'username', 'user_ranges']
        widgets = {'user_ranges': RangeWidget(SplitDateTimeWidget())}
