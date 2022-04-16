from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Import the forms needed to update the user information and profile settings.
from home.forms import UserUpdateForm, ProfileUpdateForm
from .forms import UserDeleteForm
from django.contrib.auth.models import User
from django.views.generic import ListView
from search.models import Post

# Create your views here.

@login_required
def profile(request):
  # Use capital letters for POST, otherwise update user settings will not work.
  if request.method == 'POST':
    # Pass the existing user information through 'request.POST'.
    # Associate the form user to the current instance, so that we update the
    # existing user rathern than create a new one.
    u_form = UserUpdateForm(request.POST, instance=request.user)

    # Pass the existing form information through 'request.POST'.
    # Pass the existing profile picture information through 'request.FILES'.
    # Associate the form profile to the current instance, so that we update the
    # existing profile rathern than create a new one.
    p_form = ProfileUpdateForm(request.POST, request.FILES,
      instance=request.user.profile)

    # Validtate the forms.
    if u_form.is_valid() and p_form.is_valid():
      u_form.save()
      p_form.save()

      # Show a success message after saving the forms.
      messages.success(request, f'Your profile has been updated!')
      # Redirect user to the profile page after saving the changes.
      return redirect('user-static-profile', request.user )

  else:
    # Create empty forms.
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

  context = {
    'u_form': u_form,
    'p_form': p_form,
  }
  return render(request, 'user/profile.html', context)

@login_required
def deleteuser(request):
    if request.method == 'POST':
        delete_form = UserDeleteForm(request.POST, instance=request.user)
        user = request.user
        user.delete()
        messages.info(request, 'Your account has been deleted.')
        return redirect('home-home')
    else:
        delete_form = UserDeleteForm(instance=request.user)

    context = {
        'delete_form': delete_form
    }

    return render(request, 'user/delete_account.html', context)

def profile_detail(request, username):
    """Display user profile when clicked. All contents are static and cannot be
    modified.
    """

    # Get the user whose username matches the url parameter.
    user = User.objects.get(username=username)
    context = {
      'other_user': user,
    }
    return render(request, 'user/profile_static.html', context)

class PostListView(ListView):
  model = Post
  template_name = 'search/posts_by_user.html'
  context_object_name = 'posts'

  # Get oldest posts first.
  ordering = ['-date_posted']

  # Get newest posts first.
  # ordering = ['date_posted']

  def get_queryset(self):
    # Get the username from the URL, as defined in urls.py.
    username = self.kwargs['username']

    # Get the user with the matching username.
    user = User.objects.get(username=username)

    # Return posts created by the user.
    return Post.objects.filter(author=user)

    # print(self.request.GET)
    # query = self.request.GET.get('q')
    # return Post.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
