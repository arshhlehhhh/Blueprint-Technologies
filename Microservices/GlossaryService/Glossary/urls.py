from django.conf.urls import url 
from Glossary import views 
 
urlpatterns = [ 
    url(r'^api/getallglossary$', views.glossary_list),
    url(r'^api/getglossary/(?P<pk>[0-9]+)$', views.glossary_detail)
]
