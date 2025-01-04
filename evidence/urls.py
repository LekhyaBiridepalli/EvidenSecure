from django.urls import path
from . import views  # Import views from the evidence app

urlpatterns = [
    path('', views.home, name='home'),
      path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
      path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('cases/', views.cases, name='cases'),  # Cases Management route
    path('evidence/', views.evidence, name='evidence'),  # Evidence Management route
    path('uploadcase/', views.upload_case, name='upload_case'),
    path('uploadevidence/', views.upload_evidence, name='upload_evidence'),
    #  path('upload-case/', views.upload_case, name='upload_case'),
    # path('upload-evidence/', views.upload_evidence, name='upload_evidence'),
]
