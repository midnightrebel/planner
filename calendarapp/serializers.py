from django.contrib.postgres.forms import RangeWidget
from django.forms import SplitDateTimeWidget
from rest_framework import serializers
from .models import Meeting,UserDataRange



class CreateRangeSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return UserDataRange.objects.create(**validated_data)

    class Meta:
        model = UserDataRange
        fields = ['meeting_id','username','user_ranges']

class ListRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDataRange
        fields = ['username','user_ranges']
        widgets = { 'user_ranges': RangeWidget(SplitDateTimeWidget()) }
