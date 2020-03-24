from django.db import models
from django.contrib.auth.models import AbstractUser

class BaseClass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, unique=True)
    dob = models.DateField(null=True)
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)


class Category(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(null=True)


class Question(BaseClass):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    question = models.TextField()
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)
    CHOICES = ((0, True),(1, False))
    is_anonymous = models.IntegerField(default=0, choices=CHOICES)


class Answer(BaseClass):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    CHOICES = ((0, True),(1, False))
    is_anonymous = models.IntegerField(default=0, choices=CHOICES)


class Comment(BaseClass):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    comment = models.TextField()
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)
