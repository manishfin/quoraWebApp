from django.db import models

class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    dob = models.DateField()
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['username'], name="username")
        ]

class Category(models.Model):
    name = models.CharField(max_lenght=20)
    type = models.CharField(max_length=30)
    subType = models.CharField(max_length=50)
    description = models.TextField()

class Question(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    categoryId = models.ForeignKey(Category, on_delete=models.CASCADE)
    question = models.TextField()
    upvote = models.IntegerField()
    downvote = models.IntegerField()
    createdAt = models.DateField()
    updatedAt = models.DateField()
    isAnonymous = models.IntegerField(max_length=1, default=0, choices=(0, 1))

class Answer(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    questionId = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    createdAt = models.DateField()
    updatedAt = models.DateField()
    isAnonymous = models.IntegerField(max_length=1, default=0, choices=(0, 1))