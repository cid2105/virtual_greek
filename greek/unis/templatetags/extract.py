from django import template
from django.template.defaultfilters import stringfilter
import string, re, unicodedata
import json
register = template.Library()

@register.filter

def extract(value, arg):
	index = value.find(arg)
	end = value.find(",", index)
	start = value.find(":", index) + 2
	return value[start:end].replace("\"", "")