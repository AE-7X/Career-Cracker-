<<<<<<< HEAD
# Career-Cracker-
Career Cracker is a cutting-edge career development platform designed to empower individuals in today’s fast-changing and competitive job market. Leveraging Artificial Intelligence (AI) and Machine Learning (ML), it provides personalized career guidance for students, professionals, and mentors.

The platform simplifies career decision-making by offering AI-powered career suggestions, aptitude tests, interview simulations, and continuous performance evaluations. A built-in chatbot enhances user engagement by providing real-time career advice, study materials, and grooming tips — ensuring users are always prepared for their goals.

Career Cracker is developed using Python and Django for the backend, and JavaScript, HTML, CSS, and Bootstrap for the frontend. It integrates essential libraries like NumPy, Pandas, Scikit-Learn, Matplotlib, and NLTK for data processing, visualization, machine learning, and natural language processing.

Organized into Admin, Staff, and User modules, Career Cracker delivers smooth account management, assessment tracking, and resource sharing — making it a complete, intelligent, and user-friendly platform for career growth and development.
=======
# Online Quiz
![developer](https://img.shields.io/badge/Developed%20By%20%3A-Sumit%20Kumar-red)
---
## screenshots
### Homepage
![homepage snap](https://github.com/sumitkumar1503/onlinequiz/blob/master/static/screenshots/homepage.png?raw=true)
### Admin Dashboard
![dashboard snap](https://github.com/sumitkumar1503/onlinequiz/blob/master/static/screenshots/adminhomepage.png?raw=true)
### Exam Rules
![invoice snap](https://github.com/sumitkumar1503/onlinequiz/blob/master/static/screenshots/rules.png?raw=true)
### Exam
![doctor snap](https://github.com/sumitkumar1503/onlinequiz/blob/master/static/screenshots/exam.png?raw=true)
### Teacher
![doctor snap](https://github.com/sumitkumar1503/onlinequiz/blob/master/static/screenshots/teacher.png?raw=true)
---
## Functions
### Admin
- Create Admin account using command
```
py manage.py createsuperuser
```
- After Login, can see Total Number Of Student, Teacher, Course, Questions are there in system on Dashboard.
- Can View, Update, Delete, Approve Teacher.
- Can View, Update, Delete Student.
- Can Also See Student Marks.
- Can Add, View, Delete Course/Exams.
- Can Add Questions To Respective Courses With Options, Correct Answer, And Marks.
- Can View And Delete Questions Too.

### Teacher
- Apply for job in System. Then Login (Approval required by system admin, Then only teacher can login).
- After Login, can see Total Number Of Student, Course, Questions are there in system on Dashboard.
- Can Add, View, Delete Course/Exams.
- Can Add Questions To Respective Courses With Options, Correct Answer, And Marks.
- Can View And Delete Questions Too.
> **_NOTE:_**  Basically Admin Will Hire Teachers To Manage Courses and Questions.

### Student
- Create account (No Approval Required By Admin, Can Login After Signup)
- After Login, Can See How Many Courses/Exam And Questions Are There In System On Dashboard.
- Can Give Exam Any Time, There Is No Limit On Number Of Attempt.
- Can View Marks Of Each Attempt Of Each Exam.
- Question Pattern Is MCQ With 4 Options And 1 Correct Answer.
---

## HOW TO RUN THIS PROJECT
- Install Python(3.7.6) (Dont Forget to Tick Add to Path while installing Python)
- Open Terminal and Execute Following Commands :
```
python -m pip install -r requirements. txt
```
- Download This Project Zip Folder and Extract it
- Move to project folder in Terminal. Then run following Commands :
```
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
```
- Now enter following URL in Your Browser Installed On Your Pc
```
http://127.0.0.1:8000/
```

## CHANGES REQUIRED FOR CONTACT US PAGE
- In settins.py file, You have to give your email and password
```
EMAIL_HOST_USER = 'youremail@gmail.com'
EMAIL_HOST_PASSWORD = 'your email password'
EMAIL_RECEIVING_USER = 'youremail@gmail.com'
```

## Drawbacks/LoopHoles
- Admin/Teacher can add any number of questions to any course, But while adding course, admin provide question number.


## Feedback
Any suggestion and feedback is welcome. You can message me on facebook
- [Contact on Facebook](https://fb.com/sumit.luv)
- [Subscribe my Channel LazyCoder On Youtube](https://youtube.com/lazycoders)
>>>>>>> 3adff73 (Initial commit for My New Project)
