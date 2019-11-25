from django import template
from question.models import Course

register = template.Library()

@register.filter
def get_course_name_by_id(value):
	try:
		course_name = Course.objects.get(id=value).name
	except Course.DoesNotExist:
		course_name = ""
	return course_name
