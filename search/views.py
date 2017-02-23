from rest_framework_mongoengine.viewsets import ModelViewSet
import rest_framework_mongoengine.serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from elasticsearch_dsl.query import Match
from search.models import Answer
from search.serializers import ResultSerializer
from .apps import es_search

class ResultsViewSet(ModelViewSet):
    """
    View answers
    """
    queryset = Answer.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        """
        Returns a list of answers from a string query
        """
        query = request.GET.get('q', '')
        if query == '':
            # Return all unrank results
            serializer = self.get_serializer(Answer.objects.all(), many=True)
        else:
            # https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html
            # https://www.elastic.co/guide/en/elasticsearch/reference/current/full-text-queries.html
            query = es_search.query(Match(value={'query': query}))[0:10]
            response = query.execute()
            print(query.to_dict())
            print(response.to_dict())
            # Dummy answers
            results = [
                Answer(value="Answer 1"),
                Answer(value="Answer 2"),
                Answer(value="Answer 3"),
            ]
            serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create one or more answers
        """
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=data, many=True)
        else:
            serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

