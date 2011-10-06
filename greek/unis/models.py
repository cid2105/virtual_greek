from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

profanities = settings.PROFANITIES_LIST

class University(models.Model):
	name = models.CharField(max_length=200)
	date = models.DateTimeField(auto_now_add=True)
	

	def __unicode__(self): 
		return self.name

class Forum(models.Model):
	university = models.OneToOneField(University)
	
class Post(models.Model):
	editable = models.BooleanField()
	author = models.OneToOneField(User)
	date = models.DateTimeField('date added')
	content = models.TextField()
	forum = models.ForeignKey(Forum)
	def isSafe(self):
		content_set = set(self.content.split(" "))
		profanities_set = set(profanities.split(" "))
		if len(content_set.intersection(profanities_set)) == 0:
			return True
		else:
			return False