from django.db import models
from organization.models import Organization
from unis.models import University
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from users.fields import JSONField
from extra import ContentTypeRestrictedFileField

class Message(models.Model):
	editable = models.BooleanField()
	author = models.ForeignKey(User, related_name='private_message_author')
	recipient = models.ForeignKey(User, blank=True, null=True)
	author_viewed = models.BooleanField(default=True)
	recipient_viewed = models.BooleanField(default=False)
	content = models.TextField(blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True)

class Conversation(models.Model):
	partner = models.ForeignKey(User, related_name='conversator', blank=True, null=True)
	viewed = models.BooleanField(default=True)
	messages = models.ManyToManyField(Message, blank=True, null=True)
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True)
	
	def preview(self):
		if len(self.messages.latest('date').content) > 50:
			return self.messages.latest('date').content[0:50] + "..."
		else:
			return self.messages.latest('date').content
	
class Linkedin(models.Model):
	matriculate_year = models.IntegerField(blank=True, null=True)
	graduate_year = models.IntegerField(blank=True, null=True)
	honors = models.TextField(blank=True, null=True)
	public_profile_url = models.CharField(max_length=300, blank=True, null=True)
	
class Position(models.Model):
	start_month = models.IntegerField(blank=True, null=True)
	start_year = models.IntegerField(blank=True, null=True)
	current = models.BooleanField(default=False, blank=True)
	title = models.CharField(max_length=250, blank=True, null=True)
	company = models.CharField(max_length=250, blank=True, null=True)
	summary = models.TextField(blank=True, null=True)
	end_month = models.IntegerField(blank=True, null=True)
	end_year = models.IntegerField(blank=True, null=True)
	linkedin = models.ForeignKey(Linkedin, null=True, blank=True)
		
class UserProfile(models.Model):
	ROLE_CHOICES = (
		(u'President', u'President'),
		(u'Vice-President', u'Vice-President'),
		(u'Treasurer', u'Treasurer'),
		(u'Social Chair', u'Social Chair'),
		(u'Rush Chair', u'Rush Chair'),
		(u'House Manager', u'House Manager'),
		(u'Brother', u'Brother'),
		(u'Pledge', u'Pledge'),
	)  
	user = models.OneToOneField(User, unique=True)
	full_name = models.CharField(max_length=100, blank=True)
	nickname = models.CharField(max_length=100, blank=True)
	profile_picture = models.ImageField(upload_to='media/profile_pictures', blank=True)
	organization = models.ForeignKey(Organization, null=True)
	university = models.ForeignKey(University, null=True)
	about_me = models.TextField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	facebook_id = models.IntegerField(blank=True, null=True)
	facebook_name = models.CharField(max_length=255, blank=True, null=True)
	facebook_profile_url = models.TextField(blank=True, null=True)
	website_url = models.TextField(blank=True, null=True)
	major = models.CharField(max_length=250, blank=True, null=True)
	image = models.ImageField(blank=True, null=True, upload_to='profile_images')
	date_of_birth = models.DateField(blank=True, null=True)
	raw_data = models.TextField(blank=True, null=True)
	conversations = models.ManyToManyField(Conversation, blank=True, null=True, related_name='user_private_messages')
	linkedin = models.ForeignKey(Linkedin, unique=True, null=True, blank=True)
	ip = models.IPAddressField(blank=True, null=True, default=127.0.0.1)
	role = models.CharField(max_length=100, choices=ROLE_CHOICES)
	canvas = models.TextField(blank=True, null=True)
	phone_number = models.IntegerField(blank=True, null=True)
	resume = ContentTypeRestrictedFileField(upload_to='media/resumes', content_types=['application/pdf', 'application/zip', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'], max_upload_size=5242880, blank=True, null=True)
	
	def first_name(self):
		return self.facebook_name.split(" ")[0]
		
	def __str__(self):  
		if self.facebook_name:
			return self.facebook_name  
		else:
			return ""

def create_user_profile(sender, instance, created, **kwargs):  
	if created:  
		profile, created = UserProfile.objects.get_or_create(user=instance)  

post_save.connect(create_user_profile, sender=User)