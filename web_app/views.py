from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import auth
from django.contrib import messages
from web_app.models import User, Question, Answer, Comment, Vote
from .forms import UserSignUpForm, QuestionForm, AnswerForm


def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            # messages.success(request, 'Login Success!')
            return redirect('home')
        else:
            messages.error(request, 'Login error! User does not exists.')
    return render(request, 'web_app/login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    form = UserSignUpForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
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
    comments = Comment.objects.filter(answer=answer).order_by('-created_at')
    upvote_count = Vote.objects.filter(answer=answer, upvote=True).count()
    downvote_count = Vote.objects.filter(answer=answer, downvote=True).count()
    context = {
        'question': question,
        'answer': answer,
        'comments': comments,
        'comment_count': comments.count(),
        'upvote_count': upvote_count,
        'downvote_count': downvote_count,
        'que_form': QuestionForm(),
        'ans_form': AnswerForm()
    }
    return render(request, 'web_app/question.html', context)


@login_required
def home(request):
    comments = Comment.objects.all().order_by('-created_at')
    items = Question.objects.prefetch_related('answer_set').order_by('-created_at')
    context = {
        'items': items,
        'comments': comments,
        'que_form': QuestionForm(),
        'ans_form': AnswerForm(),
    }
    return render(request, 'web_app/home.html', context)


@login_required
def add_question(request):
    user = request.user
    form = QuestionForm(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = user
        instance.save()
        messages.success(request, 'Question added successfully!')
    else:
        messages.error(request, 'Error occurred while adding the question!')
    return redirect('home')


@login_required
def edit_question(request, que_slug):
    que = get_object_or_404(Question, slug=que_slug)
    user = request.user
    if user.id == que.user.id:
        que.question = request.POST['question']
        que.save()
        messages.info(request, 'Question has been updated!')
    else:
        messages.info(request, 'User do not have permission to update this question!')
    return redirect('/question/'+que.slug)


@login_required
def delete_question(request, que_slug):
    que = get_object_or_404(Question, slug=que_slug)
    user = request.user
    if user.id == que.user.id:
        que.delete()
        messages.info(request, 'Question has been deleted!')
    else:
        messages.info(request, 'User do not have permission to delete this question!')
    return redirect('home')


@login_required
def add_answer(request, que_slug):
    question = get_object_or_404(Question, slug=que_slug)
    user = request.user
    form = AnswerForm(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = user
        instance.question = question
        instance.save()
        messages.success(request, 'Answer added successfully!')
    else:
        messages.error(request, 'Error occurred while adding the answer!')
    return redirect('home')


@login_required
def edit_answer(request, answer_id):
    ans = get_object_or_404(Answer, pk=answer_id)
    user = request.user
    if user.id == ans.user.id:
        ans.answer = request.POST['answer']
        ans.save()
        messages.info(request, 'Answer has been updated!')
    else:
        messages.info(request, 'User do not have permission to update this answer!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) or redirect('home')


@login_required
def delete_answer(request, answer_id):
    ans = get_object_or_404(Question, pk=answer_id)
    user = request.user
    if user.id == ans.user.id:
        ans.delete()
        messages.info(request, 'Answer has been deleted!')
    else:
        messages.info(request, 'User do not have permission to delete this answer!')
    return redirect('home')


@login_required
def add_comment(request):
    user = request.user
    if request.method == 'POST':
        answer = Answer.objects.get(id=request.POST['answer_id'])
        comment = request.POST['comment']
        comment_obj = Comment(answer=answer, comment=comment, user=user)
        comment_obj.save()
        messages.success(request, 'Comment added successfully!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) or redirect('home')


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
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) or redirect('home')


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
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) or redirect('home')


@login_required
def profile(request):
    return render(request, 'web_app/profile.html')