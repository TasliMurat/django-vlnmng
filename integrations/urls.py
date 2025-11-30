from django.urls import path
from . import views

urlpatterns = [
    path("<int:pk>/", views.integration_detail, name="integration_detail"),
    path("tenable/run/", views.run_tenable, name="run_tenable"),
    path("tenable/create_config/", views.CreateUpdateConfigView, name="tenablecreateupdateconfigview"),
    path("invicti/run/", views.run_invicti, name="run_invicti"),
]
