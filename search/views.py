import pprint
import re
import nltk
import string
#import enchant
from rest_framework_mongoengine.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from search.models import  Question, QuestionResult, Answer, AnswerResult
from search.serializers import QuestionSerializer, AnswerSerializer, ResultSerializer
from .apps import question_search, answer_search
from elasticsearch_dsl.query import Match
from elasticsearch_dsl import Q
#from enchant.checker import SpellChecker


class QuestionView(ModelViewSet):
    """
    Private API for viewing and updating questions
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Create one or more Questions
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

class SuggestView(GenericViewSet):
    """
    Public API for suggesting questions
    """
    serializer_class = ResultSerializer

    def get_queryset(self):
        if 'q' in self.request.GET:
            query = self.request.GET.get('q', '')
            query = Q({"match_phrase_prefix" : {"value" : query}})
            query = question_search.query(query)[0:5]
            response = query.execute(ignore_cache=False)
            return [QuestionResult(hit.value, hit.meta.score) for hit in response]
        return []
        
    def list(self, request):
        """
        Returns a list of suggestions from a string query
        """
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class SearchView(GenericViewSet):
    """
    Public API for searching for answers
    """
    serializer_class = ResultSerializer


    def get_queryset(self):
        if 'q' in self.request.GET:
            query = self.request.GET.get('q', '')
            #query = query.lower()

            q_nltk = ''
            #d = enchant.Dict('en_US')
            symbol_set = ['?', '.']
            #question w/ capital, becuase we can't make string to be lower case, because it impact the query. So we need to manually remove question what to wrote with capital letter. In the stopwords contain only lower cases
            #question_set = ['What', 'How', 'When', 'Do', 'Does', 'Which', 'Why']
            question_set = ['What'] #this one make overall evaluation result better

            size_nltk_q=0
            definition_q=False
            
            if 'passthrough' not in self.request.GET:
                
                stopwords = nltk.corpus.stopwords.words('english')
                tokens = nltk.word_tokenize(query)
                
                if 'experimental' in self.request.GET:
                
                    if 'what' in query or 'What' in query: 
                        definition_q = True

                    #TAG PART OF SPEECH FOR KEY WORDS, The tagger need whole sentence in order to determine type of words
                    tagged = nltk.pos_tag(tokens)
                    pprint.pprint(tagged)

                    adj_list = []
                    noun_list = []
                    other_list = []

                    for i in range(0,len(tagged)):
                        if tagged[i][1]=='NN' or tagged[i][1]=='NNS':
                            noun_list.append(tagged[i][0])
                        elif tagged[i][1]=='JJ' or tagged[i][1]=='VBN':
                            adj_list.append(tagged[i][0])
                        else :
                            other_list.append(tagged[i][0])

                    pprint.pprint(adj_list)
                    pprint.pprint(noun_list)
                    pprint.pprint(other_list)

                    other_list = list(set(other_list) - set(stopwords))
                    other_list = list(set(other_list) - set(symbol_set))
                    other_list = list(set(other_list) - set(question_set))

                    pprint.pprint(other_list)

                    if len(adj_list) > 0 :
                        must_m_q = ' '.join(adj_list)
                        should_m_q = noun_list + other_list
                        should_m_q = ' '.join(should_m_q)
                    else :
                        must_m_q = ' '.join(noun_list)
                        should_m_q = ' '.join(other_list)

                    #for experimental
                    q_nltk = ' '.join([must_m_q, should_m_q])

                    #nltk_query = list(set(nltk_query) - set(question_set))
                    #size_nltk_q = len(nltk_query) #will use this for weight calculation

                    #spell check
                    #chkr = SpellChecker("en_US", q_nltk)
                    #for err in chkr:
                    #    pprint.pprint(err.word + "<---- spell error , suggest: ")
                    #    pprint.pprint(d.suggest(err.word))

                    #pprint.pprint(q_nltk)
                    #pprint.pprint(size_nltk_q)
                else:
                    #REMOVE UNNECCESSARY WORDS
                    
                    nltk_query = list(set(tokens) - set(stopwords))
                    nltk_query = list(set(nltk_query) - set(symbol_set))

                    q_nltk = ' '.join(nltk_query)
                    

            #test spell

            # https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#_reserved_characters
            if q_nltk:
                query = ESCAPE_RE.sub(r'\\\1', q_nltk)
                if definition_q:
                    #query = Q({"bool":{"must":[{ "match":{"tags":"definition"}},{"match":{"value":q_nltk}}]}})
                    query = Q({"bool":{"must":[{ "match":{"tags":"definition"}},{"match":{"value":must_m_q}}], "should" : [{"match" : {"value" : should_m_q}}]}})
                else: 
                    query = Q({"bool" : {"must" : {"match" : {"value" : {"query" : query}}}}})
            else:
                query = ESCAPE_RE.sub(r'\\\1', query)
                query = Q({"query_string" : {"query" : query}})

            # https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html
            # https://www.elastic.co/guide/en/elasticsearch/reference/current/full-text-queries.html


            query = answer_search.query(query)[0:10]
            response = query.execute(ignore_cache=False)

            pprint.pprint(query.to_dict()) # debug query
        
            #no result return from definition question query, just return the best match
            if len(response) == 0 and definition_q:
                pprint.pprint('research')
                query = Q({"bool" : {"must" : {"match" : {"value" : {"query" : q_nltk}}}}})
                query = answer_search.query(query)[0:10]
                response = query.execute(ignore_cache=False)
                pprint.pprint(query.to_dict()) # debug query

            return [
                AnswerResult(
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
