from django import VERSION as DJANGO_VERSION
from django.http import HttpResponse


if DJANGO_VERSION >= (1, 10):
    from django.conf.urls import url
elif DJANGO_VERSION >= (1, 6):
    from django.conf.urls import patterns, url
else:
    from django.conf.urls.defaults import patterns, url


urlpatterns = [
    url(r'^test-url/$', lambda r: HttpResponse('ok'), name='test'),
    url(r'^test-url-with-arg/([-\w]+)/$', lambda r, arg: HttpResponse('ok'), name='test_with_arg'),
    url(r'^test-url-with-kwarg/(?P<arg>[-\w]+)/$', lambda r, arg: HttpResponse('ok'), name='test_with_kwarg'),
]

if DJANGO_VERSION < (1, 10):
    urlpatterns = patterns('', *urlpatterns)
