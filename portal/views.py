from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Parent, FinancialRecord, ClassRoom
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import StudentRegistrationForm, ParentRegistrationForm, AssignmentForm, ResultForm


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
    if teacher.is_class_teacher:
        # Retrieve the classroom where this teacher is assigned as the class teacher.
        class_room = ClassRoom.objects.filter(class_teacher=teacher).first()
        assignments = class_room.assignments.all().order_by('-posted_date') if class_room else []
    else:
        assignments = teacher.created_assignments.all().order_by('-posted_date')
    context = {
        'assignments': assignments,
    }
    return render(request, 'portal/teacher_dashboard.html', context)
    
#head teacher dashboard
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

# portal/views.py

@login_required
def student_dashboard(request):
    if not hasattr(request.user, 'student_profile'):
        return redirect('home')
    student = request.user.student_profile
    assignments = []
    for subject in student.subjects.all():
        assignments.extend(subject.assignments.all())
    assignments.sort(key=lambda a: a.due_date)
    
    # Optionally, fetch answers to display submission status
    answers = student.answers.all()
    answers_dict = { ans.assignment.id: ans for ans in answers }
    
    context = {
        'assignments': assignments,
        'answers': answers_dict,  # key: assignment.id, value: Answer instance
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
    
#Create assignment view
@login_required
@teacher_required
def create_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            # Set the teacher creating this assignment
            assignment.created_by = request.user.teacher_profile
            assignment.save()
            form.save_m2m()
            return redirect('teacher_dashboard')
    else:
        form = AssignmentForm()
    return render(request, 'portal/create_assignment.html', {'form': form})

#post result view
@login_required
@teacher_required
def post_result(request):
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = ResultForm()
    return render(request, 'portal/post_result.html', {'form': form})

from .forms import TeacherRegistrationForm

#teacher registration view
def teacher_register(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            # Create a new User for the teacher
            user = User.objects.create_user(
                username=form.cleaned_data['email'],  # using email as username
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password']
            )
            # Create the Teacher profile
            teacher = form.save(commit=False)
            teacher.user = user
            teacher.save()
            form.save_m2m()
            login(request, user)
            return redirect('dashboard_redirect')
    else:
        form = TeacherRegistrationForm()
    return render(request, 'portal/teacher_register.html', {'form': form})

from .forms import TimetableForm

@login_required
@headteacher_required
def create_timetable(request):
    if request.method == 'POST':
        form = TimetableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('headteacher_dashboard')
    else:
        form = TimetableForm()
    return render(request, 'portal/create_timetable.html', {'form': form})

from .forms import FinancialRecordUpdateForm


@login_required
def update_financial_record(request, record_id):
    try:
        record = FinancialRecord.objects.get(id=record_id)
    except FinancialRecord.DoesNotExist:
        return redirect('finance_dashboard')  # or some error page

    if request.method == 'POST':
        form = FinancialRecordUpdateForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('finance_dashboard')
    else:
        form = FinancialRecordUpdateForm(instance=record)
    return render(request, 'portal/financial_record.html', {'form': form, 'record': record})

from .models import FinancialRecord

@login_required
def finance_dashboard(request):
    # Retrieve all financial records, ordered by the latest payment date
    records = FinancialRecord.objects.all().order_by('-payment_date')
    context = {
        'records': records,
    }
    return render(request, 'portal/finance_dashboard.html', context)


from .models import Assignment, Answer
from .forms import AnswerForm

@login_required
def submit_answer(request, assignment_id):
    # Ensure the user is a student
    if not hasattr(request.user, 'student_profile'):
        return redirect('home')
    
    assignment = get_object_or_404(Assignment, id=assignment_id)
    student = request.user.student_profile

    # Check if an answer already exists for this assignment by the student
    existing_answer = Answer.objects.filter(assignment=assignment, student=student).first()

    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES, instance=existing_answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.assignment = assignment
            answer.student = student
            answer.save()
            return redirect('student_dashboard')
    else:
        form = AnswerForm(instance=existing_answer)
    
    context = {
        'form': form,
        'assignment': assignment,
    }
    return render(request, 'portal/submit_answer.html', context)

#view submition made ny students
@login_required
@teacher_required
def view_submissions(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, created_by=request.user.teacher_profile)
    # Get all answer submissions for this assignment
    submissions = assignment.answers.all()  # assuming the Answer model's related_name is 'answers'
    context = {
        'assignment': assignment,
        'submissions': submissions,
    }
    return render(request, 'portal/view_submissions.html', context)
