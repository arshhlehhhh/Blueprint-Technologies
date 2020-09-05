from django.conf.urls import url
from getArticles import views



urlpatterns = [
    url(r'^$', views.MainPage.as_view())
]