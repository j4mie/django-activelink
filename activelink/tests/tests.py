from django.template import Template, Context, loader
from django.test.client import RequestFactory


rf = RequestFactory()


# add activelink to builtin tags
loader.add_to_builtins('activelink.templatetags.activelink')

def render(template_string, dictionary=None):
    """Render a template from the supplied string, with optional context data."""
    context = Context(dictionary)
    return Template(template_string).render(context)


def test_ifactive():
    template = """{% ifactive "test" %}on{% else %}off{% endifactive %}"""

    data = {'request': rf.get('/test-url/')}
    rendered = render(template, data)
    assert rendered == 'on'

    data = {'request': rf.get('/not-test-url/')}
    rendered = render(template, data)
    assert rendered == 'off'

def test_ifactive_without_else():
    template = """{% ifactive "test" %}on{% endifactive %}"""

    data = {'request': rf.get('/test-url/')}
    rendered = render(template, data)
    assert rendered == 'on'

    data = {'request': rf.get('/not-test-url/')}
    rendered = render(template, data)
    assert rendered == ''

def test_ifactive_with_literal_url():
    template = """{% ifactive "/my-url/" %}on{% else %}off{% endifactive %}"""

    data = {'request': rf.get('/my-url/')}
    rendered = render(template, data)
    assert rendered == 'on'

    data = {'request': rf.get('/not-my-url/')}
    rendered = render(template, data)
    assert rendered == 'off'

def test_ifactive_with_url_in_variable():
    template = """{% ifactive myurl %}on{% else %}off{% endifactive %}"""

    data = {'request': rf.get('/test-url/'), 'myurl': '/test-url/'}
    rendered = render(template, data)
    assert rendered == 'on'

    data = {'request': rf.get('/test-url/'), 'myurl': '/not-test-url/'}
    rendered = render(template, data)
    assert rendered == 'off'

def test_ifstartswith():
    template = """{% ifstartswith "test" %}on{% else %}off{% endifactive %}"""

    data = {'request': rf.get('/test-url/')}
    rendered = render(template, data)
    assert rendered == 'on'

    data = {'request': rf.get('/test-url/sub/')}
    rendered = render(template, data)
    assert rendered == 'on'

    data = {'request': rf.get('/not-test-url/')}
    rendered = render(template, data)
    assert rendered == 'off'
