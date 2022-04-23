from django.contrib.auth import forms, authenticate, login as auth_login
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm
from user import views as user_views
from axes.backends import AxesBackend

members = [
  # Alex Palmer.
  {
    'first': 'Alex',
    'middle': '',
    'last': 'Palmer',
    'description': 'Computer Science student',
  },
  # Ameen El-Rasheedy
  {
    'first': 'Ameen',
    'middle': '',
    'last': 'El-Rasheedy',
    'description': 'Computer Science student',
  },
  # Davina Robinson
  {
    'first': 'Davina',
    'middle': '',
    'last': 'Robinson',
    'description': 'Computer Science student',
  },
  # Fernando Cruz
  {
    'first': 'Fernando',
    'middle': '',
    'last': 'Cruz',
    'description': 'Computer Science student',
  },
  # Luis David Licea Torres
  {
    'first': 'Luis',
    'middle': 'David',
    'last': 'Licea Torres',
    'description': 'Computer Science student, GitHub account is <code>github.com/luis-licea/</code>',
  },
]

# Create your views here.
def about(request):
  context = {
    'members': members
  }
  return render(request, 'home/about.html', context)

def login(request):
  # Handle the POST request.
  if request.POST:
    # Get username and password.
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(
      # Important custom argument used by Django-Axes.
      request=request,
      username=username,
      password=password,
    )

    # Verify that user exists and is active.
    if user is not None and user.is_active:
      # Login the user.
      auth_login(request, user)
      # Redirect user to profile page.
      return redirect('user-profile')

  return render(request, 'home/login.html')

def register(request):
  if request.method == 'POST':
    # Create registration form.
    form = UserRegistrationForm(request.POST)
    # Validate form.
    if form.is_valid():
      # Create user from registration form.
      form.save()
      # Get username.
      username = form.cleaned_data.get('username')
      # Show message showing registration is successful.
      messages.success(request, f'Account created for {username}.')
      # Return user to search page.
      return redirect('home-login')
  else:
    form = UserRegistrationForm()

  context = {
    'form': form
  }
  return render(request, 'home/register.html', context)