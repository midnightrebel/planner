from django.contrib.postgres.forms import RangeWidget
from django.forms import SplitDateTimeWidget
from drf_extra_fields.fields import DateTimeRangeField
from rest_framework import serializers

from .models import Meeting, UserDataRange





class MeetingListSerializer(serializers.ModelSerializer):
    ranges = serializers.ListField(child=DateTimeRangeField())

    class Meta:
        model = Meeting
        fields = ['ranges']


class CreateRangeSerializer(serializers.ModelSerializer):
    meeting_id = serializers.SlugRelatedField(queryset=Meeting.objects.all(), slug_field='code', read_only=False)
    user_ranges = DateTimeRangeField()

    class Meta:
        model = UserDataRange
        fields = ['meeting_id', 'username', 'user_ranges']

    def create(self, validated_data):
        answer, created = UserDataRange.objects.update_or_create(
            username=validated_data.get('username'),
            user_ranges=validated_data.get('user_ranges'),
            meeting_id=validated_data.get('meeting_id'),
            defaults={'meeting_id': validated_data.get('meeting_id')})
        return answer


class ListRangeSerializer(serializers.ModelSerializer):
    meeting_id = serializers.SlugRelatedField(queryset=Meeting.objects.all(), slug_field='code', read_only=False)

    class Meta:
        model = UserDataRange
        fields = ['meeting_id', 'username', 'user_ranges']
        widgets = {'user_ranges': RangeWidget(SplitDateTimeWidget())}
