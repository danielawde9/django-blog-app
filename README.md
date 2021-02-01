
- [1. Initial Start](#1-initial-start)
- [2. Custom Users App](#2-custom-users-app)
  - [2.1. config/settings](#21-configsettings)
  - [2.2. users/models.py](#22-usersmodelspy)
  - [2.3. users/urls](#23-usersurls)
  - [2.4. users/views](#24-usersviews)
  - [2.5. users/forms.py](#25-usersformspy)
  - [2.6. users/admin.py](#26-usersadminpy)
- [3. Templates](#3-templates)
  - [3.1. config/settings.py](#31-configsettingspy)
  - [3.2. temlpates/base](#32-temlpatesbase)
    - [3.2.1. temlpates/home](#321-temlpateshome)
  - [3.3. templates/registration/login](#33-templatesregistrationlogin)
  - [3.4. templates/signup](#34-templatessignup)
  - [3.5. templates/registration/password_change_form](#35-templatesregistrationpassword_change_form)
  - [3.6. templates/registration/password_change_done](#36-templatesregistrationpassword_change_done)
  - [3.7. templates/registration/password_reset_form](#37-templatesregistrationpassword_reset_form)
  - [3.8. templates/registration/password_reset_complete](#38-templatesregistrationpassword_reset_complete)
  - [3.9. templates/registration/password_reset_confirm](#39-templatesregistrationpassword_reset_confirm)
  - [3.10. templates/registration/password_reset_done](#310-templatesregistrationpassword_reset_done)
    - [3.10.1. Email](#3101-email)
  - [3.11. templates/registration/password_reset_email](#311-templatesregistrationpassword_reset_email)
  - [3.12. config/urls](#312-configurls)
- [4. Pages App](#4-pages-app)
  - [4.1. Pattern in adding new pages](#41-pattern-in-adding-new-pages)
  - [4.2. config/urls](#42-configurls)
  - [4.3. pages/urls](#43-pagesurls)
  - [4.4. pages/views](#44-pagesviews)
  - [4.5. Adding bootstarp to templates html](#45-adding-bootstarp-to-templates-html)
    - [4.5.1. config/settings](#451-configsettings)
- [5. Articles App](#5-articles-app)
  - [5.1. articles/models](#51-articlesmodels)
  - [5.2. articles/admin](#52-articlesadmin)
  - [5.3. articles/views](#53-articlesviews)
- [6. Static](#6-static)
- [7. Git](#7-git)
  - [7.1. Creating a new repository](#71-creating-a-new-repository)
  - [7.2. Push an existing folder](#72-push-an-existing-folder)
  - [7.3. Push an existing Git repository](#73-push-an-existing-git-repository)
  - [7.4. If you want to remove folder form git and keep it locally](#74-if-you-want-to-remove-folder-form-git-and-keep-it-locally)
  - [7.5. Global .gitignore for your machine](#75-global-gitignore-for-your-machine)
  - [7.6. Generate SSH key](#76-generate-ssh-key)
- [8. Deployment](#8-deployment)
  - [8.1. Django Deplyoment Checklist](#81-django-deplyoment-checklist)
  - [8.2. Heroku](#82-heroku)
    - [8.2.1. Procfile](#821-procfile)
  - [8.3. Heroku Deployment](#83-heroku-deployment)


# 1. Initial Start

Create a folder, install django and run the shell

    $ cd ~/Desktop
    $ mkdir news
    $ cd news
    $ pipenv install django
    $ pipenv shell

it will create a pipenv environment start a project and don't forget the "." at the end of the code

    (news) $ django-admin startproject config .
    (news) $ python manage.py startapp users
    (news) $ python manage.py startapp pages
    (news) $ python manage.py startapp articles

Run server

    (news) $ python manage.py runserver


**Note** that we did not run migrate to configure our database. It’s important to wait until
after we’ve created our new custom user model before doing so given how tightly
connected the user model is to the rest of Django.

# 2. Custom Users App

Always use a **custom user model** for all new Django projects, using `AbstractUser` not `AbstractBaseUser`

Creating our custom user model requires four steps:

- update settings.py
- create a new CustomUser model
- update the admin
- create new forms for UserCreationForm and UserChangeForm

Tell django about the new app `pages` and `users` by adding it to the bottom of `INSTALLED_APPS` in the `config/settings.py`

## 2.1. config/settings

    INSTALLED_APPS = [

        # Local
        'users.apps.UsersConfig',
        'pages.apps.PagesConfig',
        'articles.apps.ArticlesConfig', 
    ]

    ...

    AUTH_USER_MODEL = 'users.CustomUser' # new

## 2.2. users/models.py

A model is the single, definitive source of information about your data. It contains the essential fields and behaviors
of the data you’re storing. Generally, each model maps to a **single database table.**


- Each model is a Python class that subclasses django.db.models.Model.
- Each attribute of the model represents a database field.
- With all of this, Django gives you an automatically-generated database-access API

We will “model” the characteristics of the data in our database.


    from django.db import models
    from django.contrib.auth.models import AbstractUser
    # Create your models here.

    class CustomUser(AbstractUser):
        age = models.PositiveIntegerField(null=True, blank=True)


- null is database-related. When a field has null=True it can store a database entry as NULL , meaning no value.
- blank is validation-related, if blank=True then a form will allow an empty value, whereas if blank=False then a value is required.

## 2.3. users/urls

**Note** signup page from the templates needs to be created first before adding the views and the urls, i added it here to group them together

    from django.urls import path

    from .views import SignUpView

    urlpatterns = [
        path('signup/', SignUpView.as_view(), name='signup'),
    ]

## 2.4. users/views

    from django.urls import reverse_lazy
    from django.views.generic import CreateView

    from .forms import CustomUserCreationForm


    class SignUpView(CreateView):
        form_class = CustomUserCreationForm
        success_url = reverse_lazy('login')
        template_name = 'signup.html'


Why use reverse_lazy here instead of reverse ? The reason is that for all generic class- based views the URLs are not loaded when the file is imported, so we have to use the lazy form of reverse to load them later when they’re available.


## 2.5. users/forms.py

create it first `touch users/forms.py`

    from django import forms
    from django.contrib.auth.forms import UserChangeForm, UserCreationForm

    from .models import CustomUser

    class CustomerUserCreationForm(UserCreationForm):
        class Meta(UserCreationForm.Meta):
            model = CustomUser
            # default forms - fields = UserCreationForm.Meta.fields + ('age',)
            fields = ('username', 'email', 'age',) # new after fixing the templates

    class CustomerUserChangeForm(UserChangeForm):
        class Meta:
            model = CustomUser
            # default forms - fields = UserChangeForm.Meta.fields
            fields = ('username', 'email', 'age',) 

The only other step we need is to update our admin.py file since Admin is tightly
coupled to the default User model. We will extend the existing UserAdmin class to
use our new CustomUser model.


## 2.6. users/admin.py

    from django.contrib import admin
    from django.contrib.auth.admin import UserAdmin

    # Register your models here.

    from .forms import CustomUserChangeForm, CustomUserCreationForm
    from .models import CustomUser

    class CustomUserAdmin(UserAdmin):
        add_form = CustomUserCreationForm
        form = CustomUserChangeForm
        model = CustomUser
        list_display = ['email', 'username', 'age', 'is_staff', ] # customize what to show


    admin.site.register(CustomUser,CustomUserAdmin)

make the migration

    (news) $ python manage.py makemigrations users
    (news) $ python manage.py migrate

**Super user**

    (news) $ python manage.py createsuperuser


# 3. Templates

**Note** templates are ch 9 of the book and ch 10 of the git repo

Create a project-level directory called templates, and a home.html template file. it will also be used for user authentication


    (news) $ mkdir templates
    (news) $ touch templates/home.html
    (news) $ touch templates/base.html
    (news) $ mkdir templates/registration
    (news) $ touch templates/registration/login.html
    (news) $ touch templates/signup.html

Add the settings.py directory of the template

## 3.1. config/settings.py

    TEMPLATES = [
    	{
    		...
    		'DIRS': [os.path.join(BASE_DIR, 'templates')], # new
    		...
    	},
    ]
    ...
    LOGIN_REDIRECT_URL = 'home'
    LOGOUT_REDIRECT_URL = 'home'

## 3.2. temlpates/base

    <!-- temlpates/base.html -->
    <html>
    <head>
        <title>{% block title %}Newspaper App{% endblock title %}</title>
    </head>
    <body>
        <header>
            <h1><a href="{% url 'home' %}">Django blog</a></h1>
        </header>
        <div>
            {% block content %}
            {% endblock content %}
        </div>
    </body>
    </html>

### 3.2.1. temlpates/home

In our templates file home.html we can use the Django Templating Language’s for a loop to list all the objects in
object_list Why **object_list** ? This is the name of the variable that ListView returns to us.

    <!-- templates/home.html -->
    {% extends 'base.html' %}
    {% block title %}Home{% endblock title %}

    {% block content %}
        {% for post in object_list %}
            <div class="post-entry">
                <h2><a href="">{{ post.title }}</a></h2>
                <p>{{ post.body }}</p>
            </div>
        {% endfor %}
    {% endblock content %}

In order to fix the naming of **object_list** we need to rename the return of the views of the `blog/views.py`
called `context_object_name = 'what ever name you want'` here we called `all_blog_list`

    <!-- templates/home.html -->
    {% extends 'base.html' %}

    {% block content %}
        {% for post in all_blog_list %}
            <div class="post-entry">
                <h2><a href="">{{ post.title }}</a></h2>
                <p>{{ post.body }}</p>
            </div>
        {% endfor %}
    {% endblock content %}


Adding user auth


    <!-- templates/home.html -->
    {% extends 'base.html' %}

    {% block content %}
        {% if user.is_authenticated %}
            Hi {{ user.username }}!
            <p><a href="{% url 'logout' %}">Log Out</a></p>

            {% for post in all_blog_list %}
                <div class="post-entry">
                    <h2><a href="">{{ post.title }}</a></h2>
                    <p>{{ post.body }}</p>
                </div>
            {% endfor %}
        {% else %}
            <p>You are not logged in</p>
            <a href="{% url 'login' %}">Log In</a> |
            <a href="{% url 'signup' %}">Sign Up</a>
        {% endif %}

    {% endblock content %}

## 3.3. templates/registration/login

    <!-- templates/registration/login.html -->

    {% extends 'base.html' %}
    {% block title %}Log In{% endblock title %}
    {% block content %}

    <h2>Log In</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
    <button class="btn btn-success ml-2" type="submit">Log In</button>
    </form>
    {% endblock content %}


- Adding a `{% csrf_token %}` which Django provides to protect our form from cross-
site scripting attacks. You should use it for all your Django forms.
- Then to output our form data we use `{{ form.as_p }}` which renders it within
paragraph <p> tags.
- the btn class is added after the bootstrap cripy installation


## 3.4. templates/signup

    <!-- templates/signup.html -->

    {% extends 'base.html' %}
    {% block title %}Sign Up{% endblock title %}
    {% block content %}

    <h2>Sign Up</h2>
    <form method="post">
        {% csrf_token %}
        # old {{ form.as_p }}
        {{ form|crispy }}
        <button class="btn btn-success" type="submit">Sign Up</button>    
        </form>
    {% endblock content %}

~~{{ form.as_p }}~~ will be replaced by `` after installing cripy (check pages app)

**Note I** Templates is for only html, dosen't have templates/urls.py nor views.py, it will be on the users/views and users/urls

**Note II** for a better form please install crispy form, check next chapter

## 3.5. templates/registration/password_change_form
Let’s customize these two password change pages so that they match the look and
feel of our Newspaper site. Because Django already has created the views and URLs
for us, we only need to add new templates.


    (news) $ touch templates/registration/password_change_form.html
    (news) $ touch templates/registration/password_change_done.html
    (news) $ touch templates/registration/password_reset_form.html
    (news) $ touch templates/registration/password_reset_done.html
    (news) $ touch templates/registration/password_reset_confirm.html
    (news) $ touch templates/registration/password_reset_complete.html


then

    {% extends 'base.html' %}

    {% block title %}Password Change{% endblock title %}

    {% block content %}
    <h1>Password change</h1>
    <p>Please enter your old password, for security's sake, and then enter your new password twice so we can verify you typed it in correctly.</p>

    <form method="POST">
        {% csrf_token %}
        {{ form.as_p }}
        <input class="btn btn-success" type="submit" value="Change my password">
    </form>
    {% endblock content %}

## 3.6. templates/registration/password_change_done

    {% extends 'base.html' %}

    {% block title %}Password Change Successful{% endblock title %}

    {% block content %}
        <h1>Password change successful</h1>
        <p>Your password was changed.</p>
    {% endblock content %}

## 3.7. templates/registration/password_reset_form
    {% extends 'base.html' %}

    {% block title %}Forgot Your Password?{% endblock title %}

    {% block content %}
    <h1>Forgot your password?</h1>
    <p>Enter your email address below, and we'll email instructions for setting a new one.</p>

    <form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input class="btn btn-success" type="submit" value="Send me instructions!">
    </form>
    {% endblock content %}
## 3.8. templates/registration/password_reset_complete

    {% extends 'base.html' %}

    {% block title %}Password reset complete{% endblock title %}

    {% block content %}
    <h1>Password reset complete</h1>
    <p>Your new password has been set. You can log in now on the <a href=\
    "{% url 'login' %}">log in page</a>.</p>
    {% endblock content %}
## 3.9. templates/registration/password_reset_confirm
    {% extends 'base.html' %}

    {% block title %}Enter new password{% endblock title %}

    {% block content %}
    <h1>Set a new password!</h1>
    <form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input class="btn btn-success" type="submit" value="Change my password">
    </form>
    {% endblock content %}
## 3.10. templates/registration/password_reset_done
    {% extends 'base.html' %}

    {% block title %}Email Sent{% endblock title %}

    {% block content %}
    <h1>Check your inbox.</h1>
    <p>We've emailed you instructions for setting your password. You should receive the email shortly!</p>
    {% endblock content %}

### 3.10.1. Email

using [sendgrid](https://sendgrid.com/), click on “Integrate using our Web API or SMTP relay” then “SMTP Relay”


    (news) $ touch templates/registration/password_reset_email.html
    (news) $ touch templates/registration/password_reset_subject.txt

and in the subject.txt add `Please reset your password`
## 3.11. templates/registration/password_reset_email


    {% load i18n %}{% autoescape off %}
    {% trans "Hi" %} {{ user.get_username }},

    {% trans "We've received a request to reset your password. If you didn't make\
    this request, you can safely ignore this email. Otherwise, click the button\
    below to reset your password." %}

    {% block reset_link %}
    {{ protocol }}://{{ domain }}{% url 'password_reset_confirm' uidb64=uid\
    token=token %}
    {% endblock reset_link %}
    {% endautoescape %}


## 3.12. config/urls

    from django.contrib import admin
    from django.urls import path, include
    from django.views.generic.base import TemplateView

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('users/', include('users.urls')),
        path('users/', include('django.contrib.auth.urls')),
        path('', include('pages.urls')), 
    ]


also the default template to be replaced when `pages app` created in urlpatterns

~~path('', TemplateView.as_view(template_name='home.html'), name='home'),~~

    path('', include('pages.urls')), # new

    # for the pass reset (debug mode)
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


    # for the pass reset (sendgrid production mode)
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 
    DEFAULT_FROM_EMAIL = 'your_custom_email_account'
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = 'apikey'
    EMAIL_HOST_PASSWORD = 'sendgrid_password'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True


# 4. Pages App
 
**Note I** templates are ch 10 of the book and ch 11 of the git repo Bootstrap
 
**Note II** all the new apps created plus the crispy for i already added it in first section Initial start


## 4.1. Pattern in adding new pages

```mermaid
graph LR
A[Templates] --> B((View))
B --> D{URL}
```
As for the URL

```mermaid
graph LR
A[App Level URL] --  Include all the links of the app --> B[Project Level URL]
```

Then we add the path of the `home` to `config/urls.py` that includes the URLs of pages/urls.py that have all the links inside it for the pages app


## 4.2. config/urls

    from django.contrib import admin
    from django.urls import path, include
    from django.views.generic.base import TemplateView

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('users/', include('users.urls')),
        path('users/', include('django.contrib.auth.urls')),
        path('', include('pages.urls')), 
    ]

## 4.3. pages/urls

    (news) $ touch pages/urls.py

    # pages/urls.py
    from django.urls import path
    from .views import HomePageView
    urlpatterns = [
        path('', HomePageView.as_view(), name='home'),
    ]

## 4.4. pages/views

    # pages/views.py

    from django.views.generic import TemplateView
    class HomePageView(TemplateView):
        template_name = 'home.html'


## 4.5. Adding bootstarp to templates html

check the code for templates (too big to add here)

we can customize login button

customizing the sign up pages adding crispy 

    (news) $ pipenv install django-crispy-forms

### 4.5.1. config/settings

in `INSTALLED_APPS` add

    # 3rd Party
    'crispy_forms', # new

and at the end of the file add

    CRISPY_TEMPLATE_PACK = 'bootstrap4'

# 5. Articles App


Next up we define our database model which contains four fields: title , body , date ,
and author

For the author field we want to reference our custom user
model `users.CustomUser` which we set in the `settings.py` file as `AUTH_USER_MODEL` .

We can do this via get_user_model. And we also implement the best practices of
defining a `get_absolute_url` from the beginning and a `__str__` method for viewing
the model in our admin interface.


## 5.1. articles/models

    from django.conf import settings
    from django.contrib.auth import get_user_model
    from django.db import models
    from django.urls import reverse


    class Article(models.Model):
        title = models.CharField(max_length=255)
        body = models.TextField()
        date = models.DateTimeField(auto_now_add=True)
        author = models.ForeignKey(
            get_user_model(),
            on_delete=models.CASCADE,
        )

        def __str__(self):
            return self.title

        def get_absolute_url(self):
            return reverse('article_detail', args=[str(self.id)])

we should use `get_absolute_url` It sets a canonical URL for an object so even if
the structure of your URLs changes in the future, the reference to the specific object
is the same. In short, you should add a `get_absolute_url()` and `__str__()` method to
**each model** you write.

Since we have a brand new app and model, it’s time to make a new migration file and
then apply it to the database.

    (news) $ python manage.py makemigrations articles
    (news) $ python manage.py migrate


## 5.2. articles/admin

register the app in admin 

    from django.contrib import admin
    from .models import Article
    admin.site.register(Article)


## 5.3. articles/views



# 6. Static

    (news) $ mkdir static

We can update settings.py with a one-line change for STATICFILES_DIRS . Add it at the bottom of the file below the entry
for STATIC_URL .

    # config/settings.py
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

Now create a css folder within static and add a new base.css file in it. Command Line

    (news) $ mkdir static/css
    (news) $ touch static/css/base.css

For example

    /* static/css/base.css */
    header h1 a {
    color: red;
    }

add `{% load static %}` to the top of base.html

Because our other templates inherit from `base.html` we only have to add this once. Include a new line at the bottom of
the <head></head> code that explicitly references our new base.css file.

    <!-- templates/base.html -->
    {% load static %}
    <html>
    <head>
        <title>Django blog</title>
        <link href="{% static 'css/base.css' %}" rel="stylesheet">
    </head>

# 7. Git

## 7.1. Creating a new repository

    git clone https://github.com/danielawde9/django-blog-app.git
    cd django-blog-app
    git add -A
    git commit -m "Initial Commit"
    git push -u origin master

## 7.2. Push an existing folder

    git init
    git add -A
    git commit -m 'initial commit'
    git remote add origin git@github.com:danielawde9django-blog-app.git
    git push -u origin master

## 7.3. Push an existing Git repository

    cd existing_repo
    git remote rename origin old-origin
    git remote add origin git@github.com:danielawde9/django-blog-app.git
    git push -u origin --all
    git push -u origin --tags

## 7.4. If you want to remove folder form git and keep it locally

    # Remove the file from the repository
    git rm --cached - r .idea/

    # now update your gitignore file to ignore this folder
    echo '.idea' >> .gitignore

    # add the .gitignore file
    git add .gitignore

    git commit -m "Removed .idea files"
    git push origin origin

## 7.5. Global .gitignore for your machine

    touch ~/.gitignore

Nano into it and add

    .idea

then in terminal

    git config --global core.excludesfile '~/.gitignore'

Now all future git repo will ignore .idea folder

## 7.6. Generate SSH key

    ssh-keygen -t ed25519 -C “Comment”

Then add .pub which is the public key to gitlab usually in `.ssh/key.pub`

<hr>

# 8. Deployment

## 8.1. Django Deplyoment Checklist

    Run manage.py check --deploy

The secret key must be a large random value and it must be kept secret.

Make sure that the key used in production isn’t used anywhere else and avoid committing it to source control. This reduces the number of vectors from which an attacker may acquire the key.

Instead of hardcoding the secret key in your settings module, consider loading it from an environment variable:

To be tested
import os
SECRET_KEY = os.environ['SECRET_KEY']

You must never enable debug in production.

You’re certainly developing your project with `DEBUG = True`, since

    ALLOWED_HOSTS = ['.herokuapp.com', 'localhost', '127.0.0.1']

## 8.2. Heroku

- update Pipfile.lock
- new Procfile
- install gunicorn
- update settings.py

**Check `Pipfile` python required version**

    [requires]
    python_version = "3.7"

Run `pipenv lock` to generate the appropriate `Pipfile.lock` incase its not present.

### 8.2.1. Procfile

Then create a Procfile which tells Heroku how to run the remote server where our code will live.

    touch Procfile

For now, we’re telling Heroku to use gunicorn as our production server and look in our blog_project.wsgi file for further instructions.

Inside the Procfile

    web: gunicorn blog_project.wsgi --log-file -

Next install gunicorn which we’ll use in production while still using Django’s internal server for local development use.

    (blog) $ pipenv install gunicorn

## 8.3. Heroku Deployment

Make sure to login

    (blog) $ heroku login
    (blog) $ heroku create

Now we need to add a **hook** for Heroku within a git. This means that git will store both our settings for pushing code
to Bitbucket and to Heroku.

My app name is `calm-badlands-09889` so the command will be

    (blog) $ heroku git:remote -a calm-badlands-09889

~~Tell Heroku to ignore static files which we’ll cover in-depth when deploying our Blog app later in the book.~~

`~~(blog) $ heroku config:set DISABLE_COLLECTSTATIC=1~~

There’s one more step we need to take now that we have static files, which in our
case is CSS. Django does not support serving static files in production however the
WhiteNoise project does. So let’s install it.

    (blog) $ pipenv install whitenoise

in our `settings.py` file add `ALLOWED_HOSTS`

    # blog_project/settings.py
    ALLOWED_HOSTS = ['*']

Add whitenoise to the INSTALLED_APPS above the built-
in staticfiles app and also to MIDDLEWARE on the third line. Order matters for both
INSTALLED_APPS and MIDDLEWARE .

    INSTALLED_APPS = [
        'blog.apps.BlogConfig',
        'accounts.apps.AccountsConfig',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'whitenoise.runserver_nostatic', # new!
        'django.contrib.staticfiles',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware', # new!
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

at the bottom add

    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # new!
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

Push the code to Heroku and add free scaling, so it’s actually running online, otherwise the code is just sitting there.

    (blog) $ git push heroku master
    (blog) $ heroku ps:scale web=1

also git commit and push
