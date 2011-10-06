from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from organization.urls import *
from organization.views import *

class FakeUploadCookieMiddleware(object):
	def process_request(self, request):
		if (request.method == 'POST') and (request.path == reverse('uni_org_gallery', args=[request.user.get_profile().university.name, slugify(request.user.get_profile().organization.name)])) and request.POST.has_key(settings.SESSION_COOKIE_NAME):
			request.COOKIES[settings.SESSION_COOKIE_NAME] = request.POST[settings.SESSION_COOKIE_NAME]