from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.base import View
from django.contrib.auth import logout as auth_logout
from whats.models import *
from whatsup.forms import *

def index(request):
	if request.user.is_authenticated():
		try:
			curruser = usersinfo.objects.get(loginid = request.user.email)
			if curruser.status == 0:
				return redirect('/update')
			else:
				return redirect('/home')
		except:
			newuser = usersinfo(loginid = request.user.email, role = 1, number = 0, status = 0)
			newuser.save()
			return render(request, 'index.html')
	else:
		return render(request, 'index.html',{'str':'You must log in first'})

def logout(request):
	auth_logout(request)
	return HttpResponseRedirect('/')

def update(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = userinfo_form(request.POST)
			curruser = usersinfo.objects.get(loginid = request.user.email)
			curruser.loginid = request.POST['loginid']
			curruser.fname = request.POST['fname']
			curruser.lname = request.POST['lname']
			curruser.number = request.POST['number']
			curruser.status = 1
			curruser.save()
			return redirect('/home')
		else:
			curruser = usersinfo.objects.get(loginid = request.user.email)
			form = userinfo_form(initial = {'loginid':curruser.loginid, 'fname':curruser.fname, 'lname': curruser.lname, 'number':curruser.number})
			form.fields['loginid'].widget.attrs['readonly'] = True
			return render(request, 'update.html', {'form':form})
	else:
		return render(request, 'index.html',{'str':'You must log in first'})

def home(request):
	if request.user.is_authenticated():
		curruser = usersinfo.objects.get(loginid = request.user.email)
		if curruser.status == 0:
			return redirect('/update')
		else:
			return render(request, 'home.html')
	else:
		return render(request, 'index.html',{'str':'You must log in first'})
