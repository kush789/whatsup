from django import forms

from django.forms.widgets import *
from whats.models import *


class userinfo_form(forms.ModelForm):
	loginid = forms.CharField(required = True, widget = forms.TextInput)
	fname = forms.CharField(required = True, widget = forms.TextInput)
	lname = forms.CharField(required = True, widget = forms.TextInput)
	number = forms.IntegerField(required = True, widget = forms.TextInput)

	class Meta:
		model = usersinfo
		fields = ('loginid','fname','lname','number')
