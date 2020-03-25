from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('add_question', views.add_question, name='add question'),
    path('add_answer', views.add_answer, name="add answer"),
    path('add_comment', views.add_comment, name="add comment"),
    path('home', views.home, name='home'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
]
