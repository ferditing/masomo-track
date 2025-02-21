from django.shortcuts import render
from .models import Student, Parent
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import StudentRegistrationForm, ParentRegistrationForm


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
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password']
            )
            # Create the associated Student profile
            student = form.save(commit=False)
            student.user = user
            student.save()
            form.save_m2m()
            
            # Link the student to a parent if a Parent ID was provided
            parent_id = form.cleaned_data.get('parent_identifier')
            if parent_id:
                try:
                    parent = Parent.objects.get(identifier=parent_id)
                    student.parents.add(parent)
                except Parent.DoesNotExist:
                    # Optionally, you can add an error or log a message here
                    pass

            # Optionally, log in the new user immediately
            login(request, user)
            return redirect('dashboard_redirect')
    else:
        form = StudentRegistrationForm()
    return render(request, 'portal/student_register.html', {'form': form})

from django.shortcuts import render
from .decorators import parent_required, teacher_required, headteacher_required, class_teacher_required


def parent_register(request):
    if request.method == 'POST':
        form = ParentRegistrationForm(request.POST)
        if form.is_valid():
            # Create a new User for the parent
            user = User.objects.create_user(
                username=form.cleaned_data['email'] if form.cleaned_data.get('email') else form.cleaned_data['identifier'],
                email=form.cleaned_data.get('email', ''),
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password']
            )
            # Create the Parent profile with the provided identifier
            parent = form.save(commit=False)
            parent.user = user
            parent.save()
            
            # Log the user in and redirect (or show the linked children if any)
            login(request, user)
            return redirect('dashboard_redirect')
    else:
        form = ParentRegistrationForm()
    return render(request, 'portal/parent_register.html', {'form': form})
# Parent Dashboard
@login_required
@parent_required
def parent_dashboard(request):
    parent = request.user.parent_profile
    children = parent.children.all()  # Using the ManyToMany relation from Student
    context = {
        'children': children,
    }
    return render(request, 'portal/parent_dashboard.html', context)
    

# Existing teacher dashboards...
@login_required
@teacher_required
def teacher_dashboard(request):
    teacher = request.user.teacher_profile
    # Gather assignments for subjects this teacher is responsible for.
    assignments = []
    for subject in teacher.subjects.all():
        assignments.extend(subject.assignments.all())
    # Optionally, sort assignments by due date
    assignments.sort(key=lambda a: a.due_date)
    
    context = {
        'assignments': assignments,
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
    if not hasattr(request.user, 'student_profile'):
        return redirect('home')
    student = request.user.student_profile
    # Get assignments from the subjects the student is enrolled in
    assignments = []
    for subject in student.subjects.all():
        assignments.extend(subject.assignments.all())
    assignments.sort(key=lambda a: a.due_date)
    
    results = student.results.all()
    
    context = {
        'assignments': assignments,
        'results': results,
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