from django.shortcuts import *
from unis.models import *
from organization.models import *
from users.forms import RegistrationForm
from django.utils import simplejson
from datetime import *
from django.http import *
from django.contrib.auth.models import User
from django.core import serializers
from django.contrib.auth import *
from users.views import *

def uni_index(request, uni_name):
	uni = University.objects.get(name=uni_name)
	orgs = Organization.objects.filter(university=uni)
	return render_to_response('uni/index.html', {'orgs':orgs, 'title':uni_name}, context_instance=RequestContext(request))
	