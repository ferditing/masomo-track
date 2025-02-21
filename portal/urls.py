# portal/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
     path('register/parent/', views.parent_register, name='parent_register'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='portal/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.student_register, name='student_register'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
     path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/headteacher/', views.headteacher_dashboard, name='headteacher_dashboard'),
    path('dashboard/classteacher/', views.class_teacher_dashboard, name='class_teacher_dashboard'),
    # Parent dashboard:
    path('dashboard/parent/', views.parent_dashboard, name='parent_dashboard'),
]
