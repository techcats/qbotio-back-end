from rest_framework_mongoengine.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from search.models import Result
from search.serializers import ResultSerializer


class ResultsViewSet(ModelViewSet):
    """
    View answers
    """
    serializer_class = ResultSerializer
    queryset = Result.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        """
        Returns a list of answers from a string query
        """
        results = [
            Result(answer="Answer 1"),
            Result(answer="Answer 2"),
            Result(answer="Answer 3"),
        ]
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)
