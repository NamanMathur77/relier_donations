from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import hashlib
import time
import pickle


def loadall(filename):
    with open(filename,'rb') as input:
        return pickle.load(input)


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username} !!!')
            print({username})
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request,'user/register.html', {'form':form})

@login_required
def profile(request):
    if request.method=='POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save() 
            messages.success(request, f'Your Profile is updated')
            return redirect('profile')
    else:
        blockchain = loadall('blck.pkl')
        denyblockchain = loadall('denyblck.pkl')
        count=0
        red=0
        for block in blockchain.chain:
            dt=block.data
            for i in dt:
                if(type(i['sender'])==str and i['sender']==request.user.username):
                    count+=1
        for block in denyblockchain.chain:
            dt=block.data
            for i in dt:
                if(type(i['sender'])==str and i['sender']==request.user.username):
                    red+=1
        count=count-red
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'blockchain':blockchain,
        'denyblockchain':denyblockchain,
        'count':count
    }
    return render(request, 'user/profile.html',context)
