Template Tags
=============

Assets tag
----------

This tag simply marks where to output the asset tags.

.. code-block:: django

   {% assets %}

Asset tag
---------

Specifies an asset that is required for this page to function.

.. code-block:: django

   {% asset name ...deps... [mode=?] [alias=?] %}

The first positional argument is the filename or alias of an asset that is
required.

Additional positional arguments are names or aliases of assets this asset
requires to be included before it.

The ``mode`` keyword allows you to override which Processor this asset will be
assigned to. By default it will be assined to the Processor with the name
matching the assets file extension, mapped through ``DAMN_MODE_MAP``
