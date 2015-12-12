from dfss.demo.models import UserProfile, Resume
from django.contrib.auth.models import User
from django import forms


class ResumeForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )

    class Meta:
        model = Resume
        fields = ('docfile')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
