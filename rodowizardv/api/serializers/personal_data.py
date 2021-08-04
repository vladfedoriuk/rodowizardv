from core.models import PersonalData
from rest_framework import serializers
from .training import TrainingSerializer
from core.models import Training
from django.utils.translation import gettext_lazy as _


class PersonalDataSerializer(serializers.ModelSerializer):
    training = TrainingSerializer()

    class Meta:
        model = PersonalData
        fields = "__all__"


class PersonalDataSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = PersonalData
        exclude = ["is_finished", "email_confirmed"]


class PersonalDataIdSerializer(serializers.Serializer):
    id = serializers.UUIDField()
