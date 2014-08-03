.. Django Assess Managed Nicely documentation master file, created by
   sphinx-quickstart on Sat Aug  2 14:22:59 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Django Assess Managed Nicely
============================

Overview
--------

Yet another approach to handling static assets in your Django project.

Django-AMN helps you manage including assets in your templates without having
to have contortions to enable adding extra dependencies, only to have
duplicates appearing.

Simply add the ``{% assets %}`` tag where you want your assets listed, and then
use the ``{% asset %}`` tag to add a requirement.

Assets can have dependencies on other assets, so you can be sure they're
included, and in the right order.

Different asset types [css, js, less, etc] can be assigned to a different
``Processor``, which can handle how they're rendered into the template -
including compiling, translating, minifying, etc.

Each asset is assigned a mode, which by default is inferred by its file
extension.  You can override the mode of any file by specifying it in the tag:

.. code-block:: django

   {% asset 'thing/foo.html' mode='template' %}

Assets can have dependencies, so you won't forget to include what's needed.

.. code-block:: django

   {% asset 'js/knockout.js' 'js/jquery.js' %}

To make life easier, any asset can have an alias.  Aliases can be assigned in two ways:

- In the asset tag using ``alias=``

.. code-block:: django

   {% asset 'js/jquery-1.11.min.js' alias='jquery' %}

- In the Processor config. ( see below )

Dependencies can refer to aliases, allowing library versions to be updated without breaking your templates.

.. code-block:: django

   {% asset 'js/knockout.js' 'jquery' %}


.. toctree::

   settings
   tags
   processors

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

