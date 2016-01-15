import django
from django import VERSION as DJANGO_VERSION
from django.conf import settings


# bootstrap django
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
    },
]

if DJANGO_VERSION[:2] >= (1, 9):
    TEMPLATES[0].update(
        {'OPTIONS': {'builtins': ['activelink.templatetags.activelink']}}
    )


settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    ROOT_URLCONF='activelink.tests.urls',
    INSTALLED_APPS=[
        'activelink',
        'activelink.tests',
    ],
    TEMPLATES=TEMPLATES
)

if DJANGO_VERSION >= (1, 7):
    django.setup()
