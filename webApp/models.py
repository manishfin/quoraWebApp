from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=50, unique=True)
    dob = models.DateField()
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

class Category(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()

class Question(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    question = models.TextField()
    upvote = models.IntegerField()
    downvote = models.IntegerField()
    created_at = models.DateField()
    updated_at = models.DateField()
    type = models.CharField(max_length=30)
    CHOICES = ((0, True),(1, False))
    is_anonymous = models.IntegerField(default=0, choices=CHOICES)

class Answer(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    created_at = models.DateField()
    updated_at = models.DateField()
    CHOICES = ((0, True),(1, False))
    is_anonymous = models.IntegerField(default=0, choices=CHOICES)

class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    comment = models.TextField()
    upvote = models.IntegerField()
    downvote = models.IntegerField()
    date = models.DateField()
