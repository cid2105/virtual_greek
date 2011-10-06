from django import template
from django.template.defaultfilters import stringfilter
import string, re, unicodedata
from datetime import *
register = template.Library()
@register.filter
def getYear(value):
	value = str(value)
	if len(value) == 2:
		return '\'' + value
	elif len(value) == 4:
		return '\'' + value[2:]
	else:
		return ''