from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Install django-ckeditor first.
from ckeditor.fields import RichTextField
# Install Pillow first.
from PIL import Image

# Define the default profile picture name and directory once to reduce error
# proness.
default_image_name = 'default.png'
default_image_dir = 'profile_pictures/'
default_image = default_image_dir + default_image_name

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
    profile_picture = models.ImageField(default=default_image, upload_to=default_image_dir)

    # The original profile picture name is lost when updating the profile
    # picture. Keep track of the previous profile picture name so that it can be
    # deleted after it is orphaned.
    profile_picture_previous_name = models.CharField(max_length=256, default=default_image)

    # Modifies the profile picture to lower its resolution. We want to keep
    # profile pictures small in size.
    def save(self, *args, **kwargs):
        # TODO: Delete the previous image that was uploaded before saving a new
        # one.

        # print("Image name:", self.profile_picture.name)
        # print("Image path:", self.profile_picture.path)

        # Delete the orphaned profile picture.
        self.delete_profile_picture(default_image)

        # Save the new profile picture.
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

    def delete_profile_picture(self, default_image):
        # Delete the profile picture if it is not the default picture.
        if self.profile_picture_previous_name != default_image:
            print("Deleteing", self.profile_picture_previous_name)

            # Get storage access.
            storage = self.profile_picture.storage

            # Delete the the profile picture.
            storage.delete(name=self.profile_picture_previous_name)
        else:
            print(f'The image {default_image} cannot be deleted. It may be used by other users.')

        # Keep track of the profile image name. This name will be used to delete
        # the image after it is orphaned.
        self.profile_picture_previous_name = self.profile_picture.name

    def __str__(self):
        return f'{self.user.username} Profile'