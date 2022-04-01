from django.contrib.auth import forms, authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm

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
def home(request):
  return render(request, 'home/home.html')

def about(request):
  context = {
    'members': members
  }
  return render(request, 'home/about.html', context)

def login(request):
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