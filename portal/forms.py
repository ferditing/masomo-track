# portal/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Student, ClassRoom, Subject

class StudentRegistrationForm(forms.ModelForm):
    # User-related fields
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta:
        model = Student
        fields = ['admission_number', 'bio', 'classroom', 'subjects']
        widgets = {
            'subjects': forms.CheckboxSelectMultiple,  # Allow multiple selections
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
