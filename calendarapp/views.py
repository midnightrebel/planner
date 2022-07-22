import json
import random
import string

from django.db import connection, transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import DataFilter
from .models import Meeting, UserDataRange
from .serializers import CreateRangeSerializer, ListRangeSerializer


class CodeGenerateView(APIView):
    def get(self,request):
        cursor = connection.cursor()
        with cursor:
            while True:
                code = ''.join(random.choice(string.ascii_letters) for i in range(7))
                try:
                    cursor.execute(
                        "select not exists(select * from calendarapp_meeting where code = %s ) as available;",
                        [code]
                    )

                except:
                    cursor = connection.cursor()
                (available, ) = cursor.fetchone()
                if available:
                    Meeting.objects.create(code=code)
                    return Response({'code': code})

class UserMeetingViewSet(generics.GenericAPIView):
    serializer_class = ListRangeSerializer
    queryset = Meeting.objects.all()

    def get(self,request,*args,**kwargs):
        return Response(status.HTTP_200_OK)

    # POST /<code>
    def post(self, request, *args, **kwargs):
        cursor = connection.cursor()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        with cursor:
            code = kwargs['code']
            try:
                cursor.execute(
                    "update public.calendarapp_meeting set ranges = calculate_shedule(%s) where code = %s;",
                    [code, code]
                )
                transaction.commit()
            except:
                cursor = connection.cursor()
                return Response(status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data)


class RangeViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DataFilter
    queryset = UserDataRange.objects.select_related('meeting_id')
    serializer_class = ListRangeSerializer
    def create(self, request, *args, **kwargs):
        serializer = CreateRangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)