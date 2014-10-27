from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.base import View
from django.contrib.auth import logout as auth_logout
from whats.models import *
from whatsup.forms import *
from whatsup.settings import MEDIA_ROOT, STATIC_URL, ROOT_PATH, BASE_DIR
from os import remove, rename

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
			try:
				curruser.userimage = request.FILES['userimage']
				save_userimage(request.FILES['userimage'],curruser.loginid)
			except:
				if (curruser.userimage):
					pass
				else:
					curruser.userimage = 'userimg/default.jpg'
			curruser.save()
			return redirect('/home')

		try:
			curruser = usersinfo.objects.get(loginid = request.user.email)
			form = userinfo_form(initial = {'loginid':curruser.loginid, 'fname':curruser.fname, 'lname': curruser.lname, 'number':curruser.number})
			form.fields['loginid'].widget.attrs['readonly'] = True
			try:
				follow = follows.objects.get(uid = curruser.uid, fid = curruser.uid)
			except:
				newfollow = follows(uid = curruser.uid, fid = curruser.uid)
				newfollow.save()
			return render(request, 'update.html', {'form':form})
		except:
			newuser = usersinfo(loginid = request.user.email, role = 1, number = 0, status = 0)
			newuser.save()
			return redirect('/update')

	else:
		return render(request, 'index.html',{'str':'You must log in first'})

def save_userimage(file, userloginid ,path = 'userimg'):
	filename = file._get_name()

	fd = open('%s/%s/%s' % (MEDIA_ROOT, str(path),str(userloginid)), 'w')
	print MEDIA_ROOT+str(path)+str(userloginid)
	for chunk in file.chunks():
		fd.write(chunk)
	fd.close()

def home(request):
	if request.user.is_authenticated():
		try:
			curruser = usersinfo.objects.get(loginid = request.user.email)
		except:
			return redirect('/update')
		if curruser.status == 0:
			return redirect('/update')

		if request.method == "POST":
			form = post_form(request.POST, request.FILES)
			curruser = usersinfo.objects.get(loginid = request.user.email)
			newpost = posts(loginid = request.user.email, title = request.POST['posttitle'],posttext = request.POST['posttext'], uid = curruser.uid, fname = curruser.fname,lname = curruser.lname )
			try:
				newpost.postimage = request.FILES['postimage']
				save_postimage(request.FILES['postimage'])
			except:
				pass
			newpost.save()
		mastercomment = {}
		allpos = posts.objects.all()

		for i in allpos:
			mastercomment[i.pid] = comments.objects.filter(pid = i.pid)
		commentform = comment_form

		curruserposts = posts.objects.filter(uid = curruser.uid)
		count = len(curruserposts)		

		allfollowers = follows.objects.filter(fid = curruser.uid)	#all following curruser
		allfollowing = follows.objects.filter(uid = curruser.uid)	#all curruser is following

		followlist = []
		for follower in allfollowers:
			if follower.uid == curruser.uid:
				pass
			else:
				followlist.append(usersinfo.objects.get(uid = follower.uid))

		allfollow = follows.objects.filter(uid = curruser.uid)
		postbigarr = []
		allposts = []
		for following  in allfollow:
			for followpost in posts.objects.filter(uid = following.fid):
				allposts.append(followpost)
		allposts = allposts[::-1]

		votevalue = {}

		for post in allposts:
			try:
				vote = postvotes.objects.get(pid = post.pid,uid = curruser.uid)
				votevalue[post.pid] = vote.value
			except:
				votevalue[post.pid] = 0

		postform = post_form()
		commentform = comment_form
		print curruser.userimage.url
		return render(request, 'home.html', {'count':count,'votevalue':votevalue,'allfollowers':followlist,'allfollowing':allfollowing,'followingcount':len(allfollowing)-1,'followcount':len(allfollowers)-1,'mastercomment':mastercomment,'commentform':commentform,'postform':postform, 'curruser':curruser, 'allposts':allposts, 'path':MEDIA_ROOT})
	else:
		return render(request, 'index.html',{'str':'You must log in first'})


def save_postimage(file, path = 'postimg'):
	filename = file._get_name()
	fd = open('%s/%s/%s' % (MEDIA_ROOT, str(path),str(filename)), 'w')
	for chunk in file.chunks():
		fd.write(chunk)
	fd.close()

def discover(request):
	if request.user.is_authenticated():
		curruser = usersinfo.objects.get(loginid = request.user.email)
		if curruser.status == 0:
			return redirect('/update')
		currpost = posts.objects.filter(uid = curruser.uid)
		allposts = posts.objects.all()

		allposts = allposts[::-1]

		commentdict = {}
		votevalue = {}

		for post in allposts:
			try:
				vote = postvotes.objects.get(pid = post.pid)
				votevalue[post.pid] = vote.value
			except:
				votevalue[post.pid] = 0

		for post in allposts:
			commentdict[post.pid] = comments.objects.filter(pid = post.pid)

		commentform = comment_form
		return render(request, 'discover.html', {'allposts':allposts,'votevalue':votevalue,'curruser':curruser,'commentdict':commentdict,'count':len(currpost),'commentform':commentform})
		
	else:
		return redirect('/')

def follow(request,param):
	if request.user.is_authenticated():
		followuser = usersinfo.objects.get(loginid = param)
		curruser = usersinfo.objects.get(loginid = request.user.email)
		if curruser.status == 0:
			return redirect('/update')
		try:
			findfollow = follows.objects.get(uid= curruser.uid, fid = followuser.uid)
		except:
			newfollow = follows(uid= curruser.uid, fid = followuser.uid)
			newfollow.save()
		return redirect('/viewuser/'+str(param))
	else:
		return redirect('/')

def unfollow(request,param):
	if request.user.is_authenticated():
		followuser = usersinfo.objects.get(loginid = param)
		curruser = usersinfo.objects.get(loginid = request.user.email)
		if curruser.status == 0:
			return redirect('/update')
		try:
			findfollow = follows.objects.get(uid= curruser.uid, fid = followuser.uid)
			findfollow.delete()
		except:
			pass
		return redirect('/viewuser/'+str(param))
	else:
		return redirect('/')


def viewuser(request,param):
	if request.user.is_authenticated():
		curruser = usersinfo.objects.get(loginid = request.user.email)
		if curruser.status == 0:
			return redirect('/update')		
		if curruser.loginid == param:
			return redirect('/home')
		try:
			newuser = usersinfo.objects.get(loginid = param)
			allposts = posts.objects.filter(uid = newuser.uid)
			commentdict = {}

			for i in allposts:
				commentdict[i.pid] = comments.objects.filter(pid = i.pid)
			
			commentform = comment_form
			allposts = allposts[::-1]

			postform = post_form()
			commentform = comment_form
			followstatus = 0

			votevalue = {}

			for post in allposts:
				try:
					vote = postvotes.objects.get(pid = post.pid)
					votevalue[post.pid] = vote.value
				except:
					votevalue[post.pid] = 0

			try:
				findfollow = follows.objects.get(uid = curruser.uid, fid = newuser.uid)
				followstatus = 1
			except:
				followstatus = 0

			allfollowers = follows.objects.filter(fid = newuser.uid)
			allfollowing = follows.objects.filter(uid = newuser.uid)
			return render(request, 'viewuser.html',{'newuser':newuser,'votevalue':votevalue,'followingcount':len(allfollowing)-1,'followcount':len(allfollowers)-1,'followstatus':followstatus, 'commentform':commentform,'commentdict':commentdict,'allposts':allposts, 'count':len(allposts)})
		except:
			return render(request, 'usernotfound.html')
	else:
		return redirect('/')

def upvotepost(request,param):
	if request.user.is_authenticated():
		curruser = usersinfo.objects.get(loginid = request.user.email)
		currpost = posts.objects.get(pid = param)
		if curruser.status == 0:
			return redirect('/update')
		try:
			vote = postvotes.objects.get(uid = curruser.uid, pid = param)
			if vote.value == 1:
				vote.value = 0
				currpost.upcount-=1
			elif vote.value == -1:
				currpost.downcount -=1
				currpost.upcount +=1
				vote.value = 1
			elif vote.value == 0:
				currpost.upcount+=1
				vote.value = 1
			vote.save()
			currpost.save()
		except:
			vote = postvotes(uid = curruser.uid, pid = param, value = int(1))
			currpost.upcount +=1
			vote.save()
			currpost.save()
		return redirect('/viewpost/'+str(param))

	else:
		return redirect('/')

def downvotepost(request,param):
	if request.user.is_authenticated():
		curruser = usersinfo.objects.get(loginid = request.user.email)
		currpost = posts.objects.get(pid = param)
		if curruser.status == 0:
			return redirect('/update')
		try:
			vote = postvotes.objects.get(uid = curruser.uid, pid = param)
			if vote.value == 1:
				vote.value = -1
				currpost.downcount +=1
				currpost.upcount -=1
			elif vote.value == -1:
				vote.value = 0
				currpost.downcount-=1
			elif vote.value == 0:
				vote.value = -1
				currpost.downcount+=1
			vote.save()
			currpost.save()
		except:
			vote = postvotes(uid = curruser.uid, pid = param, value = int(-1))
			currpost.downcount +=1
			vote.save()
			currpost.save()
		return redirect('/viewpost/'+str(param))

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
			try:
				vote = postvotes.objects.get(pid = param, uid = curruser.uid)
				votevalue = vote.value
			except:
				votevalue = 0
			return render(request, 'viewpost.html', {'post':currpost,'votevalue':votevalue,'allcomments':allcomments,'postuser':postuser,'curruser':curruser, 'commentform':commentform})
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
			if(post.postimage):
				remove(MEDIA_ROOT+str(post.postimage.url)[6:])
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
	print "reached"
	if request.user.is_authenticated():
		curruser = usersinfo.objects.get(loginid = request.user.email)
		if curruser.status == 0:
			return redirect('/update')
		if request.method == "POST":
			print "newcom"
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
		votevalue = {}

		for post in allposts:
			try:
				vote = postvotes.objects.get(pid = post.pid)
				votevalue[post.pid] = vote.value
			except:
				votevalue[post.pid] = 0

		return render(request, 'myposts.html', {'count' : len(allposts),'votevalue':votevalue,'commentform':commentform,'curruser':curruser,'allposts':allposts,'mastercomment':mastercomment})

	else:
		return redirect('/')


