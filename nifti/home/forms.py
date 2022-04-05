from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.fields import EmailField
from django.forms.forms import Form
from user.models import Profile
from ckeditor.fields import RichTextField

class UserRegistrationForm(UserCreationForm):
    """Create user registration form.

    Args:
        UserCreationForm: Inherit from UserCreationForm to create custom form.

    Raises:
        ValidationError
    """

    username = forms.CharField(
        label='Username',
        min_length=4,
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'class': 'form-control',
                }
        )
    )

    email = forms.CharField(
        label='Email',
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email',
                'class': 'form-control',
                }
        )
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-control',
                }
        )
    )

    password2 = forms.CharField(
        label='Password Verification',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password Verification',
                'class': 'form-control',
                }
        )
    )

    def username_clean(self):
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username=username)
        if new.count():
            raise ValidationError("User already exists.")
        return username

    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError("Email already exists.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user

class UserUpdateForm(forms.ModelForm):
    """Allow users to change their username and email. """

    # This is an unstyled email component. Do not use it. It looks ugly.
    # email = forms.EmailField()

    # The form should contain an email field.
    # The 'class' attribute uses Bootstrap to style the component.
    email = forms.CharField(
        label='Email',
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email',
                'class': 'form-control',
                }
        )
    )

    # The form should contain an username field.
    # The 'class' attribute uses Bootstrap to style the component.
    username = forms.CharField(
        label='Username',
        min_length=4,
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'class': 'form-control',
                }
        )
    )

    class Meta:
        # The form should only modify the User model.
        model = User
        # The form should only modify the following fields of the model.
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    """Allow users to change their profile title, body, and profile picture.
    """

    # The form should contain the title field.
    # The 'class' attribute uses Bootstrap to style the component.
    title = forms.CharField(
        label='Title',
        min_length=1,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Title',
                'class': 'form-control',
                }
        )
    )

    # The HTML field containing the website contents.
    body = RichTextField()

    class Meta:
        # The form should only modify the Profile model.
        model = Profile
        # The form should only modify the following fields of the model.
        fields = ['title', 'body', 'profile_picture']