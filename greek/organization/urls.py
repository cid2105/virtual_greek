from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from models import Organization
from views import *

urlpatterns = patterns('',
	url(r'^$', index, name='uni_org_index'),
 	url(r'^home/$', home, name='uni_org_home'),
 	url(r'^albums/$', gallery, name='uni_org_gallery'),
	url(r'^albums/(?P<album_id>\d+)/', album, name='uni_org_album'),
 	url(r'^new/album/$', new_album, name='new_album'),
 	url(r'(?i)^brothers|sisters|members/$', members, name='uni_org_members'),
 	url(r'bulletin/$', bulletin, name='uni_org_bulletin'),
 	url(r'threads/$', threads, name='uni_org_threads'),
 	url(r'poll/$', threads, name='uni_org_threads'),
	url(r'^profile/(?P<user_id>\d+)/', profile, name='uni_org_profile'),
 	url(r'^new/topic-form/$', new_topic_form, name='new-topic-form'),
	url(r'^new/announcement/$', new_announcement, name='uni_org_new_announcement'),
	url(r'^new/topic/$', new_topic, name='new_topic'),
	url(r'^invite/$', invite, name='invite'),
	url(r'^chapter/$', chapter, name='uni_org_chapter'),
	url(r'^vote-reply/$', vote_reply, name='vote_reply'),
	url(r'^thread/(?P<topic_id>\d+)/$', topic, name='uni_org_topic'),
	url(r'^thread/(?P<topic_id>\d+)/delete-reply', delete_reply, name='uni_org_topic_delete_reply'),
)
