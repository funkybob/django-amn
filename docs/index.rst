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

Each asset is assigned a mode, which by default is inferred by its file
extension.  You can override the mode of any file by specifying it in the tag:

.. code-block:: django

   {% asset 'thing/foo.html' mode='template' %}

Assets can have dependencies, so you won't forget to include what's needed.

.. code-block:: django

   {% asset 'js/knockout.js' 'js/jquery.js' %}

To make life easier, any asset can have an alias.  Aliases can be assigned in two ways:

- In the asset tag using ``alias=``
- In the Processor config.

Dependencies can refer to aliases, allowing library versions to be updated without breaking your templates.

.. code-block:: django

   {% asset 'js/knockout.js' 'jquery' %}


Settings
--------

DAMN_PROCESSORS

A map of Processor configs.

Each value is a dict of config values.  The only required option is 'processor', which is an import path for the class to use to process this asset type.

.. code-block:: python

   DAMN_PROCESSORS = {
       'js': {
           'processor': 'damn.processors.ScriptProcessor',
           'aliases': {
               'jquery': 'js/vendor/jquery-1.11.min.js',
           }
       },
   }

Assets tag
----------

This tag simply marks where to output the asset tags.

TODO::

  Allow control of which modes are output...?

Asset tag
---------

Specifies an asset that is required for this page to function.

.. code-block:: django

   {% asset name ...deps... [mode=?] [alias=?] %}


Processors
----------

The processor takes the list of assets and renders the output to the page.

It will be assigned the list of assets, and then have render() called upon it to return a list of elements to be entered into the page.

Out of the box there are two processors:  ScriptProcessor, and LinkProcessor.

ScriptProcessor will output each asset in a script tag.

LinkProcessor will output each asset as a link tag.  You can optionally specify in the config the ``rel`` and ``type`` attributes to be used.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

