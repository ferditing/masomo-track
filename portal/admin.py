from django.contrib import admin
from .models import ClassRoom, Subject, Student, Teacher, Parent, Assignment, Result, FinancialRecord

# Register your models here.
admin.site.register(ClassRoom)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Parent)
admin.site.register(Assignment)
admin.site.register(Result)
admin.site.register(FinancialRecord)
