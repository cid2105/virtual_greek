from django.conf.urls.defaults import patterns, include, url
from views import *

urlpatterns = patterns('',
	url(r'^$', uni_index, name='uni_bulletin'),
	url(r'^(?P<org_name>[-\w]+)/', include('organization.urls')),

)
