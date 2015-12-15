from django.shortcuts import render
from django.utils import timezone
from .models import Post
from .models import UserProfile
from .models import RaceBet
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from .forms import BetForm
from .forms import ResultForm
from django.shortcuts import redirect
from django.contrib import auth
from django.db import models
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


def post_list(request):
    args = {}
    args['posts'] = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    if auth.get_user(request).pk != None:
        args['profile'] = UserProfile.objects.get(user = auth.get_user(request))
    return render(request, 'horserace/post_list.html', args)

def post_home(request):
    args = {}
    if auth.get_user(request).pk != None:
     args['profile'] = UserProfile.objects.get(user = auth.get_user(request))
    return render(request, 'horserace/carousel.html', args)

def post_detail(request, pk):
        args = {}
        args['post'] = get_object_or_404(Post, pk=pk)
        if auth.get_user(request).pk != None:
            args['profile'] = UserProfile.objects.get(user = auth.get_user(request))
        args['bets'] = RaceBet.objects.filter(race = args['post']).order_by('bet')
        return render(request, 'horserace/post_detail.html', args)

@login_required(login_url='/auth/login/')
def post_make_bet(request, pk):
        args = {}
        if auth.get_user(request).pk != None:
                args['profile'] = UserProfile.objects.get(user=request.user)#UserProfile.objects.get(user = auth.get_user(request))
                balance = args['profile'].balance
        post = get_object_or_404(Post, pk=pk)
        if request.POST:

                    args['bform'] = BetForm(request.POST,balance = balance)
                    # print(int(args['bform'].cleaned_data.get("bet")))
                    # print(int(balance))
                    if args['bform'].is_valid() and int(args['bform'].cleaned_data.get("bet")) <= int(balance):
                        bet = args['bform'].save(commit = False)
                        bet.bet = args['bform'].cleaned_bet()
                        bet.race = post
                        # bet.user = args['profile']
                        bet.user = auth.get_user(request)
                        args['profile'].balance -= args['bform'].cleaned_bet()
                        args['profile'].save()
                        bet.save()
                        # args['profile'].update()
                        return redirect('horserace.views.post_detail', pk=pk, )
        else:
            args['bform'] = BetForm(balance= balance)
        return render(request, 'horserace/post_make_bet.html', args)

def post_result_and_delete(request, pk):
        args = {}
        if auth.get_user(request).pk != None:
                args['profile'] = UserProfile.objects.get(user=request.user)#UserProfile.objects.get(user = auth.get_user(request))
        args['post'] = get_object_or_404(Post, pk=pk)
        args['bets'] = RaceBet.objects.filter(race = args['post'])
        if request.method == "POST":
            args['form'] = ResultForm(request.POST)
            if args['form'].is_valid():
                for bet in args['bets']:
                    args['post'].result = args['form'].cleaned_data['result']
                    args['post'].save()
                    current_profile = UserProfile.objects.get(user = bet.user)
                    result = args['post'].result
                    if(int(result) == int(bet.result)):
                        current_profile.balance += (args['post'].win_coef/100+1)*bet.bet
                        current_profile.save()
                    return redirect('show_result', pk=pk, )
                # args['post'].published_date = None
                # args['post'].save()
        else:
            args['form'] = ResultForm()
        return render(request, 'horserace/post_set_result.html', args)

def show_result(request, pk):
    args = {}
    if auth.get_user(request).pk != None:
                args['profile'] = UserProfile.objects.get(user=request.user)#UserProfile.objects.get(user = auth.get_user(request))
    args['post'] = get_object_or_404(Post, pk=pk)
    args['bets'] = RaceBet.objects.filter(result = args['post'].result, race = args['post'])
    return render(request, 'horserace/post_results.html', args)


def post_new(request):
    args = {}
    if auth.get_user(request).pk != None:
        args['profile'] = UserProfile.objects.get(user = auth.get_user(request))
    if request.method == "POST":
            args['form'] = PostForm(request.POST)
            if args['form'].is_valid():
                post = args['form'].save(commit=False)
                post.author = args['profile']
                post.published_date = timezone.now()
                post.save()
                return redirect('horserace.views.post_detail', pk=post.pk, )
    else:
            args['form'] = PostForm()
    return render(request, 'horserace/post_edit.html', args)

def post_edit(request, pk):
        args = {}
        if auth.get_user(request).pk != None:
         args['profile'] = UserProfile.objects.get(user = auth.get_user(request))
        args['post'] = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            args['form'] = PostForm(request.POST, instance=args['post'])
            if args['form'].is_valid():
                args['post'] = args['form'].save(commit=False)
                args['post'].author = args['profile']
                args['post'].published_date = timezone.now()
                args['post'].save()
                return redirect('horserace.views.post_detail', pk=args['post'].pk)
        else:
            args['form'] = PostForm(instance=args['post'])
        return render(request, 'horserace/post_edit.html', args)

