from rest_framework.views import APIView
from rest_framework.generics import (
    RetrieveAPIView,
    CreateAPIView,
    GenericAPIView
)
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from core.models import PersonalData
from .utils.codes import ResponseData

from .serializers import (
    PersonalDataSerializer,
    PersonalDataSerializerPOST,
    PersonalDataIdSerializer,
)

from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAdminUser
from django.utils.translation import gettext_lazy as _
from . import utils

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from django.core import mail
from django.template.loader import render_to_string
import json


def send_mails(data_obj: PersonalData, confirmation_url: str):
    with mail.get_connection() as connection:
        # send  an email to a user
        subject = _("Email Confirmation")
        confirmation_email = mail.EmailMessage(
            subject=str(subject),
            body=render_to_string(
                "core/emails/email_confirmation.html",
                {"confirmation_link": confirmation_url},
            ),
            to=[data_obj.email],
            connection=connection,
        )
        confirmation_email.content_subtype = "html"
        confirmation_email.send()
        data_obj.is_finished = True
        data_obj.save()

        # send an email to a training owner
        subject = _("New RODO data.")
        data_json = json.dumps(data_obj.to_dict(), indent=4)
        info_email = mail.EmailMessage(
            subject=str(subject),
            body=render_to_string(
                "core/emails/email_training_owner.html",
                {"data_json": data_json},
            ),
            to=[data_obj.training.email],
            connection=connection,
        )
        info_email.content_subtype = "html"
        info_email.send()


authorization = openapi.Parameter(
    name="Authorization",
    in_=openapi.IN_HEADER,
    description="Token <token>",
    type=openapi.TYPE_STRING,
)
pd_id = openapi.Parameter(
    name="id",
    in_=openapi.IN_QUERY,
    description="The uuid of the personal data",
    type=openapi.TYPE_STRING,
)

class PersonalDataMixIn:
    serializer_class = PersonalDataSerializer

    def get_object(self):
        id_serializer = PersonalDataIdSerializer(data=self.request.query_params)
        if id_serializer.is_valid():
            cd = id_serializer.data
            pd_id = cd.get("id")
            return get_object_or_404(self.get_queryset(), id=pd_id)
        else:
            raise utils.codes.WrongPersonalDataUUID

    def get_queryset(self):
        return PersonalData.objects.all()
    
class PersonalDataViewGET(PersonalDataMixIn, RetrieveAPIView):

    permission_classes = [IsAdminUser]
    authentication_classes = [
        BasicAuthentication,
        SessionAuthentication,
        TokenAuthentication,
    ]

    @swagger_auto_schema(
        manual_parameters=[authorization, pd_id],
        responses={200: PersonalDataSerializer},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PersonalDataViewPOST(CreateAPIView):
    serializer_class = PersonalDataSerializerPOST

    def perform_create(self, serializer):
        data_obj = serializer.save()
        confirmation_url = self.request.build_absolute_uri(data_obj.get_absolute_url())
        send_mails(data_obj, confirmation_url)

    @swagger_auto_schema(
        request_body=PersonalDataSerializerPOST,
        responses={200: PersonalDataSerializerPOST},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PersonalDataConfirm(APIView):
    @swagger_auto_schema(
        request_body=PersonalDataIdSerializer,
        responses={200: PersonalDataSerializer},
    )
    def put(self, request, *args, **kwargs):
        serializer = PersonalDataIdSerializer(data=request.data)
        if not serializer.is_valid():
            raise utils.codes.WrongPersonalDataUUID
        data_id = serializer.data.get("id")
        data_obj = get_object_or_404(PersonalData, id=data_id)
        data_obj.email_confirmed = True
        data_obj.save()
        data = PersonalDataSerializer(data_obj).data
        return Response(data=data, status=status.HTTP_200_OK)


class PersonalDataViewPUT(PersonalDataMixIn, UpdateModelMixin, GenericAPIView):
    
    @swagger_auto_schema(
        manual_parameters=[authorization, pd_id],
        responses={200: PersonalDataSerializer},
    )
    def put(self, request, *args, **kwargs):
        return super(PersonalDataViewPUT, self).partial_update(request, *args, **kwargs)
    