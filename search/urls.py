from django.conf.urls import url
import rest_framework
import rest_framework_mongoengine

from . import views

searchRouter = rest_framework.routers.SimpleRouter()
searchRouter.register(r'search', views.SearchView, base_name='search-list')
searchRouter.register(r'suggest', views.SuggestView, base_name='suggest-list')

apiRouter = rest_framework_mongoengine.routers.SimpleRouter()
apiRouter.register(r'question', views.QuestionView)
apiRouter.register(r'answer', views.AnswerView)

urlpatterns = [
]
