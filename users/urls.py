"""livepolls URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from .import views

app_name = 'users'

urlpatterns = [
    path('', views.index, name='index'),
    path('/about', views.about, name='about'),
    path('/contact', views.contact, name='contact'),
    path('/mypolls', views.mypolls, name='mypolls'),
    path('/publicpolls', views.publicpolls, name='publicpolls'),
    path('/login', views.login, name='login'),
    path('/hlogout', views.hlogout, name="hlogout"),
    path('/signup', views.signup, name='signup'),
    path('/postpoll', views.postpoll, name='postpoll'),
    path('<int:question_id>/', views.details, name='details'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote')
]
