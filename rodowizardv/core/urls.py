from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path(
        "<int:year>/<int:month>/<int:day>/<slug:training>/",
        views.TrainingView.as_view(),
        name="training",
    ),
    path("confirm/<uuid:data_id>/", views.confirm, name="data"),
]
