from django import forms
from django.forms import ModelForm
from .models import Blog, Location

class CreatePostForm(ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
        exclude = ['date_posted','author', 'location']

        widgets = {
            'image': forms.FileInput(),
            'content': forms.Textarea(attrs={'class':'form-control'}),
        }

class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = '__all__'


