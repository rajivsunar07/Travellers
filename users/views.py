from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import auth, User
from .models import Followers
from blog.models import Blog
from .forms import ProfileUpdateForm, UserUpdateForm

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

def profile_update(request):
    profile_form = ProfileUpdateForm(instance=request.user.profile)
    user_form = UserUpdateForm(instance=request.user)

    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.instance.user = user_form.instance
            profile_form.save()
            return redirect('profile', request.user.username)
        
    context={
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'users/user_update.html', context)