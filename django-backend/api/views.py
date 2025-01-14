from rest_framework import generics, permissions, viewsets, filters, status
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.response import Response
from rest_framework.decorators import action
from api.serializers.metadata import ApiMetadataSerializer
from app.metadata import PROJECT_NAME
from rest_framework.pagination import PageNumberPagination
from django.views.generic import TemplateView
from .models import User, Document
from api.serializers.api import UserSerializer, DocumentSerializer
from api.services.rag_service import RAGService

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = (permissions.AllowAny,)
    
    @action(detail=False, methods=['post'])
    async def add_with_embedding(self, request):
        content = request.data.get('content')
        if not content:
            return Response(
                {'error': 'Content is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        rag_service = RAGService()
        document = await rag_service.add_document(content)
        
        return Response({
            'id': document.id,
            'content': document.content,
            'created_at': document.created_at
        })

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

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'iban']

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
