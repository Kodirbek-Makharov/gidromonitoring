from django import template
from django.db.models import Q

register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter(name='not_has_group') 
def not_has_group(user, group_name):
    return user.groups.filter(~Q(name=group_name)).exists()