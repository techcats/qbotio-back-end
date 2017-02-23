from django.conf.urls import url
import rest_framework
import rest_framework_mongoengine

from . import views

searchRouter = rest_framework.routers.SimpleRouter()
searchRouter.register(r'search', views.SearchView, base_name='search-list')

answerRouter = rest_framework_mongoengine.routers.SimpleRouter()
answerRouter.register(r'answer', views.AnswerView)

urlpatterns = [
]
