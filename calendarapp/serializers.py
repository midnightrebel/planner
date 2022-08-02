from django.contrib.postgres.forms import RangeWidget
from django.forms import SplitDateTimeWidget
from .fields import DateTimeRangeField
from rest_framework import serializers

from .models import Meeting, UserDataRange


class MeetingListSerializer(serializers.ModelSerializer):
    ranges = serializers.ListField(child=serializers.ListField(child=DateTimeRangeField()))

    class Meta:
        model = Meeting
        fields = ['ranges']


class CreateRangeSerializer(serializers.ModelSerializer):
    meeting = serializers.SlugRelatedField(slug_field='code', read_only=True)
    user_ranges = serializers.ListField(child=DateTimeRangeField())
    class Meta:
        model = UserDataRange
        fields = ['meeting', 'username', 'user_ranges']


    def create(self, validated_data, *args, **kwargs):
        answer, created = UserDataRange.objects.update_or_create(
            username=validated_data.get('username'),
            user_ranges=validated_data.get('user_ranges'),
            meeting = validated_data.get('meeting'))
        # defaults = {'meeting__code': validated_data.get('meeting__code')}
        return answer


class ListRangeSerializer(serializers.ModelSerializer):
    meeting = serializers.SlugRelatedField(queryset=Meeting.objects.all(),slug_field='code', read_only=False)

    class Meta:
        model = UserDataRange
        fields = ['meeting', 'username', 'user_ranges']
        widgets = {'user_ranges': RangeWidget(SplitDateTimeWidget())}
