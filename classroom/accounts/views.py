from django.shortcuts import render , redirect, get_object_or_404
from .form import StudentForm, TeacherForm, SignupUserForm, TeacherAssignmentForm
from django import views
from .models import ClassAssignment, Teacher, Student, User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(views.View):
    def get(self, request):
        return render(request, 'index.html')


class SignUpView(views.View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('class:Home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'accounts/signup.html')


class TeacherSignUpView(views.View):
    view_form = SignupUserForm
    add_view_form = TeacherForm
    template_class = 'accounts/signup_teacher.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('class:Home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, requset):
        return render(requset, self.template_class, {'userform': self.view_form, 'teacherform': self.add_view_form})

    def post(self, request):
        userform = self.view_form(request.POST)
        teacherform = self.add_view_form(request.POST)

        if userform.is_valid() and teacherform.is_valid():
            user = userform.save()
            user.is_teacher = True
            user.save()

            teacher = teacherform.save(commit=False)
            teacher.user = user
            teacher.save()
            return redirect('class:Home')
        return render(request, self.template_class, {'userform': userform, 'teacherform': teacherform})


class StudentSignUpView(views.View):
    view_form = SignupUserForm
    add_view_form = StudentForm
    template_class = 'accounts/signup_student.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('class:Home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, requset):
        return render(requset, self.template_class, {'userform': self.view_form, 'studentform': self.add_view_form})

    def post(self, request):
        userform = self.view_form(request.POST)
        studentform = self.add_view_form(request.POST)

        if userform.is_valid() and studentform.is_valid():
            user = userform.save()
            user.is_teacher = True
            user.save()

            student = studentform.save(commit=False)
            student.user = user
            student.save()
            return redirect('class:Home')
        return render(request, self.template_class, {'userform': userform, 'studentform': studentform})


class LoginView(views.View):
    template_class = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('class:Home')
        return super().dispatch(request, *args, **kwargs)

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_class)

    def post(self, request):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            messages.success(request, 'wellcome')
            if self.next:
                return redirect(self.next)
            return redirect('class:Home')
        else:
            messages.error(request, 'user not found')
        return render(request, self.template_class)


class LogoutView(LoginRequiredMixin, views.View):

    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out')
        return redirect('class:Home')


class AssignmentView(LoginRequiredMixin, views.View):
    template_class = 'accounts/assignment_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_teacher:
            messages.error(request, 'access denied')
            return redirect('class:Home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        assignments = ClassAssignment.objects.filter(teacher=request.user.Teacher)
        return render(request, self.template_class, {'assignments': assignments})


class UploadAssignmentView(LoginRequiredMixin, views.View):
    form_class = TeacherAssignmentForm
    template_class = 'accounts/upload_assignment.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_teacher:
            messages.error(request, 'access denied')
            return redirect('class:Home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_class, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        teacher = request.user.Teacher
        students = teacher.class_students.all()
        if form.is_valid():
            upload = form.save(commit=False)
            upload.teacher = teacher
            upload.save()
            upload.student.add(*students)
            return redirect('class:assignment_list')
        messages.error(request, 'didnt upload')
        return render(request, self.template_class, {'form': form})


class UpdateAssignmentView(LoginRequiredMixin, views.View):
    template_name = 'accounts/update_assignment.html'
    form_class = TeacherAssignmentForm

    def get(self, request, pk):
        assignment = get_object_or_404(ClassAssignment, id=pk)
        form = self.form_class(instance=assignment)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        assignment = get_object_or_404(ClassAssignment, id=pk)
        form = self.form_class(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, 'assignment updated')
            return redirect('class:assignment_list')
        return render(request, self.template_name, {'form': form})


class DeleteAssignmentView(LoginRequiredMixin, views.View):
    template_name = 'accounts/delete_assignment.html'

    def get(self, request, pk):
        obj = get_object_or_404(ClassAssignment, id=pk)
        return render(request, self.template_name, {'object': obj})

    def post(self, request, pk):
        obj = ClassAssignment.objects.filter(id=pk)
        obj.delete()
        messages.success(request, 'deleted')
        return redirect('class:assignment_list')


class TeacherDetailView(LoginRequiredMixin,views.View):
    def dispatch(self, request, *args, **kwargs):
        self.teacher = get_object_or_404(User, id=kwargs['pk']).Teacher
        if request.user.Teacher != self.teacher:
            return redirect('class:Home')
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, pk):
        return render(request, 'accounts/detail_teacher.html', {'teacher': self.teacher})


class StudentDetailView(LoginRequiredMixin,views.View):
    def dispatch(self, request, *args, **kwargs):
        self.student = get_object_or_404(User, id=kwargs['pk']).Student
        if request.user.Student != self.student:
            return redirect('class:Home')
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, pk):
        return render(request, 'accounts/detail_student.html', {'student': self.student})


class TeacherUpdateProfile(LoginRequiredMixin, views.View):
    form_class = TeacherForm
    template_name = 'accounts/update_teacher.html'

    def dispatch(self, request, *args, **kwargs):
        self.teacher = get_object_or_404(User, id=kwargs['pk']).Teacher
        if request.user.Teacher != self.teacher:
            messages.error(request, 'access denied')
            return redirect('class:Home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        form = self.form_class(instance=self.teacher)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        form = self.form_class(request.POST, request.FILES, instance=self.teacher)
        if form.is_valid():
            form.save()
            return redirect('class:detail_teacher', request.user.id)
        return render(request, self.template_name, {'form': form})


class StudentUpdateProfile(LoginRequiredMixin, views.View):
    form_class = StudentForm
    template_name = 'accounts/update_student.html'

    def dispatch(self, request, *args, **kwargs):
        self.student = get_object_or_404(User, id=kwargs['pk']).Student
        if request.user.Student != self.student:
            messages.error(request, 'access denied')
            return redirect('class:Home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        form = self.form_class(instance=self.student)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        form = self.form_class(request.POST, request.FILES, instance=self.student)
        if form.is_valid():
            form.save()
            return redirect('class:detail_student', request.user.id)
        return render(request, self.template_name, {'form': form})

