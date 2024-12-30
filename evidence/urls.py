from django.urls import path
from . import views  # Import views from the evidence app

urlpatterns = [
    path('', views.home, name='home'),
      path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),  # Map the root URL to the home view
]
