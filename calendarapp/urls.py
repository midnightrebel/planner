from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RangeViewSet, CodeGenerateView,UserMeetingViewSet

router = DefaultRouter()
router.register('getrange', RangeViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('code/',CodeGenerateView.as_view()),
    path('<str:code>/',UserMeetingViewSet.as_view())
]
