from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Import the forms needed to update the user information and profile settings.
from home.forms import UserUpdateForm, ProfileUpdateForm

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
      # Redirect user to the profile settings page because we do anything else.
      return redirect('user-profile')

  else:
    # Create empty forms.
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

  context = {
    'u_form': u_form,
    'p_form': p_form,
  }
  return render(request, 'user/profile.html', context)