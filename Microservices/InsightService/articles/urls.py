from django.conf.urls import url 
from articles import views 
 
urlpatterns = [ 
    url(r'^api/getarticles$', views.articles_list)
]
