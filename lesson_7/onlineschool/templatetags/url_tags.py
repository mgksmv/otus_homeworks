from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def relative_url(context, **kwargs):
    query = context['request'].GET.copy()
    for parameter_name, value in kwargs.items():
        query[parameter_name] = value
    return query.urlencode()
