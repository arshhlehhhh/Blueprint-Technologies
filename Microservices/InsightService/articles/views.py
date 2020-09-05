from django.shortcuts import render
from django.http import HttpResponse
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

@api_view(['POST'])
def articles_push(request):
    check = True
    articles_data = JSONParser().parse(request)
    for a_return in articles_data:
        print(a_return)
        articles_serializer = ArticlesSerializer(data=a_return)
        if articles_serializer.is_valid():
            try:
                articles_serializer.save()
            except:
                check = False
    if check:
        return HttpResponse('<h1>All success</h1>')
    return HttpResponse('<h1>Failures found</h1>')