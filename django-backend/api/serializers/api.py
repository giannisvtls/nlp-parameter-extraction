from rest_framework import serializers
from api.models import EfoTerm, EfoTermSynonym

class EfoTermSynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = EfoTermSynonym
        fields = ['id', 'label']

class EfoTermSerializer(serializers.ModelSerializer):
    synonyms = EfoTermSynonymSerializer(many=True, read_only=True)

    class Meta:
        model = EfoTerm
        fields = ['id', 'term', 'synonyms']