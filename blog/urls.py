from django.urls import path
from .views import *

urlpatterns = [
    path('', blog, name='blog'),
    path('create-blog/', create_blog, name='create_blog')
]
