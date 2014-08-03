django-amn
==========

Django Asset Management Nicely

Read the docs at http://django-assets-managed-nicely.readthedocs.org/en/latest/

Overview
========


Template:

    <!doctype html>{% load damn %}
    <html>
        <head>
        {% assets %}
        </head>
        <body>
        ...
        {% asset 'js/jquery.js' alias='jquery' %}
        # Depends on 'jquery'
        {% asset 'js/bootstrap.js' 'jquery' alias='bootstrap' %}
        </body>
    </html>

Output:

    <!doctype html>
    <html>
        <head>
            <script src='/static/js/jquery.js'></script>
            <script src='/static/js/bootstrap.js'></script>
        </head>
        <body>
        </body>
    </html>

But also, with the right processor you can concatenate, minify, etc, your files:

    <!doctype html>
    <html>
        <head>
            <script src='/static/built/jquery_js_bootstrap_js.min.js'></script>
        </head>
        <body>
        </body>
    </html>

