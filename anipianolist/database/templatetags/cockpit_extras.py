from django import template
import environ

env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env()

register = template.Library() 

def check(user, group):
    return user.groups.filter(name=env(group)).exists() 

@register.filter(name='is_admin') 
def is_admin(user):
    return check(user, 'ADMIN_GROUP')

@register.filter(name='is_moderator') 
def is_moderator(user):
    return check(user, 'MODERATOR_GROUP')

@register.filter(name='is_maintainer') 
def is_moderator(user):
    return check(user, 'MAINTAINER_GROUP')