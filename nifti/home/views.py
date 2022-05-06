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
    'description': 'I am interested in working in IT and related fields. See my <a href="https://www.linkedin.com/in/alex-palmer-686625238/" style="color: #d63384; text-decoration: none;"><code>LinkedIn</code></a>',
  },
  # Ameen El-Rasheedy
  {
    'first': 'Ameen',
    'middle': '',
    'last': 'El-Rasheedy',
    'description': 'I enjoy learning new things relating to software development and telecommunications. You can visit my <a href="https://www.linkedin.com/in/ameen-el-rasheedy-9965a6137/" style="color: #d63384; text-decoration: none;"><code>LinkedIn</code></a>.',
  },
  # Davina Robinson
  {
    'first': 'Davina',
    'middle': '',
    'last': 'Robinson',
    'description': 'I enjoy working with web design languages such as PHP C#, and HTML 5 and CSS. Here is my <a href="https://www.linkedin.com/mwlite/in/davina-robinson-b3455b189" style="color: #d63384; text-decoration: none;"><code>LinkedIn</code></a>.',
  },
  # Fernando Cruz
  {
    'first': 'Fernando',
    'middle': '',
    'last': 'Cruz',
    'description': 'I enjoy playing around with game design using Unity and hope to find employment as a game developer or a web developer. Check out my <a href="https://www.linkedin.com/in/fernando-cruz-32b02520a/" style="color: #d63384; text-decoration: none;"><code>LinkedIn</code></a> profile.',
  },
  # Luis David Licea Torres
  {
    'first': 'Luis',
    'middle': 'David',
    'last': 'Licea Torres',
    'description': 'I am a computer scientist. I am intersted in software and web development. Check out my personal website <code><a href="https://luisliceatorres.com" style="color: #d63384; text-decoration: none;">luisliceatorres.com</a></code> and my <a href="https://github.com/luis-licea/" style="color: #d63384; text-decoration: none;"><code>GitHub</code></a> account.'
  },
]

# Create your views here.
# Alex
def about(request):
  # show member info
  """ show member info"""
  context = {
    'members': members
  }
  return render(request, 'home/about.html', context)

# Luis
def login(request):
  """Handle user login."""
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

# Luis
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