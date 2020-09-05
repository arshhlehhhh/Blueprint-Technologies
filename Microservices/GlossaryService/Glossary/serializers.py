from rest_framework import serializers 
from Glossary.models import Glossary
 
 
class GlossarySerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Glossary
        fields = ('id',
                  'term',
                  'description',
                  'actionable')
