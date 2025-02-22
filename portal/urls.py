from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/student/', views.student_register, name='student_register'),
    path('register/parent/', views.parent_register, name='parent_register'),
    path('register/teacher/', views.teacher_register, name='teacher_register'),
    
    # Login and Logout
    path('login/', auth_views.LoginView.as_view(template_name='portal/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # Dashboard Redirect
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    
    # Individual Dashboards
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/headteacher/', views.headteacher_dashboard, name='headteacher_dashboard'),
    path('dashboard/classteacher/', views.class_teacher_dashboard, name='class_teacher_dashboard'),
    path('dashboard/parent/', views.parent_dashboard, name='parent_dashboard'),
    path('dashboard/finance/', views.finance_dashboard, name='finance_dashboard'),  # You'd create this view/template
    
    # Teacher functions
    path('dashboard/teacher/create-assignment/', views.create_assignment, name='create_assignment'),
    
    # Headteacher functions
    path('dashboard/headteacher/create-timetable/', views.create_timetable, name='create_timetable'),
    
    # Finance functions
    path('dashboard/finance/update-record/<int:record_id>/', views.update_financial_record, name='financial_record'),
]
