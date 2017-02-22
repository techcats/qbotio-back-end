from rest_framework_mongoengine.serializers import DocumentSerializer
from search.models import Answer

class ResultSerializer(DocumentSerializer):
    """
    Serializes results
    """
    class Meta:
        model = Answer
        fields = '__all__'
