from django.shortcuts import render,redirect,reverse
from django.shortcuts import get_object_or_404

from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from teacher import models as TMODEL
from student import models as SMODEL
from teacher import forms as TFORM
from student import forms as SFORM
from django.contrib.auth.models import User

from .models import GroupDiscussion
from .forms import GroupDiscussionForm



def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'quiz/index.html')


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def afterlogin_view(request):
    if is_student(request.user):      
        return redirect('student/student-dashboard')
                
    elif is_teacher(request.user):
            return redirect('teacher/teacher-dashboard')
    else:
        return redirect('admin-dashboard')

from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout
@csrf_protect
def custom_logout_view(request):
        logout(request)
        return redirect('home')


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


def admin_dashboard_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'total_course':models.Course.objects.all().count(),
    'total_question':models.Question.objects.all().count(),
    }
    return render(request,'quiz/admin_dashboard.html',context=dict)

def admin_teacher_view(request):
    dict={
    'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'pending_teacher':TMODEL.Teacher.objects.all().filter(status=False).count(),
    'salary':TMODEL.Teacher.objects.all().filter(status=True).aggregate(Sum('salary'))['salary__sum'],
    }
    return render(request,'quiz/admin_teacher.html',context=dict)

def admin_view_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=True)
    return render(request,'quiz/admin_view_teacher.html',{'teachers':teachers})


def admin_teachernew_view(request):
    dict={
    'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'pending_teacher':TMODEL.Teacher.objects.all().filter(status=False).count(),
    'salary':TMODEL.Teacher.objects.all().filter(status=True).aggregate(Sum('salary'))['salary__sum'],
    }
    return render(request,'quiz/admin_teachernew.html',context=dict)

def admin_view_teachernew_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=True)
    return render(request,'quiz/admin_view_teachernew.html',{'teachers':teachers})



def update_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=TMODEL.User.objects.get(id=teacher.user_id)
    userForm=TFORM.TeacherUserForm(instance=user)
    teacherForm=TFORM.TeacherForm(request.FILES,instance=teacher)
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=TFORM.TeacherUserForm(request.POST,instance=user)
        teacherForm=TFORM.TeacherForm(request.POST,request.FILES,instance=teacher)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacherForm.save()
            return redirect('admin-view-teacher')
    return render(request,'quiz/update_teacher.html',context=mydict)



def delete_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-teacher')




def admin_view_pending_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=False)
    return render(request,'quiz/admin_view_pending_teacher.html',{'teachers':teachers})


def approve_teacher_view(request,pk):
    teacherSalary=forms.TeacherSalaryForm()
    if request.method=='POST':
        teacherSalary=forms.TeacherSalaryForm(request.POST)
        if teacherSalary.is_valid():
            teacher=TMODEL.Teacher.objects.get(id=pk)
            teacher.salary=teacherSalary.cleaned_data['salary']
            teacher.status=True
            teacher.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-pending-teacher')
    return render(request,'quiz/salary_form.html',{'teacherSalary':teacherSalary})

def reject_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-pending-teacher')

def admin_view_teacher_salary_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=True)
    return render(request,'quiz/admin_view_teacher_salary.html',{'teachers':teachers})

from .models import Notification
from .forms import NotificationForm

def admin_add_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_view_notification')  # Redirect to the view notifications page
    else:
        form = NotificationForm()

    return render(request, 'quiz/admin_add_notification.html', {'form': form})

def admin_view_notification(request):
    notifications = Notification.objects.all()
    return render(request, 'quiz/admin_view_notification.html', {'notifications': notifications})


def admin_student_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    }
    return render(request,'quiz/admin_student.html',context=dict)

def admin_view_student_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'quiz/admin_view_student.html',{'students':students})



def update_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=SMODEL.User.objects.get(id=student.user_id)
    userForm=SFORM.StudentUserForm(instance=user)
    studentForm=SFORM.StudentForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=SFORM.StudentUserForm(request.POST,instance=user)
        studentForm=SFORM.StudentForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
            return redirect('admin-view-student')
    return render(request,'quiz/update_student.html',context=mydict)



def delete_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/admin-view-student')


def admin_course_view(request):
    return render(request,'quiz/admin_course.html')


def admin_add_course_view(request):
    courseForm=forms.CourseForm()
    if request.method=='POST':
        courseForm=forms.CourseForm(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-course')
    return render(request,'quiz/admin_add_course.html',{'courseForm':courseForm})


def admin_view_course_view(request):
    courses = models.Course.objects.all()
    return render(request,'quiz/admin_view_course.html',{'courses':courses})

def delete_course_view(request,pk):
    course=models.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/admin-view-course')



def admin_question_view(request):
    return render(request,'quiz/admin_question.html')


def admin_add_question_view(request):
    questionForm=forms.QuestionForm()
    if request.method=='POST':
        questionForm=forms.QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            course=models.Course.objects.get(id=request.POST.get('courseID'))
            question.course=course
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-question')
    return render(request,'quiz/admin_add_question.html',{'questionForm':questionForm})


def admin_view_question_view(request):
    courses= models.Course.objects.all()
    return render(request,'quiz/admin_view_question.html',{'courses':courses})

def view_question_view(request,pk):
    questions=models.Question.objects.all().filter(course_id=pk)
    return render(request,'quiz/view_question.html',{'questions':questions})

def delete_question_view(request,pk):
    question=models.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/admin-view-question')

def admin_view_student_marks_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'quiz/admin_view_student_marks.html',{'students':students})

def admin_view_marks_view(request,pk):
    courses = models.Course.objects.all()
    response =  render(request,'quiz/admin_view_marks.html',{'courses':courses})
    response.set_cookie('student_id',str(pk))
    return response

def admin_check_marks_view(request,pk):
    course = models.Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student= SMODEL.Student.objects.get(id=student_id)

    results= models.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'quiz/admin_check_marks.html',{'results':results})
    




def aboutus_view(request):
    return render(request,'quiz/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'quiz/contactussuccess.html')
    return render(request, 'quiz/contactus.html', {'form':sub})


def admin_course1_view(request):
    return render(request,'quiz/admin_course1.html')

def admin_add_course1_view(request):
    courseForm=forms.CourseForm()
    if request.method=='POST':
        courseForm=forms.CourseForm(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-course')
    return render(request,'quiz/admin_add_course1.html',{'coursesForm':courseForm})

def admin_view_course1_view(request):
    courses = models.Course.objects.all()
    return render(request,'quiz/admin_view_course1.html',{'courses':courses})



def admin_customer_view(request):
    return render(request,'quiz/admin_customer.html')

def admin_view_customer_view(request):
    customers=models.Customer.objects.all()
    return render(request,'quiz/admin_view_customer.html',{'customers':customers})


def delete_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return redirect('admin-view-customer')


def update_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,request.FILES,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('admin-view-customer')
    return render(request,'quiz/update_customer.html',context=mydict)


def admin_add_customer_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('/admin-view-customer')
    return render(request,'quiz/admin_add_customer.html',context=mydict)


def admin1_view_customer_view(request):
    customers=models.Customer.objects.all()
    return render(request,'quiz/admin1_view_customer.html',{'customers':customers})



def discussion_list(request):
    discussions = GroupDiscussion.objects.all()  # Fetch all discussions from the database
    return render(request, 'student/discussion_list.html', {'discussions': discussions})


def add_discussion(request):
    if request.method == 'POST':
        form = GroupDiscussionForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new discussion to the database
            return redirect('discussion_list')  # Redirect to the discussion list
    else:
        form = GroupDiscussionForm()
    return render(request, 'teacher/add_discussion.html', {'form': form})

# View to handle displaying the details of a specific discussion
from django.shortcuts import render
from .models import GroupDiscussion

def view_discussion(request):
    # Fetch all discussions from the database
    discussions = GroupDiscussion.objects.all()
    return render(request, 'student/view_discussion.html', {'discussions': discussions})

def staff_gd_view(request):
    return render(request, 'teacher/staff_gd.html')


def viewgd(request):
    # Fetch all discussions from the database
    discussions = GroupDiscussion.objects.all()
    return render(request, 'teacher/viewgd.html', {'discussions': discussions})







from django.contrib import messages

from .forms import FeedbackForm  # Import your FeedbackForm



def student_feedback_view(request):
    """
    Handles student feedback submissions.
    """
    if request.method == 'POST':
        form = FeedbackForm(request.POST)  # Instantiate the form with POST data
        if form.is_valid():  # Validate the form data
            form.save()  # Save the data to the database
            messages.success(request, "Thank you for your feedback!")  # Success message
            return redirect('student-feedback')  # Redirect to avoid form resubmission
        else:
            messages.error(request, "There was an error with your submission. Please try again.")  # Error message
    else:
        form = FeedbackForm()  # Instantiate an empty form for GET requests

    context = {
        'form': form,  # Pass the form to the template
    }
    return render(request, 'student/student_feedback.html', context)  # Render the feedback template

def add_feedback_view(request):
    """
    Handles adding new feedback manually via a template.
    """
    if request.method == "POST":
        # Extract data from POST request
        feedback_title = request.POST.get('feedback_title', '').strip()
        username = request.POST.get('username', '').strip()
        feedback_text = request.POST.get('feedback', '').strip()
        rating = request.POST.get('rating')

        # Basic validation
        if not feedback_title or not username or not feedback_text or not rating:
            messages.error(request, "All fields are required. Please try again.")
        else:
            # Save feedback to the database
            models.Feedback.objects.create(
                feedback_title=feedback_title,
                username=username,
                feedback=feedback_text,
                rating=int(rating)
            )
            messages.success(request, "Feedback submitted successfully!")

    # Pass the rating range to the template
    return render(request, 'student/add_feedback.html', {'ratings': range(1, 6)})


def view_feedback_view(request):
    """
    Displays all feedback from the database.
    """
    feedbacks = models.Feedback.objects.all().order_by('-id')  # Fetch feedbacks in descending order
    # Pass the feedback data to the template
    return render(request, 'student/view_feedback.html', {'feedbacks': feedbacks})

def views_feedback_view(request):
    """
    Displays all feedback from the database.
    """
    feedbacks = models.Feedback.objects.all().order_by('-id')  # Fetch feedbacks in descending order
    # Pass the feedback data to the template
    return render(request, 'student/view_feedback.html', {'feedbacks': feedbacks})


from .models import Institution
from .forms import InstitutionForm

# View to list all institutions
from django.shortcuts import render
from .models import Institution  # Assuming you have an Institution model

# Create a view to display the list of institutions
def institution_list(request):
    # Query the Institution model to get all institutions
    institutions = Institution.objects.all()

    # Render the template with the list of institutions
    return render(request, 'quiz/institution_list.html', {'institutions': institutions})

# View to add a new institution




def add_institution(request):
    return render(request,'quiz/add_institution.html')


def admin_add_institution(request):
    if request.method == "POST":
        form = InstitutionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_add_institution')  # Redirect to the admin page
    else:
        form = InstitutionForm()

    return render(request, 'quiz/admin_add_institution.html', {'form': form})


from django.shortcuts import render
from .models import Institution

def admin_view_institution(request):
    institutions = Institution.objects.all()  # Fetch all institutions
    return render(request, 'quiz/admin_view_institution.html', {'institutions': institutions})

def student_view_institution(request):
    institutions = Institution.objects.all()  # Fetch all institutions
    return render(request, 'student/student_view_institution.html', {'institutions': institutions})

from .models import Notification
from .forms import NotificationForm

def admin_add_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_view_notification')  # Redirect to the view notifications page
    else:
        form = NotificationForm()

    return render(request, 'quiz/admin_add_notification.html', {'form': form})

def admin_view_notification(request):
    notifications = Notification.objects.all()
    return render(request, 'quiz/admin_view_notification.html', {'notifications': notifications})

from django.shortcuts import render
import joblib
import numpy as np
from django.shortcuts import render
import joblib


def student_view_notification(request):
    notifications = Notification.objects.all()
    return render(request, 'student/student_view_notification.html', {'notifications': notifications})

from django.shortcuts import render
import joblib
import numpy as np
from django.shortcuts import render
import joblib









def career_prediction(request):
    skill_labels = {
        "database_fundamentals": "Database Fundamentals",
        "computer_architecture": "Computer Architecture",
        "distributed_computing": "Distributed Computing",
        "cyber_security": "Cyber Security",
        "networking": "Networking",
        "software_development": "Software Development",
        "programming_skills": "Programming Skills",
        "project_management": "Project Management",
        "computer_forensics": "Computer Forensics",
        "technical_communication": "Technical Communication",
        "ai_ml": "AI/ML",
        "software_engineering": "Software Engineering",
        "business_analysis": "Business Analysis",
        "communication_skills": "Communication Skills",
        "data_science": "Data Science",
        "troubleshooting_skills": "Troubleshooting Skills",
        "graphics_designing": "Graphics Designing"
    }

    if request.method == 'POST':
        user_input = [int(request.POST.get(skill, 0)) for skill in skill_labels]
        model = joblib.load('career.pkl')
        prediction = model.predict([user_input])
        return render(request, 'student/result.html', {'prediction': prediction[0]})

    return render(request, 'student/index.html', {'skill_labels': skill_labels})

from django.shortcuts import render, get_object_or_404
from .models import Course, Question

def display_answers(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = Question.objects.filter(course=course)

    return render(request, 'student/display_answers.html', {
        'course': course,
        'questions': questions,
    })





from django.http import HttpResponseRedirect
from .models import Question, Course
from .forms import QuestionForm  # Assuming your form is inside forms.py

def teacher_edit_question_view(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('/teacher/teacher-view-question')  # Redirect to question list
    else:
        form = QuestionForm(instance=question)
    
    return render(request, 'teacher/teacher_edit_question.html', {'form': form, 'question': question})






def admin_gd(request):
    return render(request, 'quiz/admingd.html')




def admin_viewgd(request):
    # Fetch all discussions from the database
    discussions = GroupDiscussion.objects.all()
    return render(request, 'quiz/admin_viewgd.html', {'discussions': discussions})

