from django.conf import settings
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import permissions
from rest_framework.schemas import get_schema_view
from rest_framework.routers import DefaultRouter
from .views import (
    EfoTermViewSet,
    IndexView,
    ChatRoomView,
    WSCheckView
)
from app.metadata import PROJECT_NAME

router = DefaultRouter()
router.register(r'api/efoterms', EfoTermViewSet)

urlpatterns = [
    path('', IndexView.as_view(), name='root'),
    path('', include(router.urls)),
    path('chat/<str:room_name>/', ChatRoomView.as_view(), name='chat_room'),
    path('ws-check/', WSCheckView.as_view(), name='ws_check'),
]

if settings.DEV_DOCS:
    urlpatterns += [
        path('api/openapi', get_schema_view(
            title="NLP Assignement Parameter Extraction",
            public=True,
            permission_classes=(permissions.AllowAny,)
        ), name='openapi-schema'),
        path('api/docs', TemplateView.as_view(
            template_name='swagger-ui.html',
            extra_context=dict(title=PROJECT_NAME, schema_url='openapi-schema')
        ), name='swagger-ui'),
    ]