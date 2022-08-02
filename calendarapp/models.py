import uuid
from datetime import timedelta

from django.contrib.postgres.fields import (DateTimeRangeField,
                                            ArrayField,
                                            )
from django.db import models
from django.utils import timezone
from psycopg2._range import DateTimeTZRange


def next_ten_years():
    now = timezone.now()
    return DateTimeTZRange(now, now + timedelta(days=3652), bounds='[]')


class Meeting(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, )
    ranges = ArrayField(base_field=DateTimeRangeField(), null=True)

    def __str__(self):
        return self.code


class UserDataRange(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name="meetings", db_index=True)
    username = models.CharField(max_length=255)
    user_ranges = ArrayField(base_field=DateTimeRangeField(), null=True, )

    def __str__(self):
        return self.username
