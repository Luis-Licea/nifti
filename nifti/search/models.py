from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Install django-ckeditor first.
from ckeditor.fields import RichTextField
from user.models import Profile

# Create your models here.
class Post(models.Model):
    # Associates a post to a profile
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # The title of the post
    #TODO: add feature in frontend preventing entering more than 100 chars
    title = models.CharField(max_length=100)

    # The HTML field containing the website contents.
    body = RichTextField(blank=True, null=True)

    # The date the post was created.
    date_posted = models.DateTimeField(default=timezone.now)

    #default setting is Service Consumer
    service_provider = models.BooleanField(default=False)


#TODO: make a function add_tag() whenever a user submits/creates a post
'''
if(tag exist in Tag Table):
    create new entry in TagToPostTable
else:
    create new entry in Tag with the actual tag name
    create new entry in TagToPostTable 
'''
#holds the tag names, works with the TagToPostTable
class Tag(models.Model):
    post = models.OneToOneField(Profile, on_delete=models.CASCADE)
    
    #TODO: frontend feature preventing entering more than 20 chars per tag.
    tag_name = models.CharField(max_length=20)

#this class prevents duplicates in the Tag table
class TagToPostTable(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
