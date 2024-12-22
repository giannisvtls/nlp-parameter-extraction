from rest_framework import generics, permissions
from rest_framework.schemas.openapi import AutoSchema
from api.serializers.metadata import ApiMetadataSerializer
from app.metadata import PROJECT_NAME
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, filters
from django.views.generic import TemplateView
from .models import EfoTerm
from api.serializers.api import EfoTermSerializer

class IndexView(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ApiMetadataSerializer
    schema = AutoSchema(operation_id_base='ApiMetadata')
    def get_object(self):
        return {
            'description': f"{PROJECT_NAME} API",
            'version': "0.0.1"
        }

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class EfoTermViewSet(viewsets.ModelViewSet):
    queryset = EfoTerm.objects.all().distinct()
    serializer_class = EfoTermSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['term', 'synonyms__label']
    
    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('synonyms')
        return queryset

class ChatRoomView(TemplateView):
    template_name = 'chat_room.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_name'] = kwargs.get('room_name')
        context['api_base_url'] = self.request.build_absolute_uri('/')[:-1]
        return context

class WSCheckView(TemplateView):
    template_name = 'ws_check.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ws_url'] = self.request.build_absolute_uri('/')[:-1].replace('http', 'ws')
        return context