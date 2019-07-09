from django.conf.urls import url
from .views import RegistrationAPI, LoginAPI, UserAPI

urlpatterns = [
    url("register/$", RegistrationAPI.as_view()),
    url("^login/$", LoginAPI.as_view()),
    url("^user/$", UserAPI.as_view()),
]
