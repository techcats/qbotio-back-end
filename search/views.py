import pprint
import re
import nltk
from rest_framework_mongoengine.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from search.models import Answer, Result
from search.serializers import AnswerSerializer, ResultSerializer
from .apps import es_search

class AnswerView(ModelViewSet):
    """
    Private API for viewing and updating answers
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

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


ESCAPE_RE = re.compile(r'([+-=&|><(){}[\]\^"~\?:\\\/])')

class SearchView(GenericViewSet):
    """
    Public API for searching for answers
    """
    serializer_class = ResultSerializer

    def get_queryset(self):
        if 'q' in self.request.GET:
            query = self.request.GET.get('q', '')
            # https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#_reserved_characters
            query = ESCAPE_RE.sub(r'\\\1', query)

            q_nltk = ''
            if 'passthrough' not in self.request.GET:
                tokens = nltk.word_tokenize(query)
                pprint.pprint(tokens)
                stopwords = nltk.corpus.stopwords.words('english')
                nltk_query = list(set(tokens) - set(stopwords))
                pprint.pprint(nltk_query)

                q_nltk = ' '.join(nltk_query)
                pprint.pprint(q_nltk)

            # https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html
            # https://www.elastic.co/guide/en/elasticsearch/reference/current/full-text-queries.html
            if q_nltk:
                query = es_search.query('query_string', query=q_nltk)[0:10]
            else:
                query = es_search.query('query_string', query=query)[0:10]

            response = query.execute(ignore_cache=False)

            pprint.pprint(query.to_dict()) # debug query
            return [
                Result(
                    hit.value,
                    hit.source,
                    hit.origin,
                    hit.meta.score
                )
                for hit in response
            ]
        return []

    def list(self, request):
        """
        Returns a list of answers from a string query
        """
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)
