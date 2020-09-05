from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from articles.models import Articles
from articles.serializers import ArticlesSerializer
from rest_framework.decorators import api_view

@api_view(['GET'])
def articles_list(request):
    articles = Articles.objects.all()

    articles_serializer = ArticlesSerializer(articles, many=True)
    return JsonResponse(articles_serializer.data, safe=False)