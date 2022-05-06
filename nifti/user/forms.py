from django import forms
from django.contrib.auth.models import User

# Alex
class UserDeleteForm(forms.ModelForm):
    """The form deletes the user that is logged in."""
    class Meta:
        model = User
        fields = []   #Form has only submit button.  Empty "fields" list still necessary, though.