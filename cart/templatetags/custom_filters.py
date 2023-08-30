from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return value * arg
    except (ValueError, TypeError):
        return None



from django import template

register = template.Library()

@register.filter
def calculate_sum(queryset, attribute):
    return sum(getattr(obj, attribute) for obj in queryset)
