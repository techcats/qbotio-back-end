from rest_framework_mongoengine import serializers
from search.models import Result

class ResultSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Result
        fields = '__all__'
