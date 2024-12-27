MCQ APP
1. Download and install anaconda3
2. Set system environment variable file path
---User/user/anaconda3
---User/user/anaconda3/Scripts
---User/user/anaconda3/Library/bin
3.Open vs code and terminal then under cmd
     Change directory to your current working directory and then type
	conda create -p env python -y
        conda init
	conda activate env/
4.pip install Django 
	python -m django --version
	django-admin startproject MCQ
5. Open Django folder in Vs-code
6.cd D:\Django\MCQ\MCQ_APP
7. D:\Django\MCQ\MCQ_APP>python manage.py runserver (To run project in localhost)
8.Press ctrl+c to interrupt runserver
9. To create app inside project D:\Django\MCQ\MCQ_APP>python manage.py startapp Quiz
10.D:\Django\MCQ\MCQ_APP>python manage.py migrate
11. Create urls.py file under Quiz folder.
12. Copy urls.py file content and paste it into newly created file.
13. Under urls.py import views and create index views under views.py
14. import include inside urls.py of MCQ_APP and set url as Quiz.urls.
14. Create folder templates and static under MCQ_APP and create base.html file under template
15.Under setting.py inside TEMPLATES
DIR:[os.path.join(BASE_DIR,'templates')]
16.Create a static folder inside MCQ_APP and create
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
17.{% load static %} under base.html to load css file from static folder
18 Create two files config.py and services.py under Quiz folder and import necessary libraries and also perform database connection activities.
19. Goto open ai website and generate api key under dashboard.
20. pip install openai
21. Go to views.py and do some coding..







