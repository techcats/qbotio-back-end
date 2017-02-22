from rest_framework_mongoengine import serializers
from search.models import Result

class ResultSerializer(serializers.DocumentSerializer):
    """
    Serializer for Result model
    """
    class Meta:
        model = Result
        fields = '__all__'
