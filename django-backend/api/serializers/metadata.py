from rest_framework import serializers

class ApiBuildSerializer(serializers.Serializer):
    branch = serializers.CharField(read_only=True, allow_blank=True, default='')
    commit = serializers.CharField(read_only=True, allow_blank=True, default='')
    date = serializers.DateTimeField(read_only=True, allow_null=True, default=None)

    def update(self, instance, validated_data):
        raise Exception("Not supported")

    def create(self, validated_data):
        raise Exception("Not supported")


class ApiMetadataSerializer(serializers.Serializer):
    description = serializers.CharField(read_only=True, allow_blank=True, default='')
    version = serializers.CharField(read_only=True, allow_blank=True, default='')

    def update(self, instance, validated_data):
        raise Exception("Not supported")

    def create(self, validated_data):
        raise Exception("Not supported")