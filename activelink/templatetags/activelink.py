from django.template import Library
from django.core.urlresolvers import reverse, NoReverseMatch
from django.conf import settings

register = Library()


def get_current_url_pattern(pattern, *args, **kwargs):
    try:
        # Let's try to search by urlname first
        # according to django's warnings, we should never mix
        # *args and **kwargs, therefore we reverse using either
        # *args or **kwargs
        if args:
            pattern = reverse(pattern, args=args)
        else:
            pattern = reverse(pattern, kwargs=kwargs)
    except NoReverseMatch:
        # fallback to path
        pass

    return pattern


def output_class(condition, active_class, inactive_class):
    if condition:
        act = getattr(settings, 'ACTIVE_LINK_CLASS')
        if active_class:
            act = active_class
        return act
    else:
        inact = getattr(settings, 'INACTIVE_LINK_CLASS')
        if inactive_class:
            inact = inactive_class
        return inact


def get_request_or_warn(context):
    request = context.get('request')
    current_url = None
    if not request:
        import warnings
        warnings.warn("The activelink templatetags require that a "
                      "'request' variable is available in the template's "
                      "context. Check you are using a RequestContext to "
                      "render your template, and that "
                      "'django.core.context_processors.request' is in "
                      "your TEMPLATE_CONTEXT_PROCESSORS setting"
        )
    else:
        current_url = request.path

    return (request, current_url)


@register.simple_tag(takes_context=True)
def active(context, pattern, active_class='active', inactive_class='',
           *args, **kwargs):

    pattern = get_current_url_pattern(pattern, *args, **kwargs)

    request, current_url = get_request_or_warn(context)
    if not request:
        condition = False
    else:
        condition = current_url == pattern

    return output_class(
        condition,
        active_class,
        inactive_class
    )


@register.simple_tag(takes_context=True)
def startswith(context, pattern, active_class='active', inactive_class='',
               *args, **kwargs):
    pattern = get_current_url_pattern(pattern, *args, **kwargs)

    request, current_url = get_request_or_warn(context)
    if not request:
        condition = False
    else:
        condition = current_url.startswith(pattern)

    return output_class(
        condition,
        active_class,
        inactive_class
    )
