from django.template import Library

register = Library()

@register.filter
def get_range( value ):
	#{% for i in 3|get_range %}
	return range( value )
	

	