from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, AbstractBaseUser
from django.db.models import UniqueConstraint
from .models import *

class NewUserForm(UserCreationForm):

	first_name = forms.CharField(required = True)
	last_name = forms.CharField(required = True)
	email = forms.EmailField(required = True)

	class Meta:
		model = User
		fields = ("username", "first_name", "last_name", "email", "password1", "password2")
		unique_together = ('email',)

		def save(self, commit = True):
			user = super(NewUserForm, self).save(commit = False)
			user.email = self.cleaned_data.get('email')
			if User.objects.filter(email = user.email).exists():
				raise forms.ValidationError(u'Account with that email already exists')
			user.first_name = self.cleaned_data.get('first_name')
			user.last_name = self.cleaned_data.get('last_name')
			if commit:
				user.save()
			return user
