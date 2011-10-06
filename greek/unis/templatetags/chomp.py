from django import template
from django.template.defaultfilters import stringfilter
import string
register = template.Library()

@register.filter
@stringfilter

def chomp(value):
	lower = string.lower(value)
	return lower.replace(' ', '')
	