from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Install django-ckeditor first.
from ckeditor.fields import RichTextField

# Create your models here.
class Profile(models.Model):

    # Associates profile to a User, and deletes Profile if User is deleted.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The title of the profile.
    #TODO: add feature in frontend preventing users from registering their username 
    #with more than 100 chars
    title = models.CharField(max_length=100, default="User Profile")

    #TODO: add feature in frontend preventing entering more than 200 chars
    description = models.CharField(max_length=200, default='')

    # The HTML field containing the website contents.
    body = RichTextField(default='')

    # The date the profile was created.
    date_created = models.DateTimeField(default=timezone.now)

    profile_picture = models.ImageField(default="profile_pictures/default.jpg", upload_to="profile_pictures")
