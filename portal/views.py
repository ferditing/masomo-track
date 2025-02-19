from django.shortcuts import render
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
