from django.template import Library

register = Library()

@register.filter(name="subtract_incr")
def subtract_incr(value1, value2):
	return value1-value2+1
		
@register.filter
def subtract(value1, value2):
	#{% for i in 3|get_range %}
	return value1-value2
	

