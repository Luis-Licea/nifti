from django import forms
from django.contrib.auth.models import User


class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []   #Form has only submit button.  Empty "fields" list still necessary, though.