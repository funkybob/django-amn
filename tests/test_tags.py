
from unittest import TestCase
from django.test.utils import TestTemplateLoader, override_with_test_loader

TEMPLATES = TestTemplateLoader({
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
})

class TagTests(TestCase):

    @override_with_test_loader(TEMPLATES)
    def test_simple(self):
        t = get_template('basetag')
        t.render()

    @override_with_test_loader(TEMPLATES)
    def test_one(self):
        t = get_template('test2')
        o = t.render({})
        self.assertContains(o, '<script src="/static/js/jquery.js"></script>")

