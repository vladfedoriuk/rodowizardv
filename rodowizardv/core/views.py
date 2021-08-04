from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Training, PersonalData
from .forms.personal_data import PersonalDataForm
from django.views.decorators.http import require_http_methods
from django.core import mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
import json


class TrainingView(View):

    template_name = "core/wizard.html"
    success_template_name = "core/success.html"
    personal_data_form_class = PersonalDataForm

    def get(self, request, year, month, day, training):
        training = get_object_or_404(
            Training,
            start_time__year=year,
            start_time__month=month,
            start_time__day=day,
            slug=training,
        )
        personal_data_form = self.personal_data_form_class()
        return render(
            request,
            self.template_name,
            {"training": training, "personal_data_form": personal_data_form},
        )

    def post(self, request, year, month, day, training):
        training = get_object_or_404(
            Training,
            start_time__year=year,
            start_time__month=month,
            start_time__day=day,
            slug=training,
        )
        data_obj = PersonalData(training=training)
        personal_data_form = self.personal_data_form_class(
            request.POST, instance=data_obj
        )
        if personal_data_form.is_valid():
            cd = personal_data_form.cleaned_data
            data_obj = personal_data_form.save()
            confirmation_url = request.build_absolute_uri(data_obj.get_absolute_url())

            with mail.get_connection() as connection:
                # send  an email to a user
                subject = _("Email Confirmation")
                confirmation_email = mail.EmailMessage(
                    subject=str(subject),
                    body=render_to_string(
                        "core/emails/email_confirmation.html",
                        {"confirmation_link": confirmation_url},
                    ),
                    to=[cd["email"]],
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
                    to=[training.email],
                    connection=connection,
                )
                info_email.content_subtype = "html"
                info_email.send()

            return render(request, self.success_template_name, {"training": training})

        else:
            return render(
                request,
                self.template_name,
                {"training": training, "personal_data_form": personal_data_form},
            )


@require_http_methods(["GET"])
def confirm(request, data_id):
    data_obj = get_object_or_404(PersonalData, pk=data_id)
    data_obj.email_confirmed = True
    data_obj.save()
    return render(request, "core/confirmed.html", {"email": data_obj.email})
