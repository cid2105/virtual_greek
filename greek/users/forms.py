from django import forms
from unis.models import University
from organization.models import Organization
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
	fratname = forms.CharField(max_length=100)
	email = forms.EmailField(max_length=100)
	university = forms.CharField(max_length=100)
 	type = forms.CharField(max_length=100)
	def clean_email(self):
		data = self.cleaned_data['email']
		try: 
			User.objects.get(email=data)
			raise forms.ValidationError("An account for this email already exists")
			return data
		except User.DoesNotExist:
			return data
				 
	def clean(self):
		cleaned_data = self.cleaned_data
		fratname = cleaned_data["fratname"]
		university = University.objects.get(name = cleaned_data["university"])
		if Organization.objects.filter(name = str(fratname), university=university):
            # We know these are not in self._errors now (see discussion
            # below).
			msg = u"This fraternity already exists"
			self._errors["fratname"] = self.error_class([msg])

			del cleaned_data["fratname"]
			del cleaned_data["university"]

		return cleaned_data