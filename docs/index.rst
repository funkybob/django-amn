.. Django Assess Managed Nicely documentation master file, created by
   sphinx-quickstart on Sat Aug  2 14:22:59 2014.

Django Assess Managed Nicely
============================

Overview
--------

Yet another approach to handling static assets in your Django project.

Django-AMN helps you manage including assets in your templates without
requiring contortions to enable adding extra dependencies, only to have
duplicates appearing.

Simply add the ``{% assets %}`` tag where you want your assets listed, and then
use the ``{% asset %}`` tag to add a requirement.

Assets can have dependencies on other assets, so you can be sure they're
included, and in the right order.

Different asset types [css, js, less, etc] will be assigned to a different
``Processor``, which can handle how they're rendered into the template -
including compiling, translating, minifying, etc.

Each asset is assigned a mode (by default its file extension) which you can
override by specifying it in the tag:

.. code-block:: django

   {% asset 'thing/foo.html' mode='template' %}

Assets can have dependencies, so you won't forget to include what's needed.

.. code-block:: django

   {% asset 'js/knockout.js' 'js/jquery.js' %}

You can also pre-define asset dependencies in your settings.

To make life easier, any asset can have an alias.  Aliases can be assigned in
two ways; either in the tag, or in your settings.

.. code-block:: django

   {% asset 'js/jquery-1.11.min.js' alias='jquery' %}

Dependencies can refer to aliases, allowing library versions to be updated
without breaking your templates.

.. code-block:: django

   {% asset 'js/knockout.js' 'jquery' %}

If you've configured aliases in your settings, you can use them directly:

.. code-block:: django

   {% asset 'jqplot' %}

.. toctree::
   :maxdepth: 2

   settings
   tags
   processors
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

