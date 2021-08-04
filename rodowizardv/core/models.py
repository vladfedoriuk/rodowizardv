import uuid
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Training(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name=_("Training title"),
    )
    start_time = models.DateTimeField(
        verbose_name=_("Start time"), help_text=_("The date and time training starts")
    )
    end_time = models.DateTimeField(
        verbose_name=_("End time"), help_text=_("The date and time training ends")
    )
    email = models.EmailField()

    slug = models.SlugField(unique_for_date="start_time")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "core:training",
            kwargs={
                "year": self.start_time.year,
                "month": self.start_time.month,
                "day": self.start_time.day,
                "training": self.slug,
            },
        )

    class Meta:
        ordering = ("-start_time", "end_time")


class PersonalData(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    training = models.ForeignKey(
        Training,
        on_delete=models.CASCADE,
        related_name="consents",
        related_query_name="consent",
    )
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    surname = models.CharField(max_length=255, verbose_name=_("Surname"))
    email = models.EmailField(verbose_name=_("Email address"))
    phone_number = models.CharField(max_length=20, verbose_name=_("Phone Number"))
    street = models.CharField(
        max_length=100, verbose_name=_("Street and number of a building")
    )
    post_code = models.CharField(max_length=10, verbose_name=_("Postal code"))
    city = models.CharField(max_length=100, verbose_name=_("City"))
    consent_1 = models.BooleanField(
        help_text=_(
            """
        Consent to the processing of the personal data 
        in a way that is necessary for training realization."""
        ),
        default=False,
        verbose_name=_("*"),
    )
    consent_2 = models.BooleanField(
        help_text=_(
            """
        Consent to granting the third party access to the personal data 
        in a way that is necessary for training realization."""
        ),
        default=False,
        verbose_name=_("*"),
    )
    consent_3 = models.BooleanField(
        help_text=_(
            """
        Consent to granting the third party access to the personal data 
        in terms of my participation in the exam."""
        ),
        default=False,
        verbose_name=_("*"),
    )
    is_finished = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse(
            "core:data",
            kwargs={
                "data_id": self.pk,
            },
        )

    def to_dict(self):
        return {
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "phone number": self.phone_number,
            "street": self.street,
            "post code": self.post_code,
            "city": self.city,
        }

    class Meta:
        verbose_name = _("Personal Data")
        verbose_name_plural = verbose_name
