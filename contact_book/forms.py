from django import forms
from .models import Email
from django.contrib.auth.models import User


class EmailCreateForm(forms.ModelForm):
    """ Email creation form """

    class Meta:
        model = Email
        fields = ['email']
