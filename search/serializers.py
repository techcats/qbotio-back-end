from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer
from search.models import Answer

class AnswerSerializer(DocumentSerializer):
    """
    Serializes results
    """
    class Meta:
        model = Answer
        fields = '__all__'

class ResultSerializer(serializers.Serializer):
    value = serializers.CharField()
    source = serializers.CharField()
    origin = serializers.CharField()
    score = serializers.FloatField()

