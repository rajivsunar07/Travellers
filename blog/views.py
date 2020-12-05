from django.shortcuts import render, redirect
from .models import Blog, Location
from users.models import Followers
from .forms import CreatePostForm, LocationForm

# Create your views here.

def blog(request):
    following = Followers.objects.filter(follower=request.user).values('following')
    posts = Blog.objects.filter()
    following_list = []
    post_list = []
    
    for i in following:
        following_list.append(i['following'])

    for post in posts:
        if post.author.id in following_list:
            post_list.append(post)

    context = {
        'post_list' : post_list
    }
    return render(request, 'blog/blog.html', context=context)

def create_blog(request):
    post_form = CreatePostForm()
    location_form = LocationForm()
    
    if request.method == 'POST':
        post_form = CreatePostForm(request.POST, request.FILES)
        location_form = LocationForm(request.POST)

        #check if the location is already entered
        address = Location.objects.filter(address=location_form.instance.address)
        if address.count() != 0:
            city = Location.objects.filter(city=location_form.instance.city)
            if city.count() != 0:
                country = Location.objects.filter(country=location_form.instance.country)
                if country.count() != 0:
                    location_form.save()
        
        post_form.instance.location = location_form.instance
        post_form.instance.author = request.user
        location_form.save()
        post_form.save()
        return redirect('blog')

    context = {
        'post_form': post_form,
        'location_form': location_form
    }

    return render(request, 'blog/create_blog.html', context=context)

