from django.conf.urls.defaults import *
from django.http import HttpResponse


urlpatterns = patterns('',
    url(r'^test-url/$', lambda r: HttpResponse('ok'), name='test'),
    url(r'^test-url-with-arg/([-\w]+)/$', lambda r, arg: HttpResponse('ok'), name='test_with_arg'),
    url(r'^test-url-with-kwarg/(?P<arg>[-\w]+)/$', lambda r, arg: HttpResponse('ok'), name='test_with_kwarg'),
)
