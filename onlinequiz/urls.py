from django.urls import path, include
from django.contrib import admin
from quiz import views
from django.contrib.auth.views import LogoutView, LoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # Teacher and Student modules
    path('teacher/', include('teacher.urls')),
    path('student/', include('student.urls')),

    # Home and authentication
    path('', views.home_view, name='home'),
    path('logout/', views.custom_logout_view, name='custom_logout'),
    path('adminlogin', LoginView.as_view(template_name='quiz/adminlogin.html'), name='adminlogin'),

    # Static pages
    path('aboutus', views.aboutus_view, name='aboutus'),
    path('contactus', views.contactus_view, name='contactus'),
    path('afterlogin', views.afterlogin_view, name='afterlogin'),

    # Admin dashboard
    path('admin-dashboard', views.admin_dashboard_view, name='admin-dashboard'),
    path('adminclick', views.adminclick_view, name='adminclick'),

    # Admin - Teacher management
    path('admin-teacher', views.admin_teacher_view, name='admin-teacher'),
    path('admin-view-teacher', views.admin_view_teacher_view, name='admin-view-teacher'),
    path('admin_teachernew_view',views.admin_teachernew_view,name="admin_teachernew_view"),
    path('admin_view_teacher_view',views. admin_view_teacher_view,name=" admin_view_teacher_view"),
    path('admin_view_teachernew_view',views.admin_view_teachernew_view,name="admin_view_teachernew_view"),
    path('update-teacher/<int:pk>', views.update_teacher_view, name='update-teacher'),
    path('delete-teacher/<int:pk>', views.delete_teacher_view, name='delete-teacher'),
    path('admin-view-pending-teacher', views.admin_view_pending_teacher_view, name='admin-view-pending-teacher'),
    path('admin-view-teacher-salary', views.admin_view_teacher_salary_view, name='admin-view-teacher-salary'),
    path('approve-teacher/<int:pk>', views.approve_teacher_view, name='approve-teacher'),
    path('reject-teacher/<int:pk>', views.reject_teacher_view, name='reject-teacher'),

    # Admin - Student management
    path('admin-student', views.admin_student_view, name='admin-student'),
    path('admin-view-student', views.admin_view_student_view, name='admin-view-student'),
    path('admin-view-student-marks', views.admin_view_student_marks_view, name='admin-view-student-marks'),
    path('admin-view-marks/<int:pk>', views.admin_view_marks_view, name='admin-view-marks'),
    path('admin-check-marks/<int:pk>', views.admin_check_marks_view, name='admin-check-marks'),
    path('update-student/<int:pk>', views.update_student_view, name='update-student'),
    path('delete-student/<int:pk>', views.delete_student_view, name='delete-student'),

    # Admin - Course management
    path('admin-course', views.admin_course_view, name='admin-course'),
    path('admin-add-course', views.admin_add_course_view, name='admin-add-course'),
    path('admin-view-course', views.admin_view_course_view, name='admin-view-course'),
    path('delete-course/<int:pk>', views.delete_course_view, name='delete-course'),

    # Admin - Question management
    path('admin-question', views.admin_question_view, name='admin-question'),
    path('admin-add-question', views.admin_add_question_view, name='admin-add-question'),
    path('admin-view-question', views.admin_view_question_view, name='admin-view-question'),
    path('view-question/<int:pk>', views.view_question_view, name='view-question'),
    path('delete-question/<int:pk>', views.delete_question_view, name='delete-question'),

    # Admin - Institution management
    path('admin-institution-list', views.institution_list, name='institution-list'),
    path('add_institution/', views.add_institution, name='add_institution'),
    path('add_institution/admin_add_institution', views.admin_add_institution, name='admin_add_institution'),
    path('add_institution/admin_view_institution', views.admin_view_institution, name='admin-view-institution'),
    path('add_institution/student_view_institution', views.student_view_institution, name='student-view-institution'),

    

    # Group discussions
    path('discussions/', views.discussion_list, name='discussion_list'),
    path('view_discussion/', views.view_discussion, name='view_discussion'),
    path('addgd/', views.add_discussion, name='addgd'),
    path('staff_gd', views.staff_gd_view, name='staff_gd'),


     path('viewgd/', views.viewgd, name='viewgd'),


    # Feedback
    path('student/student-feedback/', views.student_feedback_view, name='student-feedback'),
    path('add-feedback/', views.add_feedback_view, name='add-feedback'),
    path('view-feedback/', views.views_feedback_view, name='views-feedback'),
    path('add_notification/admin_add_notification', views.admin_add_notification, name='admin_add_notification'),
    path('add_notification/admin_view_notification', views.admin_view_notification, name='admin_view_notification'),
    path('add_notification/student_view_notification', views.student_view_notification, name='student_view_notification'),

 path('career_prediction',views.career_prediction, name='career_prediction'),
 path('course/<int:course_id>/answers/', views.display_answers, name='display_answers'),
 path('teacher/edit-question/<int:question_id>/', views.teacher_edit_question_view, name='edit-question'),


path('admin_gd',views.admin_gd, name='admin_gd'),
path('admin_viewgd/', views.admin_viewgd, name='admin_viewgd'),

]

# Add media URL settings
if settings.DEBUG:  # Use static for media only during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
