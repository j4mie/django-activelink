from django.template import Library, Node, NodeList, VariableDoesNotExist
from django.core.urlresolvers import NoReverseMatch
from django.templatetags.future import url
from django.template.defaulttags import TemplateIfParser


register = Library()


class ActiveLinkNodeBase(Node):

    def __init__(self, urlnode, var, nodelist_true, nodelist_false):
        self.urlnode = urlnode
        self.var = var
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false

    def render(self, context):
        try:
            var = self.urlnode.render(context)
        except NoReverseMatch:
            try:
                var = self.var.eval(context)
            except VariableDoesNotExist:
                var = None

        request = context.get('request')

        # Gracefully fail if request is not in the context
        if not request:
            import warnings
            warnings.warn("The activelink templatetags require that a "
                          "'request' variable is available in the template's "
                          "context. Check you are using a RequestContext to "
                          "render your template, and that "
                          "'django.core.context_processors.request' is in "
                          "your TEMPLATE_CONTEXT_PROCESSORS setting"
            )
            return self.nodelist_false.render(context)

        equal = self.is_active(request, var)

        if equal:
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)


class ActiveLinkEqualNode(ActiveLinkNodeBase):

    def is_active(self, request, path_to_check):
        return path_to_check == request.path


class ActiveLinkStartsWithNode(ActiveLinkNodeBase):

    def is_active(self, request, path_to_check):
        return request.path.startswith(path_to_check)


def parse(parser, token, end_tag):
    bits = token.split_contents()[1:2]
    var = TemplateIfParser(parser, bits).parse()
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()

    return var, nodelist_true, nodelist_false

@register.tag
def ifactive(parser, token):
    urlnode = url(parser, token)
    var, nodelist_true, nodelist_false = parse(parser, token, 'endifactive')
    return ActiveLinkEqualNode(urlnode, var, nodelist_true, nodelist_false)


@register.tag
def ifstartswith(parser, token):
    urlnode = url(parser, token)
    var, nodelist_true, nodelist_false = parse(parser, token, 'endifstartswith')
    return ActiveLinkStartsWithNode(urlnode, var, nodelist_true, nodelist_false)
