from django.apps import AppConfig
from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

es_settings = settings.ELASTICSEARCH
es_search = Search(using=Elasticsearch(
    [es_settings['HOST']],
    http_auth=(es_settings['USER'], es_settings['PASSWORD']),
    port=es_settings['PORT'],
), index='qbotio')

class SearchConfig(AppConfig):
    name = 'search'
