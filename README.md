# django-activelink

**django-activelink** is a Django template library for checking whether the current page matches a given URL. It is useful for highlighting active links in menus.

## Installation

You can install django-activelink from PyPI:

    pip install django-activelink

Add `activelink` to your `INSTALLED_APPS`:

    INSTALLED_APPS = (
        ...
        'activelink',
        ...
    )

Whenever you want to use django-activelink in a template, you need to load its template library:

    {% load activelink %}

**IMPORTANT**: django-activelink requires that the current request object is available in your template's context. This means you must be using a `RequestContext` when rendering your template, and `django.core.context_processors.request` must be in your `TEMPLATE_CONTEXT_PROCESSORS` setting. See [the documentation](https://docs.djangoproject.com/en/dev/ref/templates/api/#subclassing-context-requestcontext) for more information.

## Usage

Three template tags are provided: `ifactive`, `ifstartswith` and `ifcontains`. These take exactly the same arguments as the built-in `url` template tag. They check whether the URL provided matches the current request URL. This is easiest to explain with an example:

    <a href="{% url "myurl" %}" class="{% ifactive "myurl" %}on{% else %}off{% endifactive %}">Menu item</a>

You can also pass a literal URL rather than a URL name:

    <a href="/myurl/" class="{% ifactive "/myurl/" %}on{% else %}off{% endifactive %}">Menu item</a>

The `ifstartswith` tag checks whether the *beginning* of the current URL matches. This is useful for top-level menu items with submenus attached.

The `ifcontains` tag checks that the current URL contains the searched part.

**Note:** Django 1.3 started the process of gradually deprecating the existing `url` template tag and replacing it with a new one, which requires literal string arguments to be quoted. See [the release notes](https://docs.djangoproject.com/en/dev/releases/1.3/#changes-to-url-and-ssi) for more information. To be forwards-compatible, django-activelink *only* supports the new version of the syntax. You can still use it in templates using the old version, but you have to remember to quote your strings properly.

## Development

To contribute, fork the repository, make your changes, add some tests, commit, push, and open a pull request.

### How to run the tests

This project is tested with [nose](http://nose.readthedocs.org). Clone the repository, then run `pip install -r test-requirements.txt` to install nose and Django into your virtualenv. Then, simply type `nosetests` to find and run all the tests.

## (Un)license

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this
software, either in source code form or as a compiled binary, for any purpose,
commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this
software dedicate any and all copyright interest in the software to the public
domain. We make this dedication for the benefit of the public at large and to
the detriment of our heirs and successors. We intend this dedication to be an
overt act of relinquishment in perpetuity of all present and future rights to
this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
