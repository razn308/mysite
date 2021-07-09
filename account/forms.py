from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from . models import Account
from django.shortcuts import render, redirect


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=30)

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2')
        exclude = []

class LoginForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')
        exclude = []

    
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid Details!')

class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('email', 'username')
        exclude = []

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                user = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" is already in use.' % email)

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                user = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError('Username "%s" is already in use.' % username)
