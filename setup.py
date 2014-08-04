from distutils.core import setup


setup(
    name='django-amn',
    version='0.2.1',
    description='Django asset dependency management.',
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    keywords=['django', 'assets',],
    packages=[
        'damn',
        'damn.templatetags',
    ],
    zip_safe=False,
)

