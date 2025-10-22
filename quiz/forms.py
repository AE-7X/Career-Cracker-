from django import forms
from django.contrib.auth.models import User
from . import models
from .models import Feedback

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class TeacherSalaryForm(forms.Form):
    salary=forms.IntegerField()

class CourseForm(forms.ModelForm):
    class Meta:
        model=models.Course
        fields=['course_name','question_number','total_marks']

class QuestionForm(forms.ModelForm):
    
    #this will show dropdown __str__ method course model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in course model and return it
    courseID=forms.ModelChoiceField(queryset=models.Course.objects.all(),empty_label="Course Name", to_field_name="id")
    class Meta:
        model=models.Question
        fields=['marks','question','option1','option2','option3','option4','answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }
class CoursesForm(forms.ModelForm):
    class Meta:
        model=models.Course
        fields=['course_name','question_number','total_marks']

class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields=['address','mobile','profile_pic']



        
from django import forms
from .models import GroupDiscussion

class GroupDiscussionForm(forms.ModelForm):
    class Meta:
        model = GroupDiscussion
        fields = ['title', 'date', 'time', 'link']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'link': forms.URLInput(attrs={'placeholder': 'https://meet.google.com/...'}),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_title', 'username', 'feedback', 'rating']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

from django import forms
from .models import Institution

class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ['name', 'contact', 'courses_provided', 'location', 'image']
        widgets = {
            'courses_provided': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter courses separated by commas'}),
        }
from django import forms
from .models import Notification

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Add Notification', 'class': 'notification-input'})
        }