from django.db import models

from student.models import Student
from django.contrib.auth.models import User

class Course(models.Model):
   course_name = models.CharField(max_length=50)
   question_number = models.PositiveIntegerField()
   total_marks = models.PositiveIntegerField()
   def __str__(self):
        return self.course_name

class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)

class Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=40,null=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name



from django.db import models

class GroupDiscussion(models.Model):
    title = models.CharField(max_length=200, help_text="Enter the title of the discussion")
    date = models.DateField(help_text="Enter the date of the discussion")
    time = models.TimeField(help_text="Enter the time of the discussion")
    link = models.URLField(max_length=500, help_text="Enter the Google Meet link")

    def __str__(self):
        return self.title


class Feedback(models.Model):
    feedback_title = models.CharField(max_length=200)
    username = models.CharField(max_length=100)
    feedback = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    def __str__(self):
        return f"Feedback from {self.username} - {self.feedback_title}"

from django.db import models

class Institution(models.Model):
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=15)  # Phone number or email
    courses_provided = models.TextField()  # You can use a ManyToManyField if linking to a Course model
    location = models.CharField(max_length=300)
    image = models.ImageField(upload_to='institution_images/')  # Requires `Pillow` library

    def __str__(self):
        return self.name

from django.db import models

class Notification(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text
    


