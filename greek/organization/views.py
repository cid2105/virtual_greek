# Create your views here.
from django.shortcuts import *
from unis.models import *
from django.conf import settings
from models import *
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from forms import *
from users.models import *
from organization.models import *
from datetime import * 
from django.core.urlresolvers import reverse
import re
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

PAGE_SIZE = 6
PHOTO_SIZE = 9
ANNOUNCEMENT_SIZE = 4

@csrf_exempt
def vote_reply(request, uni_name, org_name):
	if request.is_ajax():
		if 'type' and 'reply' in request.POST:
			reply = Reply.objects.get(id=request.POST['reply'])
			type = request.POST['type']
			if type == 'praise':
				reply.praises.add(request.user)
				if request.user in reply.tazes.all():
					reply.tazes.remove(request.user)
			if type == 'unpraise':
				reply.praises.remove(request.user)
			if type == 'taze':
				reply.tazes.add(request.user)
				if request.user in reply.praises.all():
					reply.praises.remove(request.user)
			if type == 'untaze':
				reply.tazes.remove(request.user)
			reply.save()
			return HttpResponse("success")
	return HttpResponse("failure")				
				
def getDict(request, uni_name, org_name, Title=True):
	base_url = reverse('uni_org_index', args=[uni_name, org_name])
	org_name = re.sub('\-', ' ', org_name).title()
	org = Organization.objects.get(university__name = uni_name, name = org_name)
	uni = University.objects.get(name = uni_name)
	title = 'home' if Title else 'members' 
	try:
		chapter = Chapter.objects.get(university = uni, organization=org)
	except Chapter.DoesNotExist:
		chapter = Chapter(organization=org, university = uni)
		chapter.save()
	dict = {'base_url': base_url, 'uni_name': uni_name, 'org_name':org_name, 'org':org, 'uni':uni, 'title':title, 'hash_tags':getHashes(), 'chapter':chapter}
	if len(Announcement.objects.filter(university = uni, organization=org)) > 0:
		dict = paginateCollection(request, dict, Announcement.objects.filter(university = uni, organization=org), 'announcements')
	return dict

@csrf_exempt
def delete_reply(request, uni_name, org_name, topic_id):
	if request.is_ajax() and request.POST.get('reply_id'):
		reply = Reply.objects.get(id=int(request.POST['reply_id']))
		reply.delete()
		return HttpResponse('success')
	return HttpResponse('failure')
	
def paginateCollection(request, dict, collection, key, photos = False, announcements = False):
	
	if key == 'announcements':
		paginator = Paginator(collection, ANNOUNCEMENT_SIZE)
	else:
		paginator = Paginator(collection, PAGE_SIZE) if not photos else Paginator(collection, PHOTO_SIZE)
	if not page in request.GET:
		page = 1
	else:
		page = request.GET.get('page')	
	try:
		collection = paginator.page(page)
	except PageNotAnInteger:
		collection = paginator.page(1)
	except EmptyPage:
		collection = paginator.page(paginator.num_pages)
	dict.update({key:collection, 'paginator':paginator, 'page':page})
	return dict
	
def new_topic_form(request, uni_name, org_name):
	return render_to_response('organization/new_topic_form.html', getDict(request, uni_name, org_name), context_instance=RequestContext(request))

def invite(request, uni_name, org_name):
	return render_to_response('organization/invite.html', getDict(request, uni_name, org_name), context_instance=RequestContext(request))	
	
def getClasses():
	array = []
	if datetime.now().month >= 8:
		for i in range(4):
			array.append(i+1+datetime.now().year)
	else:
		for i in range(4):
			array.append(i+datetime.now().year)
	return array
	
@csrf_exempt
def index(request, uni_name, org_name):
	dict = getDict(request, uni_name, org_name, False)
	dict['classes'] = getClasses()
	if request.is_ajax() and request.POST:
		if 'param' and 'value' in request.POST:
			chapter = dict['chapter']
			if request.POST['param'] == 'chapter':
				chapter.name = request.POST['value']
			elif request.POST['param'] == 'about':
				chapter.about = request.POST['value']				
			else:
				chapter.year_founded = int(request.POST['value'])
			chapter.save()
			return HttpResponse('success')
		return HttpResponse('failure')
	return render_to_response('organization/index.html',dict, context_instance=RequestContext(request))

def chapter(request, uni_name, org_name):
	dict = getDict(request, uni_name, org_name)
	dict.update({'title':'chapter'})
	return render_to_response('organization/chapter.html', dict, context_instance=RequestContext(request))
	
def home(request, uni_name, org_name):
	org_name = re.sub('\-', ' ', org_name).title()
	org = Organization.objects.get(university__name = uni_name, name = org_name)
	return render_to_response('organization/home.html', {'org':org, 'title': org_name}, context_instance=RequestContext(request))

def getHashes():
	hashes = []
	for hash in HASH_CHOICES:
		hashes.append("#" + hash[0].replace("#", "").capitalize())
	return hashes
	
def bulletin(request, uni_name, org_name):
	dict = getDict(request, uni_name, org_name)
	dict.update(hash_tags=getHashes())
	return render_to_response('organization/bulletin.html', dict, context_instance=RequestContext(request))

def album(request, uni_name, org_name, album_id):
	dict = getDict(request, uni_name, org_name)
	album = dict['org'].albums.get(id=album_id)	
	albums = dict['org'].albums.all()
	albums_by_year = {}
	if albums:
		for al in albums:
			if al.date.year in albums_by_year:      
				albums_by_year[al.date.year].append(al)
			else:
				albums_by_year[al.date.year] = [al]
	dict.update({'albums':albums, 'albums_by_year':albums_by_year, 'album':album, 'title':'gallery'})
	dict = paginateCollection(request, dict, album.photos.all(), 'photos', True)
	return render_to_response('organization/album.html', dict, context_instance=RequestContext(request))

def gallery(request, uni_name, org_name):
	dict = getDict(request, uni_name, org_name)
	albums = dict['org'].albums.all()
	albums_by_year = {}
	if albums:
		for album in albums:
			if album.date.year in albums_by_year:      
				albums_by_year[album.date.year].append(album)
			else:
				albums_by_year[album.date.year] = [album]
	dict.update({'albums':albums, 'title':'gallery', 'albums_by_year':albums_by_year})
	return render_to_response('organization/gallery.html', dict, context_instance=RequestContext(request))	
	
def new_album(request, uni_name, org_name):
	dict = getDict(request, uni_name, org_name)
	dict.update({'title':'gallery', 'session_cookie_name': settings.SESSION_COOKIE_NAME, 'session_key': request.session.session_key})

	if 'title' and 'description' in request.POST and 'photos' in request.FILES:
		album = Album(title = request.POST['title'], description = request.POST['description'])
		album.save()
		photo_list = []
		for file in request.FILES.getlist('photos'):
			pic = Photo.objects.create(url = file)
			pic.save()
			photo_list.append(pic)
		map(album.photos.add, photo_list)
		if len(photo_list) > 0:
			album.thumbnail = photo_list[0] 

  		album.save()
		org = dict['org']
		org.albums.add(album)
		org.save()
		dict['org'] = org
		return render_to_response('organization/gallery.html', dict, context_instance=RequestContext(request))	
	dict['error'] = 'One or more fields are incomplete'
	return render_to_response('organization/gallery.html', dict, context_instance=RequestContext(request))	
		
	
def threads(request, uni_name, org_name):
	dict = getDict(request, uni_name, org_name)
	dict['topics'] = Topic.objects.filter(organization=request.user.get_profile().organization, university=request.user.get_profile().university, members__id__contains = request.user.id )
	return render_to_response('organization/threads.html', dict, context_instance=RequestContext(request))	
	
def new_announcement(request, uni_name, org_name):
	dict = getDict(request, uni_name, org_name)
	if request.POST:
		hash = request.POST['hash_tag']
		content = request.POST['content']
		announcement = Announcement(author=request.user, date=datetime.now(), content=content, hash=hash, university=dict['uni'], organization=dict['org'])
		announcement.save()
	dict['topics'] = Topic.objects.filter(organization=request.user.get_profile().organization, university=request.user.get_profile().university, members__id__contains = request.user.id )	
	return render_to_response('users/index.html', dict, context_instance=RequestContext(request))	
	
def members(request, uni_name, org_name):
	if request.is_ajax():
		org_name = re.sub('\-', ' ', org_name).title()
		org = Organization.objects.get(university__name = uni_name, name = org_name)
		return render_to_response('organization/members.html', {'org':org, 'title': org_name}, context_instance=RequestContext(request))
	
def topic(request, uni_name, org_name, topic_id):
	topic = get_object_or_404(Topic, pk=topic_id)
	replies = topic.reply_set.all()
	dict = getDict(request, uni_name, org_name)
	dict.update({'topic':topic})
	dict = paginateCollection(request, dict, replies, "replies")
	if request.POST and request.POST['reply']:
		reply = Reply(author = request.user, date=datetime.now(), topic = topic, content=request.POST['reply'])
		reply.save()
		dict.update({'new_post':True})
	return render_to_response('organization/topic.html', dict, context_instance=RequestContext(request))

def profile(request, uni_name, org_name, user_id):
	user = get_object_or_404(User, pk=user_id)
	dict = getDict(request, uni_name, org_name)
	dict['user'] = user
	dict.update({'title':'profile', 'curr_year':datetime.now().year, 'step':10 })
	return render_to_response('organization/profile.html', dict, context_instance=RequestContext(request))
			
def new_topic(request, uni_name, org_name):
	if request.is_ajax():	
		form = TopicForm(request.POST)
		clean = form.is_valid()
		errors = ""
		if not clean:
			for e in form.errors.iteritems():
				errors += str(e[1])
		members = request.POST['privacy']
		org = request.user.get_profile().organization
		uni = request.user.get_profile().university
		if members in ['Fraternity', 'Sorority', 'Society']:
			members = User.objects.filter(userprofile__organization = org, userprofile__university = uni)
		elif members in ['Brothers', 'Sisters', 'Members']:
			members = User.objects.filter(userprofile__organization = org, userprofile__university = uni).filter(userprofile__role = 'Brother')						
		elif members == 'Pledges':
			members = User.objects.filter(userprofile__organization = org, userprofile__university = uni).filter(userprofile__role = 'Pledge')						
		elif members == 'Public':
			members = User.objects.all()
		else:
			member_list = [x.strip() for x in members.split(",")]
			members = User.objects.filter(userprofile__name__in = member_list)
		topic = Topic(author = request.user, organization = org, date=datetime.now(), university=uni, topic=request.POST['topic'])
		topic.save()
		reply = Reply(author = request.user, date=datetime.now(), topic = topic, content=request.POST['body'])
		reply.save()
		for member in members:
			topic.members.add(member)
		return HttpResponse(errors)
	else:
		return HttpResponse("fail")
		