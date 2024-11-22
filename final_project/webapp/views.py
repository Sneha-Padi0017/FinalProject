import numpy as np
import os
from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import CreateUserForm
import pickle
# Create your views here.
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    return render(request, 'accounts/index.html')

@login_required(login_url='login')
def home1(request):
    return render(request, 'accounts/index.html')

@login_required(login_url='login')
def predict(request):
    r1 = int(request.POST.dict()['val1'])
    r2 = int(request.POST.dict()['val2'])
    r3 = int(request.POST.dict()['val3'])
    r4 = int(request.POST.dict()['val4'])
    r5= int(request.POST.dict()['val5'])
    # with open("random_forest_regressor_model.pkl", 'rb') as file:
    #     loaded_model = pickle.load(file)
    # loaded_model = pickle.load(open('rf_model.sav', 'rb'))
    
    from joblib import dump, load
    loaded_model = load('rf_model.sav')
    
    result = loaded_model.predict([[r1,r2,r3,r4,r5]])
    print(result)
    rounded_number = round(result[0], 2)
    bb=""
    
    if rounded_number < 50:
        bb = "Low"
    elif rounded_number >50 and rounded_number<100:
        bb="Moderate"
    elif rounded_number >100 and rounded_number<150:
        bb="Moderate High"
    elif rounded_number>150 and rounded_number<200:
        bb="High"
    elif rounded_number>200 and rounded_number<300:
        bb="Very Unhealthy"
    elif rounded_number >300:
        bb="Hazardous"
        
    return render(request, "accounts/result.html",{"p1":rounded_number,"p2":bb})


