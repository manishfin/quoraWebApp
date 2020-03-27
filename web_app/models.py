from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

class BaseClass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class User(AbstractUser):
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
    CHOICES = ((0, True),(1, False))
    is_anonymous = models.IntegerField(default=0, choices=CHOICES)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.question)
        super(Question, self).save(*args, **kwargs)


class Answer(BaseClass):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    CHOICES = ((0, True),(1, False))
    is_anonymous = models.IntegerField(default=0, choices=CHOICES)

    @classmethod
    def get_object(self, answer_id):
        try:
            answer = self.objects.get(id=answer_id)
        except self.DoesNotExist:
            answer = None
        return answer


class Comment(BaseClass):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    comment = models.TextField()


class Vote(BaseClass):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    upvote = models.BooleanField(null=True)
    downvote = models.BooleanField(null=True)

    @classmethod
    def get_object(self, user, answer):
        return self.objects.filter(user=user, answer=answer).first()