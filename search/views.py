import pprint
import re
import nltk
#import enchant
from rest_framework_mongoengine.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from search.models import Answer, Result
from search.serializers import AnswerSerializer, ResultSerializer
from .apps import es_search
from elasticsearch_dsl.query import Match
from elasticsearch_dsl import Q
#from enchant.checker import SpellChecker


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

            q_nltk = ''
            #d = enchant.Dict('en_US')
            symbol_set = ['?', '.']

            size_nltk_q=0
            definition_q=False
            
            if 'passthrough' not in self.request.GET:
                if 'what' in query: 
                    definition_q = True
			
                tokens = nltk.word_tokenize(query)
                pprint.pprint(tokens)
                stopwords = nltk.corpus.stopwords.words('english')
                nltk_query = list(set(tokens) - set(stopwords))
                nltk_query = list(set(nltk_query) - set(symbol_set))
                size_nltk_q = len(nltk_query) #will use this for weight calculation
                q_nltk = ' '.join(nltk_query)
                #spell check
                #chkr = SpellChecker("en_US", q_nltk)
                #for err in chkr:
                #    pprint.pprint(err.word + "<---- spell error , suggest: ")
                #    pprint.pprint(d.suggest(err.word))

                pprint.pprint(q_nltk)
                pprint.pprint(size_nltk_q)

            #test spell

            # https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#_reserved_characters
            if q_nltk:
                query = ESCAPE_RE.sub(r'\\\1', q_nltk)
                if definition_q:
                    query = Q({"bool":{"must":[{ "match":{"tags":"definition"}},{"match":{"value":q_nltk}}]}})
                else: query = Q({"bool" : {"must" : {"match" : {"value" : {"query" : query}}}}})
            else:
                query = ESCAPE_RE.sub(r'\\\1', query)
                query = Q({"query_string" : {"query" : query}})

            # https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html
            # https://www.elastic.co/guide/en/elasticsearch/reference/current/full-text-queries.html


            query = es_search.query(query)[0:10]
            response = query.execute(ignore_cache=False)

            pprint.pprint(query.to_dict()) # debug query
        
            #no result return from definition question query, just return the best match
            if len(response) == 0 and definition_q:
                pprint.pprint('research')
                query = Q({"bool" : {"must" : {"match" : {"value" : {"query" : q_nltk}}}}})
                query = es_search.query(query)[0:10]
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
