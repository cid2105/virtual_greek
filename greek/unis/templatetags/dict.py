from django import template
register = template.Library()
import ast
@register.filter
def dict(value, arg):
	value = str(value)
	dict = ast.literal_eval(value)
	return dict[arg]
