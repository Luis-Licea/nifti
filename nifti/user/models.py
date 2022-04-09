from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Install django-ckeditor first.
from ckeditor.fields import RichTextField
# Install Pillow first.
from PIL import Image

# Create your models here.
class Profile(models.Model):

    # Associates profile to a User, and deletes Profile if User is deleted.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The title of the profile. The title may be used for search.
    #TODO: add feature in frontend preventing users from registering their username 
    #with more than 100 chars
    title = models.CharField(max_length=100, default="User Profile")

    # The HTML field containing the website contents.
    body = RichTextField(default='', blank=True)

    # The date the profile was created.
    date_created = models.DateTimeField(default=timezone.now)

    # The profile picture will be used on the profile and posts.
    profile_picture = models.ImageField(default="profile_pictures/default.jpg", upload_to="profile_pictures")

    # Modifies the profile picture to lower its resolution. We want to keep
    # profile pictures small in size.
    def save(self, *args, **kwargs):
        # TODO: Delete the previous image that was uploaded before saving a new
        # one.
        super().save(*args, **kwargs)

        # Get the profile picture.
        img = Image.open(self.profile_picture.path)

        # The max height and width of the profile picture.
        max_size = 400

        # Check that the profile picture is not too large.
        if img.height > max_size or img.width > max_size:
            # Specify the desired width and height.
            output_size = (max_size, max_size)
            # Resize the picture.
            img.thumbnail(output_size)
            # Save the resized picture.
            img.save(self.profile_picture.path)

    def __str__(self):
        return f'{self.user.username} Profile'