from django.urls import path, re_path
from . import views
from rest_framework.authtoken import views as auth_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

app_name = "api"

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("person/retrieve/", views.PersonalDataViewGET.as_view(), name="person_get"),
    path("person/confirm/", views.PersonalDataConfirm.as_view(), name="person_confirm"),
    path("person/add/", views.PersonalDataViewPOST.as_view(), name="person_post"),
    path("person/update/", views.PersonalDataViewPUT.as_view(), name="person_put"),
    path("api-token-auth/", auth_views.obtain_auth_token, name="auth"),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
