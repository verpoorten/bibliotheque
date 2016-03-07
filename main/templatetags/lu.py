
from django import template
from main.models import Livre

register = template.Library()

@register.assignment_tag(takes_context=True)
def lu(context):
    request = context['request']
    livre = context['livre']
    return Livre.is_lu(livre,request.user)
