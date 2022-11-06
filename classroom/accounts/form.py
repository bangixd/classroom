from django import forms
from .models import Teacher, Student, User, ClassAssignment, SubmitAssignment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.validators import validators


class SignupUserForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        exclude = ['class_students', 'user']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'phone', 'roll_no', 'email', 'profile_pic']


class TeacherAssignmentForm(forms.ModelForm):
    class Meta:
        model = ClassAssignment
        fields = ['assignment_name', 'assignment']
