from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import auth
from django.contrib import messages
from webApp.models import User, Question, Answer, Comment, Vote
from .forms import UserSignUpForm

# TODO: use login_required decorator instead of user.is_authenticated
# TODO: Move upvote/downvote logic to model methods
# TODO: Rename your app from WebApp to web_app or web
# TODO: Move templates to app specific folder
# TODO: Update .gitignore
# TODO: Organize your views. Login/Logout/Signup views on the top and the remaining follows
# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect('/')
    comments = Comment.objects.all().order_by('-created_at')
    items = Question.objects.prefetch_related('answer_set')
    return render(request, 'home.html', {'items': items, 'comments': comments})


def question(request, que_slug):
    # TODO: except block is not required
    try:
        question = get_object_or_404(Question, slug=que_slug)
    except Question.DoesNotExist:
        question = None

    try:
        answer = Answer.objects.get(question=question)
    except Answer.DoesNotExist:
        answer = None

    comments = Comment.objects.filter(answer=answer)
    upvote_count = Vote.objects.filter(answer=answer, upvote=True).count()
    downvote_count = Vote.objects.filter(answer=answer, downvote=True).count()
    context = {
        'question': question,
        'answer': answer,
        'comments': comments,
        'comment_count': comments.count(),
        'upvote_count': upvote_count,
        'downvote_count': downvote_count,
    }
    return render(request, 'web_app/question.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            # messages.success(request, 'Login Success!')
            return redirect('home')

    return render(request, 'login.html')


def signup(request):
    form = UserSignUpForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)


def logout(request):
    auth.logout(request)
    return redirect('/')


def add_question(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            question = request.POST['question']
            que = Question(question=question, user=user)
            que.save()
            messages.success(request, 'Question added successfully!')
    else:
        messages.error(request, 'Login required!')
    return redirect('home')


def add_answer(request, que_slug):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            answer = request.POST['answer']
            question = Question.objects.get(slug=que_slug)
            is_anonymous = False if request.user.is_anonymous else True
            ans = Answer(question=question, answer=answer, user=user, is_anonymous=is_anonymous)
            ans.save()
            messages.success(request, 'Answer added successfully!')
    else:
        messages.error(request, 'Login required!')
    return redirect('home')


def add_comment(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            answer = Answer.objects.get(id=request.POST['answer_id'])
            comment = request.POST['comment']
            comment_obj = Comment(answer=answer, comment=comment, user=user)
            comment_obj.save()
            messages.success(request, 'Comment added successfully!')
    else:
        messages.error(request, 'Login required!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) or redirect('home')


def add_upvote(request, answer_id):
    user = request.user
    if user.is_authenticated:
        try:
            answer = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            answer = None
        if answer:
            vote = Vote.objects.filter(user=user, answer=answer).first()
            if vote:
                vote.upvote = not vote.upvote
                vote.downvote = False
                vote.save()
            else:
                vote = Vote(user=request.user, upvote=True, answer=answer)
                vote.save()

            if vote.upvote:
                messages.info(request, 'You upvoted for this answer!')
            else:
                messages.info(request, 'You removed upvote for this answer!')
    else:
        messages.error(request, 'Login required!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) or redirect('home')


def add_downvote(request, answer_id):
    user = request.user
    if user.is_authenticated:
        try:
            answer = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            answer = None
        if answer:
            vote = Vote.objects.filter(user=user, answer=answer).first()
            if vote:
                vote.downvote = not vote.downvote
                vote.upvote = False
            else:
                vote = Vote(user=request.user, downvote=True, answer=answer)
            if vote.downvote:
                messages.info(request, 'You downvoted for this answer!')
            else:
                messages.info(request, 'You removed downvote for this answer!')
            vote.save()
    else:
        messages.error(request, 'Login required!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) or redirect('home')


def profile(request):
    if not request.user.is_authenticated:
        return redirect('/')
    return render(request, 'profile.html')
