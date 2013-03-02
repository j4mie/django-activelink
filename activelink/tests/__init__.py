from django.conf import settings


# bootstrap django
settings.configure(
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    ROOT_URLCONF = 'activelink.tests.urls',
    INSTALLED_APPS=[
        'activelink',
        'activelink.tests',
    ],
    ACTIVE_LINK_CLASS = 'active',
    INACTIVE_LINK_CLASS = 'inactive'
)
