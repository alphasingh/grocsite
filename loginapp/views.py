from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='loginapp:login')
def index(request):
    return render(request, 'loginapp/index.html')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('loginapp:index')
    else:
        if request.method=='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('loginapp:index')
            else:
                messages.error(request,'Username or password is incorrect')
                #return render(request, 'loginapp/login.html', context)
        context = {}
        return render(request, 'loginapp/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('loginapp:login')

def register(request):
    if request.user.is_authenticated:
        return redirect('loginapp:index')
    else:
        registerForm = CreateUserForm()
        if request.method == 'POST':
            registerForm=CreateUserForm(request.POST)
            if registerForm.is_valid():
                registerForm.save()
                user = registerForm.cleaned_data.get('username')
                messages.success(request,'Hello '+user+', your account has been created successfully! 🚀')
                return redirect('loginapp:login')

        context = {'registerForm':registerForm}
        return render(request, 'loginapp/register.html',context)
