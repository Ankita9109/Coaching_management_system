"""
URL configuration for coaching_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='home'),
    path('dashboard/', views.dashboard,name="dashboard"),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('otp-reset/', views.otp_reset, name='otp_reset'),


    path('edit-student/<int:id>/', views.edit_student, name='edit_student'),
    path('delete-student/<int:id>/', views.delete_student, name='delete_student'),
    path('fees/<int:student_id>/', views.fee_history, name='fee_history'),
    path('attendance/<int:student_id>/', views.mark_attendance, name='mark_attendance'),
    path('attendance-history/<int:student_id>/', views.attendance_history, name='attendance_history'),

    path('add-student/', views.add_student, name="add_student"),
    path('students/', views.student_list, name="student_list"),
    path('add-fee/<int:student_id>/', views.add_fee, name="add_fee"),
    path("profile/<int:student_id>/", views.student_profile, name="student_profile"),
    path('daily-attendance/', views.daily_attendance, name='daily_attendance'),
    path("receipt/<int:fee_id>/", views.fee_receipt, name="fee_receipt"),

    # course all urls
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/edit/<int:id>/', views.edit_course, name='edit_course'),
    path('courses/delete/<int:id>/', views.delete_course, name='delete_course'),
    


    # Forgot password flow
path('password-reset/',
     auth_views.PasswordResetView.as_view(
         template_name='password_reset.html'
     ),
     name='password_reset'),

path('password-reset/done/',
     auth_views.PasswordResetDoneView.as_view(
         template_name='password_reset_done.html'
     ),
     name='password_reset_done'),

path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(
         template_name='password_reset_confirm.html'
     ),
     name='password_reset_confirm'),

path('reset/done/',
     auth_views.PasswordResetCompleteView.as_view(
         template_name='password_reset_complete.html'
     ),
     name='password_reset_complete'),

path('create-admin/', views.create_admin),

]
