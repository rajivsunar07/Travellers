from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import auth, User
from .models import Followers
from blog.models import Blog

# Create your views here.

def signup(request):
    if request.method == 'POST':
        username = request.POST['user-name']
        email = request.POST['email-address']
        password = request.POST['password-signup']
        password1 = request.POST['password1-signup']

        if password == password1:
            users = User.objects.filter(username=username)
            emails = User.objects.filter(email=email)
            if len(users)==0 and len(emails)==0:
                User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, 'Account was created')
                return redirect('login')
            

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('profile', username)
        else:
            messages.info(request, 'Login failed')
    return render(request, 'users/login.html')


def profile(request, username):
    current_profile = User.objects.get(username=username)
    followers = Followers.objects.filter(following=current_profile)
    following = Followers.objects.filter(follower=current_profile)
    posts = Blog.objects.filter(author=current_profile)

    currently_following = False
    for i in followers:
        if i.follower == request.user:
            currently_following = True
            break
       
    if request.method == "POST":
        if 'unfollow' in request.POST:
            Followers.objects.get(follower=request.user, following=current_profile).delete()
            return redirect('profile', current_profile)
        else:
            Followers.objects.create(follower=request.user, following=current_profile)
            return redirect('profile', current_profile)
    context = {
        'current_profile':current_profile,
        'followers': followers,
        'following': following,
        'currently_following': currently_following,
        'posts': posts
    }
    return render(request, 'users/profile.html', context)
