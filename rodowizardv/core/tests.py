from django.test import TestCase
from django.test import Client
from .models import Training, PersonalData
from django.utils import timezone
from datetime import timedelta
from http import HTTPStatus
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.translation import activate

hour = timedelta(hours=1)


class SendConfirmTest(TestCase):
    def setUp(self):
        self.client = Client()
        training = Training(
            title="Test training",
            slug="test-training",
            start_time=timezone.now(),
            end_time=timezone.now() + hour,
            email="admin@gmail.com",
        )
        training.save()
        self.training = training

    def test_send_confirm(self):
        form_url = self.training.get_absolute_url()
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
        }
        response = self.client.post(path=form_url, data=data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        pd = PersonalData.objects.filter(**data).first()
        self.assertTrue(pd.is_finished)
        self.assertFalse(pd.email_confirmed)
        self.assertEqual(pd.training, self.training)

        confirm_url = pd.get_absolute_url()
        response = self.client.get(
            path=confirm_url,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        pd = PersonalData.objects.get(pk=pd.pk)
        self.assertTrue(pd.email_confirmed)

    def test_phone_number_validation(self):
        form_url = self.training.get_absolute_url()
        data = {
            "name": "test name",
            "surname": "test surname",
            "email": "test@gmail.com",
            "phone_number": "+48 some strange 123 phone",
            "street": "Test street",
            "post_code": "12-123",
            "city": "Test city",
            "consent_1": True,
            "consent_2": True,
            "consent_3": True,
        }
        response = self.client.post(path=form_url, data=data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response,
            """
            A phone number should match the pattern: 
            +xxxxxxxxx or xxxxxxxxx, where 'x' denotes a digit,
            and it must consist of up to 20 digits.
            """,
            html=True,
        )

    def test_post_code(self):
        form_url = self.training.get_absolute_url()
        data = {
            "name": "test name",
            "surname": "test surname",
            "email": "test@gmail.com",
            "phone_number": "+48 123 456 970",
            "street": "Test street",
            "post_code": "12x123",
            "city": "Test city",
            "consent_1": True,
            "consent_2": True,
            "consent_3": True,
        }
        response = self.client.post(path=form_url, data=data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response,
            """
            A postal code should match the pattern: 
            xx-xxx, where 'x' denotes a digit,
            and it must consist of 5 digits.
            """,
            html=True,
        )


class InternationalizationTest(TestCase):
    def setUp(self):
        self.client = Client()
        training = Training(
            title="Test training",
            slug="test-training",
            start_time=timezone.now(),
            end_time=timezone.now() + hour,
            email="admin@gmail.com",
        )
        training.save()
        self.training = training
        self.texts = [
            "A form of giving an individual consent to processing of the personal data",
            "Forma wyrażenia indywidualnej zgody na przetwarzanie danych osobowych",
        ]

    def test_internationalization(self):

        for (lang, _), text in zip(settings.LANGUAGES, self.texts):
            activate(lang)
            response = self.client.get(self.training.get_absolute_url())
            self.assertContains(response, text, html=True)
