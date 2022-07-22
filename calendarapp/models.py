from django.db import models
from django.contrib.postgres.fields import DateTimeRangeField
from django.contrib.postgres.fields import ArrayField
from psycopg2._range import DateTimeTZRange
from django.utils import timezone
from datetime import timedelta

def next_ten_years():
    now = timezone.now()

    # use a more accurate version of "10 years" if you need it
    return DateTimeTZRange(now, now + timedelta(days=3652))

class Meeting(models.Model):
    code = models.CharField(unique=True, max_length=7,default='',db_index=True)
    created_at = models.DateTimeField(auto_now_add=True,)
    ranges = ArrayField(base_field=DateTimeRangeField(),null=True,)
    def __str__(self):
        return self.code

class UserDataRange(models.Model):
    meeting_id = models.OneToOneField(Meeting,on_delete=models.CASCADE)
    username = models.CharField(max_length=255,unique=True)
    user_ranges = DateTimeRangeField(default=next_ten_years)
    def __str__(self):
        return self.username

