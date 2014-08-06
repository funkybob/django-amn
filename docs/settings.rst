Settings
========

DAMN_PROCESSORS
---------------

Default: {}

A map of Processor configs.

Each value is a dict of config values.  The only required option is 'processor', which is an import path for the class to use to process this asset type.

.. code-block:: python

   DAMN_PROCESSORS = {
       'js': {
           'processor': 'damn.processors.ScriptProcessor',
           'aliases': {
               'jquery': 'js/vendor/jquery-1.11.min.js',
               'jqplot': 'js/vendor/jqploy-0.9.min.js',
           },
           'deps': {
               'jqplot': ['jquery',],
           },
       },
   }

See :doc:`Processors <processors>` for more details.

DAMN_MODE_MAP
-------------

Default: {}

A map of file extensions to mode names.

In the absense of an entry here, or an explicit ``mode=`` attribute on the
asset tag, the asset will be assigned to a mode with the same name as its file
extension.

DAMN_MODE_ORDER
---------------

Default: ['css', 'js',]

A list of the order in which asset types should be rendered.

