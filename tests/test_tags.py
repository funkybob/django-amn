
from django.test import TestCase

from django.test.utils import setup_test_template_loader, override_settings
from django.template import Context
from django.template.loader import get_template

TEMPLATES = {
    'basetag': '''{% load damn %}{% assets %}''',
    'test_one': '''
{% load damn %}
{% assets %}
{% asset 'js/jquery.js' %}
''',
    'test_two': '''
{% load damn %}
{% assets %}
{% asset 'js/jquery.js' %}
{% asset 'js/knockout.js' %}
''',
    'test_three': '''
{% load damn %}
{% assets %}
{% asset 'js/knockout.js' 'js/jquery.js' %}
{% asset 'js/jquery.js' %}
''',
    'test_mixed': '''
{% load damn %}
{% assets %}
{% asset 'js/jquery.js' %}
{% asset 'css/bootstrap.css' %}
''',

    'test_alias': '''
{% load damn %}
{% assets %}
{% asset 'js/knockout.js' 'jquery' %}
{% asset 'js/jquery.js' alias='jquery' %}
''',
}

DEFAULT_SETTINGS = {
    'STATIC_URL': '/static/',

    'DAMN_PROCESSORS': {
        'js': {
            'processor': 'damn.processors.ScriptProcessor',
        },
        'css': {
            'processor': 'damn.processors.LinkProcessor',
            'type': 'text/css',
        },
    }

}

@override_settings(**DEFAULT_SETTINGS)
class TagTests(TestCase):

    @classmethod
    def setUpClass(self):
        setup_test_template_loader(TEMPLATES)

    def test_simple(self):
        t = get_template('basetag')
        t.render(Context())

    def test_one(self):
        t = get_template('test_one')
        o = t.render(Context())
        self.assertTrue('<script src="/static/js/jquery.js"></script>' in o)

    def test_two(self):
        t = get_template('test_two')
        o = t.render(Context())
        self.assertTrue('<script src="/static/js/jquery.js"></script>' in o)
        self.assertTrue('<script src="/static/js/knockout.js"></script>' in o)

    def test_three(self):
        t = get_template('test_three')
        o = t.render(Context())
        self.assertTrue('<script src="/static/js/jquery.js"></script>' in o)
        self.assertTrue('<script src="/static/js/knockout.js"></script>' in o)
        self.assertTrue(
            o.index('src="/static/js/jquery.js"') < o.index('src="/static/js/knockout.js"')
        )

    def test_mixed(self):
        t = get_template('test_mixed')
        o = t.render(Context())
        self.assertTrue('<script src="/static/js/jquery.js"></script>' in o)
        self.assertTrue('<link rel="stylesheet" type="text/css" href="/static/css/bootstrap.css">' in o)

    def test_alias(self):
        t = get_template('test_alias')
        o = t.render(Context())

        self.assertTrue('<script src="/static/js/jquery.js"></script>' in o)
        self.assertTrue('<script src="/static/js/knockout.js"></script>' in o)
        self.assertTrue(
            o.index('src="/static/js/jquery.js"') < o.index('src="/static/js/knockout.js"')
        )
