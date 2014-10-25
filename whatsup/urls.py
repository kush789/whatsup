from django.conf.urls import patterns, include, url
from views import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'whatsup.views.home', name='home'),
    # url(r'^whatsup/', include('whatsup.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    #for my post images

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),



    #genral

	url(r'^$', index, name='home'), #index page
	url('', include('social.apps.django_app.urls', namespace='social')),
	url(r'^logout$', logout),

    #user specific

    url(r'^update$', update),
    url(r'^myposts$', myposts),
    url(r'^home', home),
    url(r'^discover', discover),


    #public urls

    url(r'^viewpost/(?P<param>.+)', viewpost),
    url(r'^upvotepost/(?P<param>.+)', upvotepost),
    url(r'^downvotepost/(?P<param>.+)', downvotepost),
    url(r'^viewuser/(?P<param>.+)', viewuser),
    url(r'^deletepost/(?P<param>.+)', deletepost),
    url(r'^deletecomment/(?P<param>.+)', deletecomment),
    url(r'^addcomment/(?P<param>.+)', addcomment),
    url(r'^follow/(?P<param>.+)', follow),
    url(r'^unfollow/(?P<param>.+)', unfollow),

)
