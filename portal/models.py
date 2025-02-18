from django.db import models
from django.contrib.auth.models import User

# Model for subjects
class Subject(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        'Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subjects_taught'
    )

    def __str__(self):
        return self.name

# Model for classes (using ClassRoom to avoid reserved word conflicts)
class ClassRoom(models.Model):
    name = models.CharField(max_length=50)
    # Each class can have a designated class teacher
    class_teacher = models.ForeignKey(
        'Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='classes'
    )
    # Subjects assigned to this class (this lets the class teacher access them)
    subjects = models.ManyToManyField(Subject, related_name='classrooms', blank=True)

    def __str__(self):
        return self.name

# Profile for students
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    admission_number = models.CharField(max_length=20, unique=True)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    subjects = models.ManyToManyField(Subject, related_name='students', blank=True)
    bio = models.TextField(blank=True, null=True)
    parents = models.ManyToManyField('Parent', related_name='children', blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.admission_number})"

# Profile for teachers
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    # Subjects that the teacher is responsible for as a subject teacher.
    subjects = models.ManyToManyField(Subject, related_name='teacher_subjects', blank=True)
    is_headteacher = models.BooleanField(default=False)    # True if the teacher is the headteacher
    is_class_teacher = models.BooleanField(default=False)    # True if the teacher is a class teacher

    def __str__(self):
        if self.is_headteacher:
            role = "Headteacher"
        elif self.is_class_teacher:
            role = "Class Teacher"
        else:
            role = "Subject Teacher"
        return f"{self.user.get_full_name()} ({role})"

# Profile for parents
class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')

    def __str__(self):
        return self.user.get_full_name()

# Model for assignments posted by subject teachers
class Assignment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    posted_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.subject.name}"

# Model for recording results (marks/scores)
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='results')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='results', null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    date_recorded = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Result: {self.student.user.get_full_name()} - {self.subject.name}"

# Model for tracking financial payments
class FinancialRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='financial_records')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"FinancialRecord: {self.student.user.get_full_name()} - {self.amount_paid}"
