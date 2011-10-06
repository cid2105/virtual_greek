from django.conf.urls.defaults import patterns, include, url
from views import *

urlpatterns = patterns('',
	url(r'^inbox/$', inbox, name='inbox'),
    url(r'^profile/$', profile, name='profile'),
	url(r'^bulletin/$', bulletin, name='bulletin'),
	url(r'^calendar/$', calendar, name='calendar'),
	url(r'^home/$', home, name='home'),
	url(r'^start/$', start, name='start'),
	url(r'^messages/(?P<conversation_id>\d+)/$', message, name='message'),
	url(r'^send-message/$', send_message, name='send_message'),
	url(r'^brother-validation/$', brother_validation, name='brother_validation'),
	url(r'^new-message/$', new_message, name='new_message'),
	url(r'^save-whiteboard/$', save_canvas, name='save_canvas'),
	url(r'^upload/resume/$', upload_resume, name='upload_resume'),
	url(r'^upload/profile-picture/$', upload_profile_picture, name='upload_profile_picture'),
)
