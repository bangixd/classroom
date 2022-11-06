from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_delete
import os

class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)


class Student(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name='Student')
    name = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    roll_no = models.PositiveIntegerField()
    profile_pic = models.ImageField(upload_to='students_pics', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['roll_no', ]


class Teacher(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name='Teacher')
    name = models.CharField(max_length=250)
    email = models.EmailField()
    subject_name = models.CharField(max_length=250)
    phone = models.CharField(max_length=11)
    profile_pic = models.ImageField(upload_to='teachers_pics', blank=True, null=True)
    class_students = models.ManyToManyField(Student, through='StudentInClass')

    def __str__(self):
        return self.name


class StudentMark(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='given_marks')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject_name = models.CharField(max_length=250)
    marks_obtained = models.IntegerField()
    mark_max = models.IntegerField()

    def __str__(self):
        return self.subject_name


class StudentInClass(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='class_teacher')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='class_student_name')

    def __str__(self):
        return self.student.name

    class Meta:
        unique_together = ['student', 'teacher']
        verbose_name_plural = 'StudentInClasses'


class ClassAssignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_assignment')
    student = models.ManyToManyField(Student, related_name='student_assignment')
    created_at = models.DateTimeField(auto_now=True)
    assignment_name = models.CharField(max_length=250)
    assignment = models.FileField(upload_to='assignments')

    def __str__(self):
        return self.assignment_name

    class Meta:
        ordering = ['created_at']


def delete_assignment_file(sender, **kwargs):
    obj = kwargs['instance']
    file_path = ClassAssignment.objects.get(id=obj.id).assignment.path
    if os.path.exists(file_path):
        os.remove(file_path)


pre_delete.connect(receiver=delete_assignment_file, sender=ClassAssignment)


class SubmitAssignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_submit')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_submit')
    created_at = models.DateTimeField(auto_now=True)
    submitted_assignment = models.ForeignKey(ClassAssignment, on_delete=models.CASCADE,
                                             related_name='submission_for_assignment')
    submit = models.FileField(upload_to='submission')

    def __str__(self):
        return 'submitted'+str(self.submitted_assignment.assignment_name)

    class Meta:
        ordering = ['created_at']















