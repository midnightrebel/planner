import random
import string

from django.db import connection, transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import DataFilter
from .models import Meeting, UserDataRange
from .serializers import CreateRangeSerializer, ListRangeSerializer, MeetingListSerializer


class CodeGenerateView(APIView):
    def get(self,request):
        with connection.cursor() as cursor:
            while True:
                code = ''.join(random.choice(string.ascii_letters) for _ in range(7))
                try:
                    cursor.execute(
                        "select not exists(select * from calendarapp_meeting where code = %s ) as available;",
                        [code]
                    )
                except Exception as e:
                    return Response({'error': e})
                (available,) = cursor.fetchone()
                if available:
                    Meeting.objects.create(code=code)
                    return Response({'code': code})


class UserRetrieveView(generics.RetrieveUpdateAPIView):
    serializer_class = MeetingListSerializer
    queryset = Meeting.objects.all()
    lookup_field = 'code'

class UserMeetingViewSet(generics.ListCreateAPIView):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DataFilter
    serializer_class = ListRangeSerializer
    queryset = UserDataRange.objects.select_related('meeting_id')

    # POST /<code>
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = CreateRangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)
        with connection.cursor() as cursor:
            code = serializer.data["meeting_id"]
            try:
                cursor.execute(
                    "update public.calendarapp_meeting set ranges = calculate_shedule(%s) where code = %s;",
                    [code, code]
                )
            except Exception as e:
                cursor = connection.cursor()
                print(e)
                return Response(status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data)
