from django.contrib import admin
from .models import User, Question, Answer, Comment, Category
# Register your models here.
admin.site.register([User, Question, Answer, Comment, Category])
