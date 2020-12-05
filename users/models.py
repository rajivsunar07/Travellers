from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class Followers(models.Model):
    follower = models.OneToOneField(User, on_delete=models.CASCADE, related_name='follower')
    following = models.OneToOneField(User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        db_table = "Followers"



class Profile(models.Model):
    ''' For additional infomation of the user '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    class Meta:
        db_table = "Profile"

# Signal to create a profile object whenever a user object is created
def create_profile(sender, **kwargs):
    if kwargs['created']:
        profile = Profile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)