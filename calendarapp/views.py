import random
import string

from django.db import connection, transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import DataFilter
from .models import Meeting, UserDataRange
from .serializers import CreateRangeSerializer, ListRangeSerializer, CreateRetrieveRangeSerializer


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
    serializer_class = CreateRetrieveRangeSerializer
    queryset = UserDataRange.objects.select_related('meeting_id')
    lookup_field = 'meeting_id__code'

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        meeting = Meeting.objects.filter(code=kwargs.get('meeting_id__code')).first()
        print(meeting)

        if not meeting:
            return Response({'error': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.update({'meeting_id_id': meeting.id})
        serializer.save()

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "update public.calendarapp_meeting set ranges = calculate_shedule(%s) where code = %s;",
                    [meeting.code, meeting.code]
                )
            except Exception as e:
                print(e)
                return Response({'error': e}, status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)

class UserMeetingViewSet(generics.ListCreateAPIView):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DataFilter
    serializer_class = ListRangeSerializer
    queryset = UserDataRange.objects.select_related('meeting_id')

    # POST /<code>
    def post(self, request, *args, **kwargs):
        serializer = CreateRangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        with connection.cursor() as cursor:
            code = serializer.data["meeting_id"]
            try:
                cursor.execute(
                    "update public.calendarapp_meeting set ranges = calculate_shedule(%s) where code = %s;",
                    [code, code]
                )
                transaction.commit()
            except Exception as e:
                cursor = connection.cursor()
                print(e)
                return Response(status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data)
