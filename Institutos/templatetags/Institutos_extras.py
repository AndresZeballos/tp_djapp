from django import template

register = template.Library()

@register.filter
def with_centro(things, c):
    return things.filter(centro_id=c.id)