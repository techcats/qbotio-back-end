from django.apps import AppConfig
from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

es_settings = settings.ELASTICSEARCH
es_http_auth = None
if 'USER' in es_settings:
    es_http_auth = (es_settings['USER'], es_settings['PASSWORD'])
es_client = Elasticsearch([es_settings['HOST']], http_auth=es_http_auth, port=es_settings['PORT'])

question_search = Search(using=es_client, index='qbotio', doc_type='question')
answer_search = Search(using=es_client, index='qbotio', doc_type='answer')

class SearchConfig(AppConfig):
    name = 'search'
