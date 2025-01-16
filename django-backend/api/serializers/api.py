from rest_framework import serializers
from api.models import User, Document

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'iban', 'balance']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'content', 'created_at']
        read_only_fields = ['embedding']
