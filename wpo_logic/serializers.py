from wpo_logic.models import CodigosPostales
from rest_framework import serializers


class CodigosPostalesSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['codigo_postal_id']
        model = CodigosPostales

