from rest_framework_mongoengine.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from search.models import Answer
from search.serializers import ResultSerializer

class ResultsViewSet(ModelViewSet):
    """
    View answers
    """
    serializer_class = ResultSerializer
    queryset = Answer.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        """
        Returns a list of answers from a string query
        """
        query = request.GET.get('q', '')
        if query == '':
            # Return all unrank results
            serializer = ResultSerializer(Answer.objects.all(), many=True)
            return Response(serializer.data)
        # Dummy answers
        results = [
            Answer(value="Answer 1"),
            Answer(value="Answer 2"),
            Answer(value="Answer 3"),
        ]
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)
