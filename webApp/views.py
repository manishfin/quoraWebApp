from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from webApp.models import User, Question
# Create your views here.
def home(request):
    if request.user.id is None:
        return redirect('/')
    questions = Question.objects.all()
    return render(request, 'home.html', {'questions': questions})


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


def add(request):
    if request.method == 'POST':
        question = request.POST['question']
        user = request.user
        que = Question(question=question, user=user)
        que.save()
    return redirect('home')