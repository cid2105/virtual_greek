from django import forms
from unis.models import University
from organization.models import Organization
from django.contrib.auth.models import User

class TopicForm(forms.Form):
	topic = forms.CharField(max_length=250)
	body = forms.CharField()
	privacy = forms.CharField()
	
	def clean_topic(self):
		data = self.cleaned_data['topic']
		return data