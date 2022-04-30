from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Install django-ckeditor first.
from ckeditor.fields import RichTextField
from user.models import Profile
from django.urls import reverse

#Ameen
# Create your models here.
class Post(models.Model):
    # Associates a post to a profile
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    #TODO: add feature in frontend preventing entering more than 100 chars
    title = models.CharField(max_length=100,default='Post Title')

    # The HTML field containing the website contents.
    body = RichTextField(default='', blank=True)

    #TODO: add feature in frontend preventing entering more than 100 chars
    address = models.CharField(max_length=200,default='')

    #address gets converted to lat, long to use distance-based search.
    latitude = models.DecimalField(max_digits=30, decimal_places=10, default=0.0)
    longitude = models.DecimalField(max_digits=30, decimal_places=10, default=0.0)

    # The date the post was created.
    date_posted = models.DateTimeField(default=timezone.now)

    #default setting is Service Consumer
    service_provider = models.BooleanField(default=False)

    # Derive the post url from the key number.
    def get_absolute_url(self):
        # Return the full URL path to a post.
        return reverse('post-detail', kwargs={'pk': self.pk})

#Ameen
#TODO: make a function add_tags() whenever a user submits/creates a post (Use signals in signals.py)
class Tag(models.Model):
    #TODO: frontend feature preventing entering more than 20 chars per tag.
    tag_name = models.CharField(max_length=20)

#Ameen
#this class prevents duplicates in the Tag table
class TagToPostTable(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

