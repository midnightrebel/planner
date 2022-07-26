from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import CodeGenerateView, UserMeetingViewSet, UserRetrieveView
schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)
urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', CodeGenerateView.as_view()),
    path('meeting/<str:code>',UserRetrieveView.as_view()),
    path('<str:meeting__code>/', UserMeetingViewSet.as_view())
]
