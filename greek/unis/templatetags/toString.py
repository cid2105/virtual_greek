from django import template
from django.template.defaultfilters import stringfilter
import string

register = template.Library()

@register.filter
@stringfilter
def toString(value):
	return str(value)
