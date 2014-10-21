from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.base import View
from django.contrib.auth import logout as auth_logout
from whats.models import *

def index(request):
	if request.user.is_authenticated():
		try:
			curruser = userinfo.objects.get(loginid = request.user.email)
			return render(request, 'home.html', {'email':curruser.loginid})
		except:
			newuser = userinfo(loginid = request.user.email, role = 1, number = 0)
			newuser.save()
			return render(request, 'ind.html')
	else:
		return render(request, 'index.html',{'str':'You must log in first'})

def logout(request):
	auth_logout(request)
	return HttpResponseRedirect('/')