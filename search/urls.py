from django.conf.urls import url
from . import views
from rest_framework_mongoengine.routers import SimpleRouter

searchRouter = SimpleRouter()
searchRouter.register(r'search', views.ResultsViewSet)

urlpatterns = [
]
