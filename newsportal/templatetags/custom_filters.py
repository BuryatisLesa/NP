from django import template


register = template.Library()

@register.filter()
def type(var):
    return f'{var}'

