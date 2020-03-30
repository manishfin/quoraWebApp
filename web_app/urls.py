from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('add_question', views.add_question, name='add question'),
    path('edit_question/<str:que_slug>', views.edit_question, name='edit question'),
    path('delete_question/<str:que_slug>', views.delete_question, name='delete question'),
    path('add_answer/<str:que_slug>', views.add_answer, name="add answer"),
    path('edit_answer/<int:answer_id>', views.edit_answer, name='edit answer'),
    path('delete_answer/<int:answer_id>', views.delete_answer, name='delete answer'),
    path('question/<str:que_slug>', views.question, name="question"),
    path('add_comment', views.add_comment, name="add comment"),
    path('<int:answer_id>/add_upvote', views.add_upvote, name="add upvote"),
    path('<int:answer_id>/add_downvote', views.add_downvote, name="add downvote"),
    path('home', views.home, name='home'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile'),
]
