from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ResultList.as_view(), name='index'),
]
