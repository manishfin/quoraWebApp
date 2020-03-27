from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import auth
from django.contrib import messages
from web_app.models import User, Question, Answer, Comment, Vote
from .forms import UserSignUpForm


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            # messages.success(request, 'Login Success!')
            return redirect('web_app/home')
        else:
            messages.error(request, 'Login error! User does not exists.')
    return render(request, 'web_app/login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def signup(request):
    form = UserSignUpForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('web_app/login')
    context = {
        'form': form,
    }
    return render(request, 'web_app/signup.html', context)


def question(request, que_slug):
    question = get_object_or_404(Question, slug=que_slug)
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


@login_required
def home(request):
    comments = Comment.objects.all().order_by('-created_at')
    items = Question.objects.prefetch_related('answer_set')
    return render(request, 'web_app/home.html', {'items': items, 'comments': comments})


@login_required
def add_question(request):
    user = request.user
    if request.method == 'POST':
        question = request.POST['question']
        que = Question(question=question, user=user)
        que.save()
        messages.success(request, 'Question added successfully!')
    return redirect('web_app/home')


@login_required
def edit_question(request, que_slug):
    que = get_object_or_404(Question, slug=que_slug)
    user = request.user
    if user.id == que.user.id:
        que.question = request.POST['question']
        que.save()
        messages.info('Question has been updated!')
    else:
        messages.info('User do not have permission to update this question!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) or redirect('web_app/home')


@login_required
def add_answer(request, que_slug):
    user = request.user
    if request.method == 'POST':
        answer = request.POST['answer']
        question = Question.objects.get(slug=que_slug)
        is_anonymous = False if request.user.is_anonymous else True
        ans = Answer(question=question, answer=answer, user=user, is_anonymous=is_anonymous)
        ans.save()
        messages.success(request, 'Answer added successfully!')
    return redirect('web_app/home')


@login_required
def edit_answer(request, answer_id):
    ans = get_object_or_404(Answer, pk=answer_id)
    user = request.user
    if user.id == ans.user.id:
        ans.answer = request.POST['answer']
        ans.save()
        messages.info('Answer has been updated!')
    else:
        messages.info('User do not have permission to update this answer!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) or redirect('web_app/home')


@login_required
def add_comment(request):
    user = request.user
    if request.method == 'POST':
        answer = Answer.objects.get(id=request.POST['answer_id'])
        comment = request.POST['comment']
        comment_obj = Comment(answer=answer, comment=comment, user=user)
        comment_obj.save()
        messages.success(request, 'Comment added successfully!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) or redirect('web_app/home')


@login_required
def add_upvote(request, answer_id):
    user = request.user
    answer = Answer.get_object(answer_id)
    if answer:
        vote = Vote.get_object(user, answer)
        if vote:
            vote.upvote = not vote.upvote
            vote.downvote = False
        else:
            vote = Vote(user=request.user, upvote=True, answer=answer)
        if vote.upvote:
            messages.info(request, 'You upvoted for this answer!')
        else:
            messages.info(request, 'You removed upvote for this answer!')
        vote.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) or redirect('web_app/home')


@login_required
def add_downvote(request, answer_id):
    user = request.user
    answer = Answer.get_object(answer_id)
    if answer:
        vote = Vote.get_object(user, answer)
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
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) or redirect('web_app/home')


@login_required
def profile(request):
    return render(request, 'web_app/profile.html')