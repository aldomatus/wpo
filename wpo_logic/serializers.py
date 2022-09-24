from wpo_logic.models import CodigosPostales
from wpo_logic.models import SportsLocation
from rest_framework import serializers


class CodigosPostalesSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['codigo_postal_id']
        model = CodigosPostales


class SportsLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportsLocation
        fields = '__all__'

    def create(self, validated_data):
        return SportsLocation.objects.create(**validated_data)
