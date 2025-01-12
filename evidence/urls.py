from django.urls import path
from . import views  # Import views from the evidence app

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('cases/', views.cases, name='cases'),  # Cases Management route
    path('evidence/', views.evidence_view, name='evidence'),  # Evidence Management route
    path('add_case/', views.add_case, name='add_case'),
    path('cases/<str:case_id>/', views.case_detail, name='case_detail'),  # Case details view
    path('add_evidence/', views.add_evidence, name='add_evidence'),  # Accept case_number in URL
    path('view_file/<str:file_id>/', views.view_file, name='view_file'),


        

]
