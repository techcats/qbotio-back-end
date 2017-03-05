from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer
from search.models import Question, Answer

class QuestionSerializer(DocumentSerializer):
    """
    Serializes results
    """
    class Meta:
        model = Question
        fields = '__all__'

class AnswerSerializer(DocumentSerializer):
    """
    Serializes results
    """
    class Meta:
        model = Answer
        fields = '__all__'

class ResultSerializer(serializers.Serializer):
    value = serializers.CharField()
    source = serializers.CharField(required=False)
    origin = serializers.CharField(required=False)
    score = serializers.FloatField()

