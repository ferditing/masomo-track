# portal/decorators.py

from functools import wraps
from django.http import HttpResponseForbidden

def student_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'student_profile'):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You must be a student to access this page.")
    return _wrapped_view

def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'teacher_profile'):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You must be a teacher to access this page.")
    return _wrapped_view

def parent_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'parent_profile'):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You must be a parent to access this page.")
    return _wrapped_view

def headteacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        teacher_profile = getattr(request.user, 'teacher_profile', None)
        if teacher_profile and teacher_profile.is_headteacher:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You must be a headteacher to access this page.")
    return _wrapped_view

def class_teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        teacher_profile = getattr(request.user, 'teacher_profile', None)
        if teacher_profile and teacher_profile.is_class_teacher:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You must be a class teacher to access this page.")
    return _wrapped_view
