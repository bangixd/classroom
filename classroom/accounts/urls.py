from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'class'
urlpatterns = [
    path('', views.HomeView.as_view(), name='Home'),
    path('signup/', views.SignUpView.as_view(), name='SignUp'),
    path('signup/teacher/', views.TeacherSignUpView.as_view(), name='TeacherSignUp'),
    path('detail/teacher/<int:pk>', views.TeacherDetailView.as_view(), name='detail_teacher'),
    path('update/teacher/<int:pk>', views.TeacherUpdateProfile.as_view(), name='update_teacher'),
    path('signup/student/', views.StudentSignUpView.as_view(), name='StudentSignUp'),
    path('detail/student/<int:pk>', views.StudentDetailView.as_view(), name='detail_student'),
    path('update/student/<int:pk>', views.StudentUpdateProfile.as_view(), name='update_student'),
    path('login/', views.LoginView.as_view(), name='Login'),
    path('logout/', views.LogoutView.as_view(), name='Logout'),
    path('assignment/', views.AssignmentView.as_view(), name='assignment_list'),
    path('assignment/upload/', views.UploadAssignmentView.as_view(), name='upload_assignment'),
    path('assignment/update/<int:pk>', views.UpdateAssignmentView.as_view(), name='update_assignment'),
    path('assignment/delete/<int:pk>', views.DeleteAssignmentView.as_view(), name='delete_assignment'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




