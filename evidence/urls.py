from django.urls import path
from . import views  # Import views from the evidence app

urlpatterns = [
    path('', views.landing_page, name='landing_page'),  # Map the root URL to the home view
]
