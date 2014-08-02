
from django.test import TestCase

from django.test.utils import setup_test_template_loader, override_settings
from django.template import Context
from django.template.loader import get_template

TEMPLATES = {
    'basetag': '''{% load damn %}{% assets %}''',
    'test_one': '''
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
    'test_two': '''
<!doctype html>{% load damn %}
<html>
<head>
{% assets %}
</head>
<body>
{% asset 'js/jquery.js' %}
{% asset 'js/knockout.js' %}
</body>
</html>
''',
    'test_three': '''
<!doctype html>{% load damn %}
<html>
<head>
{% assets %}
</head>
<body>
{% asset 'js/knockout.js' 'js/jquery.js' %}
{% asset 'js/jquery.js' %}
</body>
</html>
''',
    'test_mixed': '''
{% load damn %}
<head>
{% assets %}
</head>
<body>
{% asset 'js/jquery.js' %}
{% asset 'css/bootstrap.css' %}
</body>
</html>
''',

}

DAMN_PROCESSORS = {
    'js': {
        'processor': 'damn.processors.ScriptProcessor',
    },
    'css': {
        'processor': 'damn.processors.LinkProcessor',
        'type': 'text/css',
    },
}

DEFAULT_SETTINGS = {
    'STATIC_URL': '/static/',
}

class TagTests(TestCase):

    @classmethod
    def setUpClass(self):
        setup_test_template_loader(TEMPLATES)

    @override_settings(
        DAMN_PROCESSORS=DAMN_PROCESSORS,
        **DEFAULT_SETTINGS
    )
    def test_simple(self):
        t = get_template('basetag')
        t.render(Context())

    @override_settings(
        DAMN_PROCESSORS=DAMN_PROCESSORS,
        **DEFAULT_SETTINGS
    )
    def test_one(self):
        t = get_template('test_one')
        o = t.render(Context())
        self.assertTrue('<script src="/static/js/jquery.js"></script>' in o)

    @override_settings(
        DAMN_PROCESSORS=DAMN_PROCESSORS,
        **DEFAULT_SETTINGS
    )
    def test_two(self):
        t = get_template('test_two')
        o = t.render(Context())
        self.assertTrue('<script src="/static/js/jquery.js"></script>' in o)
        self.assertTrue('<script src="/static/js/knockout.js"></script>' in o)

    @override_settings(
        DAMN_PROCESSORS=DAMN_PROCESSORS,
        **DEFAULT_SETTINGS
    )
    def test_three(self):
        t = get_template('test_three')
        print 'test three'
        o = t.render(Context())
        print o
        self.assertTrue('<script src="/static/js/jquery.js"></script>' in o)
        self.assertTrue('<script src="/static/js/knockout.js"></script>' in o)
        self.assertTrue(
            o.index('src="/static/js/jquery.js"') < o.index('src="/static/js/knockout.js"')
        )

    @override_settings(
        DAMN_PROCESSORS=DAMN_PROCESSORS,
        **DEFAULT_SETTINGS
    )
    def test_mixed(self):
        t = get_template('test_mixed')
        o = t.render(Context())
