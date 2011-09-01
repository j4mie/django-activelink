from django.conf.urls.defaults import *
from django.http import HttpResponse


urlpatterns = patterns('',
    url(r'^test-url/$', lambda r: HttpResponse('ok'), name='test'),
)
