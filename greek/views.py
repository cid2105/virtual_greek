from django.shortcuts import *
from unis.models import *
from organization.models import *
from organization.views import *
from users.forms import RegistrationForm
from django.utils import simplejson
from datetime import *
from django.http import *
from django.contrib.auth.models import User
from django.core import serializers
from django.contrib.auth import *
from users.views import *
from django.template.defaultfilters import slugify

STATIC_URL = '/media/'

def index(request):
	if request.user.is_authenticated():
		topics = Topic.objects.filter(organization=request.user.get_profile().organization, university=request.user.get_profile().university, members = request.user)
		if topics:
			dict = getPagedTopics(request, topics)
		else:
			dict = getDict(request, request.user.get_profile().university.name, slugify(request.user.get_profile().organization.name))
		dict.update({'title':home})
		return render_to_response('users/index.html', dict, context_instance=RequestContext(request))
	return render_to_response('home/index.html', {}, context_instance=RequestContext(request))

def auth_login(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	active = True
	template = 'home/index.html'
	error = False
	if user is not None:	
		if user.is_active:
			login(request, user)
			template = 'users/index.html'
			return HttpResponseRedirect("/")
		else:			
   			active = False
	else:
		error = True
	return render_to_response(template, {'active':active, 'error': error}, context_instance=RequestContext(request))
	
def auth_logout(request):
	logout(request)
	return redirect('index')
	
	
def ajax_register(request):
	return render_to_response('home/register.html', {}, context_instance=RequestContext(request))
	
def default_context(request):
	if hasattr(request, 'user'):
		return {'user':request.user, 'STATIC_URL': STATIC_URL, 'MEDIA_URL': STATIC_URL }
	return {'STATIC_URL': STATIC_URL, 'MEDIA_URL': STATIC_URL}
	
def register(request):	
	if request.is_ajax():
		if request.POST['fratname'] and request.POST['university'] and request.POST['email'] and request.POST['type']:
			try:
				uni = University.objects.get(name=str(request.POST['university']))
			except University.DoesNotExist:
				uni = University(name=str(request.POST['university']), date = datetime.now())
			uni.save()
			form = RegistrationForm(request.POST)
			clean = form.is_valid()
			# Make some dicts to get passed back to the browser
			rdict = {'bad':'false'}
			errors = ""
			if not clean:
				rdict.update({'bad':'true'})
				for e in form.errors.iteritems():
					errors += str(e[1])
			else:
				date = datetime.now()
				org = Organization(university = uni, name=request.POST['fratname'], date = date, type=request.POST['type'])
				org.save()
				user = User.objects.create_user(request.POST['email'], request.POST['email'], date.isoformat())
				user.save()	
				user.get_profile().organization = org
				user.get_profile().university = uni
				user.get_profile().ip = request.META['REMOTE_ADDR']
				user.get_profile().save
			json = simplejson.dumps(rdict)
			return HttpResponse(errors)
		return HttpResponse("fail")

