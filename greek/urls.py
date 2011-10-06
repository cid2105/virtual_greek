from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView
from django.conf import settings
from organization.models import *
from unis.models import *
from users.views import * 
from users.models import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/media/images/favicon.ico'}),
	url(r'^admin/doc/$', include('django.contrib.admindocs.urls')),
	
)


urlpatterns += patterns('',
    # Examples:	
	url(r'', include('social_auth.urls')),
	(r'^facebook/', include('django_facebook.urls')),
	url(r'^register/$', ajax_register, name='ajax_register'),
	(r'^accounts/register/$', 'views.register', {}, 'register'),
	url(r'^accounts/login/$', auth_login, name='login'),
	url(r'^accounts/logout/$', auth_logout, name='logout'),
	url(r'^', include('users.urls')),
#	url(r'^asdfasdf/asdfasdf/galleria/', include('photologue.urls')),
	(r'^(?P<uni_name>\w+)/', include('unis.urls')),
	url(r'^$', index, name='index'),
	



)

urlpatterns += staticfiles_urlpatterns()



INTERNAL_IPS = ('127.0.0.1',)
