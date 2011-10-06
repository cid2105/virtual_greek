
from django.shortcuts import *
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from organization.models import *
from organization.views import *
from users.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaultfilters import slugify
import re
import os
PAGE_SIZE = 5

@csrf_exempt
def profile(request):
	if request.is_ajax():
		return HttpResponse(updateProfile(request))
	return profile_base(request)

@csrf_exempt
def send_message(request):
	if request.is_ajax():
		if 'to' and 'message' in request.POST:
			recipient = User.objects.get(id=request.POST['to'])
			content = request.POST['message']
			message = Message(author=request.user, recipient=recipient, content=content)
			message.save()	
			try:
				conversation1 = request.user.get_profile().conversations.get(partner = recipient)
				conversation1.messages.add(message)
				conversation1.save()
				conversation2 = recipient.get_profile().conversations.get(partner = request.user)
				conversation2.messages.add(message)
				conversation2.save()
			except Conversation.DoesNotExist:
			   	conversation1 = Conversation(partner=recipient)
				conversation1.save()
				conversation1.messages.add(message)
				conversation2 = Conversation(partner=request.user)
				conversation2.save()
				conversation2.messages.add(message)
				request.user.get_profile().conversations.add(conversation1)
				recipient.get_profile().conversations.add(conversation2)
			request.user.get_profile().save()
			recipient.get_profile().save()
			return HttpResponse('success')
	return HttpResponse('failure')
	
def profile_base(request):
	profile = request.user.get_profile()
	dict = getDict(request, profile.university.name, slugify(profile.organization.name))
	dict.update({'title':'profile', 'curr_year':datetime.now().year, 'step':10 })
	return render_to_response('users/profile.html',dict, context_instance=RequestContext(request))
	
def upload_resume(request):
	if 'resume' in request.FILES:
		file = request.FILES['resume']
		extension_array = file.name.split(".")
		extension = "." + extension_array[len(extension_array)-1]
		file.name = 'resume_' + str(request.user.id) +  extension
		if request.user.get_profile().resume:
			request.user.get_profile().resume.delete()
		request.user.get_profile().resume = file
	request.user.get_profile().save()
	return profile_base(request)
	
def upload_profile_picture(request):
	if 'profile_picture' in request.FILES:
		if request.user.get_profile().profile_picture:
			request.user.get_profile().profile_picture.delete()
		request.user.get_profile().profile_picture = request.FILES['profile_picture']
		request.user.get_profile().save()
		return profile_base(request)
	profile = request.user.get_profile()
	dict = getDict(request, profile.university.name, slugify(profile.organization.name))
	dict.update({'title':'profile', 'curr_year':datetime.now().year, 'step':10 })
	return render_to_response('users/upload_picture.html',dict, context_instance=RequestContext(request))

def brother_validation(request):
	if 'to' in request.GET:
		try:
			member = request.user.get_profile().organization.members.get(userprofile__facebook_name__icontains=request.GET['to'])
			return HttpResponse(member.id)
		except User.DoesNotExist:
		   	return HttpResponse("failure")
					
def updatePosition(request):
	if 'position' and 'type' and 'value' in request.POST:
		position = Position.objects.get(id=request.POST['position'])
		if request.POST['type'] == 'position_title':
			position.title = request.POST['value']
		else:
			position.company = request.POST['value']
		position.save()
	return
		
def updateProfile(request):
	if 'position' or 'description' or 'major' or 'display_name' or 'phone_number' or 'graduate_year' or 'matriculate_year' in request.POST:
		if 'display_name' in request.POST:
			request.user.get_profile().facebook_name = request.POST['display_name']
		if 'phone_number' in request.POST:
			non_numeric = re.compile(r'[^\d]+')
			number = non_numeric.sub('', request.POST['phone_number'])
			request.user.get_profile().phone_number = number
		if 'description' in request.POST:
			request.user.get_profile().description = request.POST['description']
		if 'major' in request.POST:
			request.user.get_profile().major = request.POST['major']
		if 'position' in request.POST:
			updatePosition(request)
		if 'graduate_year' in request.POST:
			request.user.get_profile().linkedin.graduate_year = request.POST['graduate_year']
			request.user.get_profile().linkedin.save()
		if 'matriculate_year' in request.POST:
			request.user.get_profile().linkedin.matriculate_year = request.POST['matriculate_year']
			request.user.get_profile().linkedin.save()
		request.user.get_profile().save()
		return "success"
	else:
		return "failure"

def getPagedTopics(request, topics):
	uni = request.user.get_profile().university
	org = request.user.get_profile().organization
	base_url = reverse('uni_org_index', args=[uni.name, slugify(org.name)])
	paginator = Paginator(topics, PAGE_SIZE)
	page = request.GET.get('page')	
	try:
		topics = paginator.page(page)
	except PageNotAnInteger:
		topics = paginator.page(1)
	except EmptyPage:
		topics = paginator.page(paginator.num_pages)
	dict = {'base_url':base_url, 'uni_name':uni.name, 'page':page,'title': 'home', 'topics':topics, 'uni':uni, 'org':org, 'hash_tags':getHashes()}
	if len(Announcement.objects.filter(university = uni, organization=org)) > 0:
		dict = paginateCollection(request, dict, Announcement.objects.filter(university = uni, organization=org), 'announcements')
	dict = paginateCollection(request, dict, announcements, 'announcements')
	return dict


def message(request, conversation_id):
	conversation = get_object_or_404(Conversation, pk=conversation_id)
	messages = conversation.messages.all().order_by('-date')
	profile = request.user.get_profile()
	dict = getDict(request, profile.university.name, slugify(profile.organization.name))
	if 'message' in request.POST:
		message = Message(author = request.user, content=request.POST['message'], recipient=conversation.partner)
		message.save()
		conversation.messages.add(message)
		conversation.partner.get_profile().conversations.get(partner=request.user).messages.add(message)
		dict.update({'new_message':True})	
	dict.update({'title':'inbox', 'conversation':conversation})
	dict = paginateCollection(request, dict, messages, "messages")	
	return render_to_response('users/message.html', dict, context_instance=RequestContext(request))
	
def getPagedConversations(request, conversations):
	uni = request.user.get_profile().university
	org = request.user.get_profile().organization
	base_url = reverse('uni_org_index', args=[uni.name, slugify(org.name)])
	paginator = Paginator(conversations, PAGE_SIZE)
	page = request.GET.get('page')	
	announcements = Announcement.objects.filter(university = uni, organization=org)[:4]	
	try:
	 	conversations = paginator.page(page)
	except PageNotAnInteger:
		conversations = paginator.page(1)
	except EmptyPage:
		conversations = paginator.page(paginator.num_pages)
	return {'base_url':base_url, 'uni_name':uni.name, 'page':page, 'title': 'inbox', 'conversations':conversations, 'uni':uni, 'org':org, 'hash_tags':getHashes(), 'announcements':announcements}
		
def new_message(request):
	profile = request.user.get_profile()
	dict = getDict(request, profile.university.name, slugify(profile.organization.name))
	return render_to_response('users/new_message.html', dict, context_instance=RequestContext(request))

def start(request):
	profile = request.user.get_profile()
	dict = getDict(request, profile.university.name, slugify(profile.organization.name))
	return render_to_response('users/start.html', dict, context_instance=RequestContext(request))
	
def home(request):
	topics = Topic.objects.filter(organization=request.user.get_profile().organization, university=request.user.get_profile().university, members = request.user)
	
	dict = getPagedTopics(request, topics)
	return render_to_response('users/index.html', dict, context_instance=RequestContext(request))
	
def inbox(request):
	conversations = request.user.get_profile().conversations.all()
	profile = request.user.get_profile()
	dict = getDict(request, profile.university.name, slugify(profile.organization.name))
	dict.update({'title':'inbox'})
	dict = paginateCollection(request, dict, conversations, "conversations")
	return render_to_response('users/inbox.html', dict, context_instance=RequestContext(request))

def bulletin(request):
	return render_to_response('users/bulletin.html', {'title': 'bulletin'},context_instance=RequestContext(request))

def calendar(request):
	return render_to_response('users/calendar.html', {'title': 'calendar'}, context_instance=RequestContext(request))

@csrf_exempt
def save_canvas(request):
	if request.is_ajax():
		if request.POST['user'] and request.POST['data']:
			user = User.objects.get(pk=request.POST['user'])
			user.get_profile().canvas = request.POST['data']
			user.get_profile().save()
			user.save()
			return HttpResponse("success")
	return HttpResponse("fail")
