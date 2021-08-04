from django import forms
from core.models import Training
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = "__all__"

    def clean(self):
        cd = super().clean()
        if (
            cd.get("start_time")
            and cd.get("end_time")
            and cd.get("start_time") >= cd.get("end_time")
        ):
            raise ValidationError(
                _("The time the training ends cannot be less than the time it starts.")
            )
        return cd
