from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.base import View
from django.contrib.auth import logout as auth_logout
from whats.models import *
from whatsup.forms import *
from whatsup.settings import MEDIA_ROOT, STATIC_URL, ROOT_PATH, BASE_DIR

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
		try:
			curruser = usersinfo.objects.get(loginid = request.user.email)
			form = userinfo_form(initial = {'loginid':curruser.loginid, 'fname':curruser.fname, 'lname': curruser.lname, 'number':curruser.number})
			form.fields['loginid'].widget.attrs['readonly'] = True
			return render(request, 'update.html', {'form':form})
		except:
			newuser = usersinfo(loginid = request.user.email, role = 1, number = 0, status = 0)
			newuser.save()
			return redirect('/update')

	else:
		return render(request, 'index.html',{'str':'You must log in first'})

def home(request):
	if request.user.is_authenticated():
		curruser = usersinfo.objects.get(loginid = request.user.email)

		if curruser.status == 0:
			return redirect('/update')

		if request.method == "POST":
			form = post_form(request.POST, request.FILES)
			curruser = usersinfo.objects.get(loginid = request.user.email)
			newpost = posts(loginid = request.user.email, title = request.POST['posttitle'],posttext = request.POST['posttext'], uid = curruser.uid, fname = curruser.fname,lname = curruser.lname )
			try:
				newpost.postimage = request.FILES['postimage']
				save_image(request.FILES['postimage'])
			except:
				pass
			newpost.save()
		mastercomment = {}
		allposts = posts.objects.all()

		for i in allposts:
			mastercomment[i.pid] = comments.objects.filter(pid = i.pid)
		commentform = comment_form

		curruserposts = posts.objects.filter(uid = curruser.uid)
		count = len(curruserposts)
		allposts = posts.objects.all()
		allposts = allposts[::-1]
		postform = post_form()
		return render(request, 'home.html', {'count':count,'mastercomment':mastercomment,'postform':postform, 'user':curruser, 'allposts':allposts, 'path':MEDIA_ROOT})
	else:
		return render(request, 'index.html',{'str':'You must log in first'})


def save_image(file, path = ''):
	filename = file._get_name()
	fd = open('%s/%s' % (MEDIA_ROOT, str(path)+str(filename)), 'w')
	for chunk in file.chunks():
		fd.write(chunk)
	fd.close()

def viewuser(request,param):
	if request.user.is_authenticated():
		curruser = usersinfo.objects.get(loginid = request.user.email)
		if curruser.status == 0:
			return redirect('/update')		
		try:
			newuser = usersinfo.objects.get(fname = param)
			allposts = posts.objects.filter(uid = newuser.uid)
			return render(request, 'viewuser.html',{'newuser':newuser, 'allposts':allposts, 'count':len(allposts)})
		except:
			return render(request, 'usernotfound.html')
	else:
		return redirect('/')

def viewpost(request,param):
	if request.user.is_authenticated():
		curruser = usersinfo.objects.get(loginid = request.user.email)
		if curruser.status == 0:
			return redirect('/update')

		try:
			currpost = posts.objects.get(pid = param)
			postuser = usersinfo.objects.get(uid = currpost.uid)
			if request.method == "POST":
				newcomment = comments(uid = curruser.uid, pid = param, fname = curruser.fname, lname = curruser.lname, loginid = curruser.loginid, commenttext = request.POST['commenttext'], upcount = 0, downcount = 0)
				newcomment.save()
			allcomments = comments.objects.filter(pid = param)
			commentform = comment_form

			return render(request, 'viewpost.html', {'post':currpost,'allcomments':allcomments,'postuser':postuser,'curruser':curruser, 'commentform':commentform})
		except:
			return render(request, 'postnotfound.html')
	else:
		return redirect('/')

def deletepost(request,param):
	if request.user.is_authenticated():
		curruser = usersinfo.objects.get(loginid = request.user.email)
		if curruser.status == 0:
			return redirect('/update')
		post = posts.objects.get(pid = param)
		if post.uid == curruser.uid:
			post.delete()
		return redirect('/myposts')
	else:
		return redirect('/')

def deletecomment(request,param):
	if request.user.is_authenticated():
		curruser = usersinfo.objects.get(loginid = request.user.email)
		if curruser.status == 0:
			return redirect('/update')		
		comment = comments.objects.get(cid = param)
		postid = comment.pid
		comment.delete()
		return redirect('/viewpost/'+str(postid))
	else:
		return redirect('/')


def addcomment(request,param):
	if request.user.is_authenticated():
		curruser = usersinfo.objects.get(loginid = request.user.email)
		if curruser.status == 0:
			return redirect('/update')
		if request.method == "POST":
			newcomment = comments(uid = curruser.uid, pid = param, fname = curruser.fname, lname = curruser.lname, loginid = curruser.loginid, commenttext = request.POST['commenttext'], upcount = 0, downcount = 0)
			newcomment.save()
		return redirect('/viewpost/'+str(param))

	else:
		return redirect('/')


def myposts(request):
	if request.user.is_authenticated():
		curruser = usersinfo.objects.get(loginid = request.user.email)
		if curruser.status == 0:
			return redirect('/update')
		allposts = posts.objects.filter(uid = curruser.uid)
		allposts = allposts[::-1]
		mastercomment = {}
		for i in allposts:
			mastercomment[i.pid] = comments.objects.filter(pid = i.pid)
		commentform = comment_form

		return render(request, 'myposts.html', {'count' : len(allposts),'commentform':commentform,'curruser':curruser,'allposts':allposts,'mastercomment':mastercomment})

	else:
		return redirect('/')
