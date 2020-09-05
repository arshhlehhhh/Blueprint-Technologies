from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from Glossary.models import Glossary
from Glossary.serializers import GlossarySerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def glossary_list(request):
    # GET list of tutorials, POST a new tutorial, DELETE all tutorials
    if request.method == 'GET':
        glossary = Glossary.objects.all()

        title = request.GET.get('title', None)
        if title is not None:
            glossary = Glossary.filter(title__icontains=title)

        glossary_serializer = GlossarySerializer(glossary, many=True)
        return JsonResponse(glossary_serializer.data, safe=False)
        # 'safe=False' for objects serialization
    elif request.method == 'POST':
        glossary_data = JSONParser().parse(request)
        glossary_serializer = GlossarySerializer(data=glossary_data)
        if glossary_serializer.is_valid():
            glossary_serializer.save()
            return JsonResponse(glossary_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(glossary_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def glossary_detail(request, pk):
    # find glossary by pk (id)
    try:
        glossary = Glossary.objects.get(pk=pk)
        if request.method == 'GET':
            glossary_serializer = GlossarySerializer(glossary)
            return JsonResponse(glossary_serializer.data)
        elif request.method == 'PUT':
            glossary_data = JSONParser().parse(request)
            glossary_serializer = GlossarySerializer(glossary, data=glossary_data)
            if glossary_serializer.is_valid():
                glossary_serializer.save()
                return JsonResponse(glossary_serializer.data)
            return JsonResponse(glossary_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE': 
            glossary.delete() 
            return JsonResponse({'message': 'Glossary was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    except Glossary.DoesNotExist:
        return JsonResponse({'message': 'The glossary does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # GET / PUT / DELETE glossary
