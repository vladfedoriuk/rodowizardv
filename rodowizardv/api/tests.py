from rest_framework.test import APITestCase
from rest_framework import status
from requests.auth import HTTPBasicAuth
from core.models import Training, PersonalData
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.translation import activate
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
import json

hour = timedelta(hours=1)


class SendConfirmTest(APITestCase):
    def setUp(self):
        training = Training(
            title="Test training",
            slug="test-training",
            start_time=timezone.now(),
            end_time=timezone.now() + hour,
            email=settings.DEFAULT_FROM_EMAIL,
        )
        training.save()
        self.training = training
        self.admin = User.objects.create_superuser(
            username=settings.DEFAULT_ADMIN.get("username"),
            password=settings.DEFAULT_ADMIN.get("password"),
            email=settings.DEFAULT_FROM_EMAIL,
        )
        pd = PersonalData(
            name="test name",
            surname="test surname",
            email="test@gmail.com",
            phone_number="+48577152970",
            street="Test street",
            post_code="12-123",
            city="Test city",
            consent_1=True,
            consent_2=True,
            consent_3=True,
            training=self.training,
        )
        pd.save()
        self.pd = pd

    def test_login_auth(self):
        url = reverse_lazy("api:person_get")
        response = self.client.get(url, data={"id": self.pd.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.login(
            username=settings.DEFAULT_ADMIN.get("username"),
            password=settings.DEFAULT_ADMIN.get("password"),
        )
        response = self.client.get(url, data={"id": self.pd.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_auth(self):
        auth_url = reverse_lazy("api:auth")
        response = self.client.post(
            auth_url,
            {
                "username": settings.DEFAULT_ADMIN.get("username"),
                "password": settings.DEFAULT_ADMIN.get("password"),
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse_lazy("api:person_get")
        token = response.data.get("token")
        self.assertFalse(token is None)
        response = self.client.get(
            url, data={"id": self.pd.id}, HTTP_AUTHORIZATION=f"Token {token}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_put(self):
        data = {
            "name": "test name",
            "surname": "test surname",
            "email": "test@gmail.com",
            "phone_number": "+48577152970",
            "street": "Test street",
            "post_code": "12-123",
            "city": "Test city",
            "consent_1": True,
            "consent_2": True,
            "consent_3": True,
            "training": self.training.pk,
        }
        url_post = reverse_lazy("api:person_post")
        response = self.client.post(url_post, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        res_data = response.data
        pd = PersonalData.objects.get(id=res_data.get("id"))
        self.assertTrue(pd.is_finished)
        self.assertFalse(pd.email_confirmed)
        url_put = reverse_lazy("api:person_put")
        response = self.client.put(
            url_put,
            {"id": pd.id},
            CONTENT_TYPE="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get("email_confirmed"))
