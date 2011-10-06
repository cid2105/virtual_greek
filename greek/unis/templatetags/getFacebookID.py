from django import template
from django.template.defaultfilters import stringfilter
import string, re, unicodedata
register = template.Library()

@register.filter
def getFacebookID(value):
	return value.replace("http://www.facebook.com/", "")