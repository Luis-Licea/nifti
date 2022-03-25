from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Install django-ckeditor first.
from ckeditor.fields import RichTextField

# Create your models here.
class Profile(models.Model):

    # The title of the profile.
    title = models.CharField(max_length=100)

    # The HTML field containing the website contents.
    body = RichTextField(blank=True, null=True)

    # The date the profile was created.
    date_posted = models.DateTimeField(default=timezone.now)

    # Associates profile to a User, and deletes Profile if User is deleted.
    author = models.ForeignKey(User, on_delete=models.CASCADE)