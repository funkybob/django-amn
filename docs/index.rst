.. Django Assess Managed Nicely documentation master file, created by
   sphinx-quickstart on Sat Aug  2 14:22:59 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Django Assess Managed Nicely's documentation!
========================================================

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

Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

