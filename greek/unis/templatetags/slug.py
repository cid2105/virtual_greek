from django import template
from django.template.defaultfilters import stringfilter
import string, re, unicodedata
register = template.Library()


@register.filter(name="phone_format")
def phone_format(phone):
	phone = str(phone)
	return '-'.join((phone[:3],phone[3:6],phone[6:]))

@register.filter(name="preview")
def preview(str):
	if len(str) > 20:
		return str[:20] + "..."
	return str

@register.filter
@stringfilter

def slug(value):
	slug = unicodedata.normalize('NFKD', value)
	slug = slug.encode('ascii', 'ignore').lower()
	slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
	slug = re.sub(r'[-]+', '-', slug)
	slug = ' '.join(slug.split('-')).title()
	slug = re.sub(r"\s+", '-', slug)
	return slug