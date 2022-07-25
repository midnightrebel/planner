from django.contrib.postgres.forms import RangeWidget
from django.forms import SplitDateTimeWidget
from rest_framework import serializers
from .models import Meeting, UserDataRange
from drf_extra_fields.fields import DateTimeRangeField
from psycopg2._range import DateTimeTZRange

class CreateRetrieveRangeSerializer(serializers.ModelSerializer):
    meeting_id = serializers.StringRelatedField(read_only=True)
    user_ranges = DateTimeRangeField(child_attrs={"bounds":"[]"})


    def update(self, instance, validated_data):

        instance.username = validated_data.get('username')
        instance.user_ranges = validated_data.get('user_ranges')
        return instance

    class Meta:
        model = UserDataRange
        fields = ['meeting_id', 'username', 'user_ranges']


class CreateRangeSerializer(serializers.ModelSerializer):
    meeting_id = serializers.SlugRelatedField(queryset=Meeting.objects.all(), slug_field='code', read_only=False)

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
