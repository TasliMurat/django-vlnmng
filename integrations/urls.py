from django.urls import path
from . import views

urlpatterns = [
    path("<int:pk>/", views.integration_detail, name="integration_detail"),
    path("setup/<str:provider>/", views.IntegrationConfigView, name="createupdateconfig"),
    path("setup/<str:provider>/<int:pk>/", views.IntegrationConfigView, name="createupdateconfig"),
]
