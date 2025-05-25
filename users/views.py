from django.shortcuts import render,HttpResponseRedirect
from django.contrib import auth
from users.models import User
from users.forms import UserLoginForm,UserRegistrationForm, UserUpdateForm
from django.urls import reverse

def login(request):
    if request.method=='POST':
        form=UserLoginForm(data=request.POST)
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user=auth.authenticate(username=username,password=password)
            if user:
                auth.login(request,user)
                return HttpResponseRedirect(reverse('home'))

    else:
        form=UserLoginForm()
    context={'form': form}
    return render(request,'users/login.html',context)

def registration(request):
    if request.method=='POST':
        form=UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
    else:        
        form=UserRegistrationForm()
    context={'form':form}

    return render(request,'users/reg.html',context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('home'))

def profile(request):
    if request.method=='POST':
        form=UserUpdateForm(instance=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile'))
        else:
            print(form.errors)
    else:
        form=UserUpdateForm(instance=request.user)
    context={'title':'Профіль', 'form':form}
    return render(request,'users/profile.html',context)