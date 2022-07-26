from django.urls import path, include
from .views import CodeGenerateView,UserMeetingViewSet,UserRetrieveView

urlpatterns = [
    path('code/',CodeGenerateView.as_view()),
    path('',UserMeetingViewSet.as_view()),
    path('<str:code>/',UserRetrieveView.as_view())
]
