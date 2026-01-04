from django.contrib.auth.forms import UserCreationForm

from django import forms

from .models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    role = forms.ChoiceField(
        choices=[
            (User.ROLE_USER, 'User'),
            (User.ROLE_AUTHOR, 'Author'),
        ],
        label="Change Role",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'bio', 'role')