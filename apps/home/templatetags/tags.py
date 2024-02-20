from django import template
register = template.Library()

@register.simple_tag()
def multiply(a, b, *args, **kwargs):
    # you would need to do any localization of the result here
    return a * b

@register.filter
def remove_dot(value):
  text = str(value).replace('.','')
  return text

@register.filter
def literales(value):
    value = int(value)
    if 19 <= value <= 20:
        return 'A'
    elif 16 <= value <= 18:
        return 'B'
    elif 12 <= value <= 15:
        return 'C'
    elif 1 <= value <= 11:
        return 'D'
    else:
        return value