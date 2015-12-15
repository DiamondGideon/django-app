from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, render_to_response
from django.shortcuts import redirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .forms import MyUserCreateForm
from .forms import UserProfileForm

def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            args['login_error'] = "No such user"
            return render_to_response('loginsys/login.html', args)

    else:
        return render_to_response('loginsys/login.html', args)

def logout(request):
    auth.logout(request)
    return redirect('/')
#
# def register(request):
#     args = {}
#     args.update(csrf(request))
#     args['form'] = UserCreationForm()
#     if request.POST:
#         newuser_form = UserCreationForm(request.POST)
#         if newuser_form.is_valid():
#             newuser_form.save()
#             newuser = auth.authenticate(username=newuser_form.cleaned_data['username'], password = newuser_form.cleaned_data['password2'], is_stuff = True)
#             newuser.is_stuff = True
#             newuser.save()
#             auth.login(request,newuser)
#             return redirect('/')
#         else:
#             args['form'] = newuser_form
#     return render_to_response('loginsys/register.html', args)

# Create your views here.

def register(request):
    args = {}
    args.update(csrf(request))
    args['uform'] = MyUserCreateForm()
    args['pform'] = UserProfileForm
    if request.POST:
        newuser_form = MyUserCreateForm(request.POST)
        newprof_form = UserProfileForm(request.POST)
        if newuser_form.is_valid() and newprof_form.is_valid():
            user = newuser_form.save()
            profile = newprof_form.save(commit = False)
            profile.user = user
            profile.save()
            newuser = auth.authenticate(username = newuser_form.cleaned_data['username'],
                                        password = newuser_form.cleaned_data['password2'],
                                        is_staff = newuser_form.cleaned_data['is_staff'],
                                        email = newuser_form.cleaned_data['email'],
                                        )
            auth.login(request,newuser)
            return redirect('/')
        else:
            args['form'] = newuser_form
    return render_to_response('loginsys/register.html', args)

