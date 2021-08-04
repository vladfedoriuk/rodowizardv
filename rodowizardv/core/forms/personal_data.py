from django import forms
from core.models import PersonalData
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _


class PersonalDataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonalDataForm, self).__init__(*args, **kwargs)
        self.fields["consent_1"].required = True
        self.fields["consent_2"].required = True
        self.fields["consent_3"].required = True

    phone_number = forms.CharField(
        validators=[
            RegexValidator(
                regex=r"^\+?[\d\-\s]{9,20}$",
                message=_(
                    """
                    A phone number should match the pattern: 
                    +xxxxxxxxx or xxxxxxxxx, where 'x' denotes a digit,
                    and it must consist of up to 20 digits."""
                ),
            ),
            MaxLengthValidator(20),
        ],
        widget=forms.widgets.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "aria-describedby": "phone-number-help",
            }
        ),
    )

    post_code = forms.CharField(
        validators=[
            RegexValidator(
                regex=r"^\d{2}\-\d{3}$",
                message=_(
                    """
                A postal code should match the pattern: 
                xx-xxx, where 'x' denotes a digit,
                and it must consist of 5 digits."""
                ),
            ),
            MaxLengthValidator(10),
        ],
        widget=forms.widgets.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "aria-describedby": "post-code-help",
            }
        ),
    )

    class Meta:
        model = PersonalData
        exclude = ["training", "is_finished", "email_confirmed"]
        widgets = {
            "name": forms.widgets.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "aria-describedby": "name-help",
                }
            ),
            "surname": forms.widgets.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "aria-describedby": "surname-help",
                }
            ),
            "email": forms.widgets.EmailInput(
                attrs={
                    "type": "email",
                    "class": "form-control",
                    "aria-describedby": "email-help",
                }
            ),
            "street": forms.widgets.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "aria-describedby": "street-help",
                }
            ),
            "city": forms.widgets.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "aria-describedby": "city-help",
                }
            ),
            "consent_1": forms.widgets.CheckboxInput(
                attrs={
                    "type": "checkbox",
                    "class": "form-check form-check-inline",
                    "aria-describedby": "consent-1-help",
                }
            ),
            "consent_2": forms.widgets.CheckboxInput(
                attrs={
                    "type": "checkbox",
                    "class": "form-check form-check-inline",
                    "aria-describedby": "consent-2-help",
                }
            ),
            "consent_3": forms.widgets.CheckboxInput(
                attrs={
                    "type": "checkbox",
                    "class": "form-check form-check-inline",
                    "aria-describedby": "consent-3-help",
                }
            ),
        }
