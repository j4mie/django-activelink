import warnings
from django.template import Template, Context, loader
from django.test.client import RequestFactory
from django.conf import settings


rf = RequestFactory()


# add activelink to builtin tags
loader.add_to_builtins('activelink.templatetags.activelink')

def render(template_string, dictionary=None):
    """Render a template from the supplied string, with optional context data."""
    context = Context(dictionary)
    return Template(template_string).render(context)


def test_ifactive():
    template = """{% active "test" "on" "off" %}"""

    data = {'request': rf.get('/test-url/')}
    rendered = render(template, data)
    print(rendered)
    assert rendered == 'on'

    data = {'request': rf.get('/not-test-url/')}
    rendered = render(template, data)
    assert rendered == 'off'


def test_ifactive_class_from_settings():
    template = """{% active "test" %}"""
    data = {'request': rf.get('/test-url/')}
    rendered = render(template, data)

    assert rendered == settings.ACTIVE_LINK_CLASS


def test_ifactive_without_else():
    template = """{% active "test" "on" %}"""

    data = {'request': rf.get('/test-url/')}
    rendered = render(template, data)
    assert rendered == 'on'

    data = {'request': rf.get('/not-test-url/')}
    rendered = render(template, data)
    assert rendered == settings.INACTIVE_LINK_CLASS or ''


def test_ifactive_with_literal_url():
    template = """{% active "/my-url/" "on" "off" %}"""

    data = {'request': rf.get('/my-url/')}
    rendered = render(template, data)
    assert rendered == 'on'

    data = {'request': rf.get('/not-my-url/')}
    rendered = render(template, data)
    assert rendered == 'off'


def test_ifactive_with_url_in_variable():
    template = """{% active myurl "on" "off" %}"""

    data = {'request': rf.get('/test-url/'), 'myurl': '/test-url/'}
    rendered = render(template, data)
    assert rendered == 'on'

    data = {'request': rf.get('/test-url/'), 'myurl': '/not-test-url/'}
    rendered = render(template, data)
    assert rendered == 'off'

def test_ifactive_with_url_arguments():
    template = """{% active "test_with_arg" "on" "off" "somearg" %}"""

    data = {'request': rf.get('/test-url-with-arg/somearg/')}
    rendered = render(template, data)
    assert rendered == 'on'

    data = {'request': rf.get('/test-url-with-arg/other/')}
    rendered = render(template, data)
    assert rendered == 'off'

    template = """{% active "test_with_kwarg" "on" "off" arg="somearg" %}"""

    data = {'request': rf.get('/test-url-with-kwarg/somearg/')}
    rendered = render(template, data)
    assert rendered == 'on'

    data = {'request': rf.get('/test-url-with-kwarg/other/')}
    rendered = render(template, data)
    assert rendered == 'off'


def test_ifstartswith():
    template = """{% startswith "test" "on" "off" %}"""

    data = {'request': rf.get('/test-url/')}
    rendered = render(template, data)
    assert rendered == 'on'

    data = {'request': rf.get('/test-url/sub/')}
    rendered = render(template, data)
    assert rendered == 'on'

    data = {'request': rf.get('/not-test-url/')}
    rendered = render(template, data)
    assert rendered == 'off'


def test_fails_gracefully_without_request():
    template = """{% active "test" "on" "off" %}"""

    with warnings.catch_warnings(record=True) as w:
        rendered = render(template)
        print(w)
        assert len(w) == 1
        assert rendered == 'off'

def test_with_querystring():
    template = """{% active "test" "on" "off" %}"""

    data = {'request': rf.get('/test-url/?foo=bar')}
    rendered = render(template, data)
    assert rendered == 'on'
