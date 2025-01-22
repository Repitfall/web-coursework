from django import forms
from django.contrib.auth.models import User
from .models import Comment


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_repeat = forms.CharField(widget=forms.PasswordInput)

    def different_passwords(self):
        data = self.cleaned_data
        if data["password"] != data["password_repeat"]:
            raise forms.ValidationError("Пароли не совпадают!")
        return data["password"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["title", "text", "file"]
