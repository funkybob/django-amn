
#from unittest import TestCase
from django.test import TestCase

from django.test.utils import setup_test_template_loader, override_settings
from django.template import Context
from django.template.loader import get_template

TEMPLATES = {
    'basetag': '''{% load damn %}{% assets %}''',
    'test2': '''
<!doctype html>{% load damn %}
<html>
<head>
{% assets %}
</head>
<body>
{% asset 'js/jquery.js' %}
</body>
</html>
''',
}

DAMN_PROCESSORS = {
    'js': {
        'processor': 'damn.processors.ScriptProcessor',
    },
}

class TagTests(TestCase):

    def setUp(self):
        setup_test_template_loader(TEMPLATES)

    @override_settings(
        DAMN_PROCESSORS=DAMN_PROCESSORS,
        STATIC_URL = '/',
    )
    def test_simple(self):
        t = get_template('basetag')
        t.render()

    @override_settings(
        DAMN_PROCESSORS=DAMN_PROCESSORS,
        STATIC_URL = '/',
    )
    def test_one(self):
        t = get_template('test2')
        o = t.render(Context())
        self.assertTrue('<script src="/static/js/jquery.js"></script>' in o)

