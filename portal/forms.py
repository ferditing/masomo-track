# portal/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Student, Parent, ClassRoom, Subject

class StudentRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    # New field to allow student to enter parent's ID
    parent_identifier = forms.CharField(max_length=20, required=False, label="Parent ID (if available)")

    class Meta:
        model = Student
        fields = ['admission_number', 'bio', 'classroom', 'subjects']
        widgets = {
            'subjects': forms.CheckboxSelectMultiple,
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Passwords do not match.")
        return cleaned_data

    def clean_subjects(self):
        subjects = self.cleaned_data.get('subjects')
        if subjects and len(subjects) < 8:
            raise forms.ValidationError("You must select at least 8 subjects.")
        return subjects

class ParentRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    # Parent must provide their unique identifier during registration
    identifier = forms.CharField(max_length=20, required=True, label="Parent ID")

    class Meta:
        model = Parent
        fields = ['identifier']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Passwords do not match.")
        return cleaned_data