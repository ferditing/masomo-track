from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import StudentRegistrationForm


def home(request):
    return HttpResponse("Welcome to Masomo Track")
# Create your views here.
# portal/views.py
def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            # Create a new User
            user = User.objects.create_user(
                username=form.cleaned_data['email'],  # using email as username
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password']
            )
            # Create the associated Student profile
            student = form.save(commit=False)
            student.user = user
            student.save()
            # Save many-to-many fields (e.g., subjects)
            form.save_m2m()
            
            # Optionally, log the user in immediately
            login(request, user)
            return redirect('home')  # Redirect to a homepage or student dashboard
    else:
        form = StudentRegistrationForm()
    return render(request, 'portal/student_register.html', {'form': form})


from django.shortcuts import render
from .decorators import parent_required, teacher_required, headteacher_required, class_teacher_required

# Parent Dashboard
@login_required
@parent_required
def parent_dashboard(request):
    context = {
        'message': "Welcome, Parent! Here you can monitor your child's academic progress and financial status."
    }
    return render(request, 'portal/parent_dashboard.html', context)

# Existing teacher dashboards...
@login_required
@teacher_required
def teacher_dashboard(request):
    context = {
        'message': "Welcome, Subject Teacher! Here you can manage your subjects and assignments."
    }
    return render(request, 'portal/teacher_dashboard.html', context)

@login_required
@headteacher_required
def headteacher_dashboard(request):
    context = {
        'message': "Welcome, Headteacher! You have full access to all school data."
    }
    return render(request, 'portal/headteacher_dashboard.html', context)

@login_required
@class_teacher_required
def class_teacher_dashboard(request):
    context = {
        'message': "Welcome, Class Teacher! Here you can view your class details and assigned subjects."
    }
    return render(request, 'portal/class_teacher_dashboard.html', context)

@login_required
def student_dashboard(request):
    context = {
        'message': "Welcome, Student! Here you can view your assignments, academic progress, and more."
    }
    return render(request, 'portal/student_dashboard.html', context)

@login_required
def dashboard_redirect(request):
    user = request.user
    # Check for a student profile first
    if hasattr(user, 'student_profile'):
        return redirect('student_dashboard')  # Create this dashboard if needed.
    # Then check if the user is a parent
    elif hasattr(user, 'parent_profile'):
        return redirect('parent_dashboard')
    # Then check if the user is a teacher
    elif hasattr(user, 'teacher_profile'):
        teacher = user.teacher_profile
        if teacher.is_headteacher:
            return redirect('headteacher_dashboard')
        elif teacher.is_class_teacher:
            return redirect('class_teacher_dashboard')
        else:
            return redirect('teacher_dashboard')
    # Default to home if no profile is found
    else:
        return redirect('home')