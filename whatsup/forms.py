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


class post_form(forms.ModelForm):
	posttitle = forms.CharField(max_length = 50, label = 'Title',widget = forms.TextInput)
	posttext = forms.CharField(max_length = 300, label = 'Body', widget = forms.TextInput)
	postimage = forms.FileField(required = False, label = 'Upload Image')

	class Meta:
		model = posts
		fields = ('posttitle','posttext', 'postimage')

class comment_form(forms.ModelForm):
	commenttext = forms.CharField(max_length = 300, label = ' ', widget = forms.TextInput)

	class Meta:
		model = comments
		fields = ('commenttext',)
