from django.db import models
from django.contrib.auth.models import User
from unis.models import University
from users.models import *
import s3 as site_s3

ORG_CHOICES = (
    ('Fraternity', 'Fraternity'),
    ('Sorority', 'Sorority'),
    ('Society', 'Society'),
)

HASH_CHOICES = (
				('#abroad', '#abroad'),
			    ('#careers', '#careers'),
			    ('#classes', '#classes'),
				('#community_service', '#community_service'),
			    ('#drinks', '#drinks'),
			    ('#events', '#events'),
			    ('#food', 	'#food'),
			    ('#funny', '#funny'),
			    ('#giveaway', '#giveaway'),
			    ('#help', '#help'),
			    ('#housing', '#housing'),
				('#lastnight', '#lastnight'),
			    ('#nightlife', '#nightlife'),
			    ('#now', '#now'),
			    ('#pledges', '#pledges'),
			    ('#random', '#random'),
			    ('#rush', '#rush'),
			    ('#sports', '#sports'),
			    ('#textbooks', '#textbooks'),	
				('#tickets', '#tickets'),						
				('#tonight', '#tonight'),	
				('#tomorrow', '#tomorrow'),	
)

class Photo(models.Model):
	date = models.DateTimeField(auto_now_add=True,  blank=True, null=True)
	caption = models.CharField(max_length=200, blank=True, null=True)
	tagged = models.ManyToManyField(User, related_name="tagged", blank=True, null=True)
	key = models.CharField(max_length=100, blank=True, null=True)
	thumbnail = models.FileField(upload_to="media/organization_thumbnails")
	new_upload = models.NullBooleanField(default=False)
	
	def _get_file_url(self):
	    return site_s3.get_s3_url('gg_organization_photos', self.key)
	url = property(_get_file_url)
	
	class Meta:
		ordering = ['-date']

class Album(models.Model):
	description = models.TextField(blank=True, null=True)
	title = models.CharField(max_length=200, blank=True, null=True)
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True)
	photos = models.ManyToManyField(Photo, blank=True, null=True, related_name="album_photos")		
	public = models.BooleanField(default=False)
	thumbnail = models.ForeignKey(Photo, blank=True, null=True, related_name="album_thumbnail")
	date = models.DateTimeField(auto_now_add=True,  blank=True, null=True)
	
	def __unicode__(self):
		return self.title
	
	class Meta:
		ordering = ['-date']

class Organization(models.Model):
	name = models.CharField(max_length=200)
	logo_key = models.CharField(max_length=500, blank=True, null=True)
 	type = models.CharField(max_length=100, choices=ORG_CHOICES)
	nickname = models.CharField(max_length=100, blank=True, null=True)
	
	def _get_logo_url(self):
	    return site_s3.get_s3_url('gg_organization_logos', self.logo_key)
	logo = property(_get_logo_url)
	
	def __str__(self):
		return self.name
		
	def member_type(self):
		if self.type == "Fraternity":
			return "Brother"
		elif self.type == "Sorority":
			return "Sister"
		else:
			return "Member"
			
class Chapter(models.Model):
	name = models.CharField(max_length=200, blank=True, null=True)
	about = models.TextField(blank=True, null=True)
	year_founded = models.IntegerField(blank=True, null=True)
 	organization = models.ForeignKey(Organization)
 	university = models.ForeignKey('unis.University', unique=True)
	members = models.ManyToManyField(User, related_name="organization_group_members", null=True, blank=True)
	rushing = models.ManyToManyField(User, related_name="organization_group_rushing", null=True, blank=True)
	alumni = models.ManyToManyField(User, related_name="organization_group_alumni", null=True, blank=True)
	president = models.ForeignKey(User, related_name="organization_president", null=True, blank=True)
	vice_president = models.ForeignKey(User, related_name="organization_vice_president", null=True, blank=True)
	treasurer = models.ForeignKey(User, related_name="organization_treasurer", null=True, blank=True)
	secretary = models.ForeignKey(User, related_name="organization_secretary", null=True, blank=True)
	rush_chair = models.ForeignKey(User, related_name="organization_rush_chair", null=True, blank=True)
	social_chair = models.ForeignKey(User, related_name="organization_social_chair", null=True, blank=True)
	house_manager = models.ForeignKey(User, related_name="organization_house_manager", null=True, blank=True)
	albums = models.ManyToManyField(Album, blank=True, null=True, related_name="organization_albums")
	
	def __unicode__(self):
		return str(self.organization) + " - " + str(self.name)
	
	def board(self):
		list = []
		if self.president is not None:
			list.append(['President', self.president.get_profile()])
		if self.vice_president is not None:
			list.append(['Vice-President', self.vice_president.get_profile()])
		if self.treasurer is not None:
			list.append(['Treasurer', self.treasurer.get_profile()])
		if self.secretary is not None:
			list.append(['Secretary', self.secretary.get_profile()])
		if self.rush_chair is not None:
			list.append(['Rush Chair', self.rush_chair.get_profile()])		
		if self.social_chair is not None:
			list.append(['Social Chair', self.social_chair.get_profile()])
		if self.house_manager is not None:
			list.append(['House Manager', self.house_manager.get_profile()])
		
		return list
		
	def positions(self):
		return ['President', 'Vice-President', 'Treasurer', 'Secretary', 'Rush Chair', 'Social Chair', 'House Manager', 'Brother', 'Rush']
		
	def exec_board(self):
		return [self.president.get_profile(), self.vice_president.get_profile(), self.treasurer.get_profile(), self.secretary.get_profile(), self.rush_chair.get_profile(), self.social_chair.get_profile(), self.house_manager.get_profile()]
		
	def status_choices(self):	
		type = self.organization.member_type
		return [type, 'Rush', 'Alumni', 'Inactive']
	
class Topic(models.Model):
	author = models.ForeignKey(User)
	date = models.DateTimeField(auto_now_add=True)
	topic = models.CharField(max_length=250)
	body = models.TextField()
	members = models.ManyToManyField(User, related_name="privacy_group_members", null=True, blank=True)
	chapter = models.ForeignKey(Chapter, null=True, blank=True)
	university = models.ForeignKey(University, null=True, blank=True)
	
	def author_name(self):
		return self.author.get_profile().facebook_name
		
	def count(self):
		return len(self.reply_set.all())
	
	def last_reply(self):
		return self.reply_set.latest('date')
		
	def __unicode__(self):
		return self.topic

	class Meta:
		ordering = ['-date']

class Reply(models.Model):
	author = models.ForeignKey(User)
	date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	content = models.TextField(blank=True, null=True)
	topic = models.ForeignKey(Topic, blank=True, null=True)
	praises = models.ManyToManyField(User, blank=True, null=True, related_name="reply_praises")
	tazes = models.ManyToManyField(User, blank=True, null=True, related_name="reply_tazes")

	def __unicode__(self):
		return self.content
	
	def preview(self):
		if self.content > 20:
			return self.content[:20] + "..."
		else:
			return self.content
	class Meta:
		ordering = ['-date']

class Announcement(models.Model):	
	author = models.ForeignKey(User)
	university = models.ForeignKey(University)
	chapter = models.ForeignKey(Chapter)
	date = models.DateTimeField(auto_now_add=True)
	content = models.TextField()
	hash = models.CharField(max_length=100)

	def __unicode__(self): 
		return (self.content[0:140] + "...") if (len(self.content) > 140) else self.content
		
	def announcer(self):
		return self.author.get_profile().facebook_name
		
	class Meta:
		ordering = ['-date']

