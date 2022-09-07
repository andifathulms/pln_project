from django import template
register = template.Library()

@register.filter
def to_class_name(value):
    return value.__class__.__name__

@register.simple_tag(name="call_method")
def call_method(obj, method_name, *args):
    method = getattr(obj, method_name)
    return method(*args)