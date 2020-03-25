from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from webApp.models import User, Question, Answer, Comment
from django.db import connection
# Create your views here.
def home(request):
    if request.user.id is None:
        return redirect('/')
    questions = Question.objects.filter(answer=None)
    answers = Answer.objects.all().order_by('-updated_at')
    comments = Comment.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'questions': questions, 'answers': answers, 'comments': comments})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('home')

        return render(request, 'login.html')
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        user.save()
        return redirect('login')
    
    return render(request, 'signup.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def add_question(request):
    if request.method == 'POST':
        question = request.POST['question']
        user = request.user
        que = Question(question=question, user=user)
        que.save()
    return redirect('home')


def add_answer(request):
    if request.method == 'POST':
        answer = request.POST['answer']
        question = Question.objects.get(id=request.POST['question_id'])
        user = request.user
        is_anonymous = False if request.user.is_anonymous else True
        ans = Answer(question=question, answer=answer, user=user, is_anonymous=is_anonymous)
        ans.save()
    return redirect('home')


def add_comment(request):
    if request.method == 'POST':
        answer = Answer.objects.get(id=request.POST['answer_id'])
        user = request.user
        comment = request.POST['comment']
        comment_obj = Comment(answer=answer, comment=comment, user=user)
        comment_obj.save()
    return redirect('home')