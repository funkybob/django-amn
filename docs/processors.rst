Processors
==========

The processor takes the list of assets and renders the output to the page.

As assets are defined in the page, the AssetRegister will assign them to
Processors, which it will in turn request to render them.

.. py:class:: Processor

   .. py:attribute:: aliases

      A map (dict) of aliases to filenames.

      This is useful for removing the need to, for instance, remember which
      version of jQuery your site is using.

   .. py:attribute:: deps

      A map of filenames or aliases to lists of other assets they depend on.

      Any use of these assets will automatically add the listed dependencies.

   .. py:method:: add_asset(filename, alias, deps)

      Add an asset to this ``Processor``.  This is used by the ``{% asset %}``
      tag.

   .. py:method:: resolve_deps()

      Return a list of filenames in an order which respects the declared
      dependencies.  All aliasese will be resolved at this point.

   .. py:method:: alias_map(name)

      Unalias a given resource name.

Out of the box there are two processors:  ScriptProcessor, and LinkProcessor.

ScriptProcessor
---------------

``ScriptProcessor`` will output each asset in a script tag, after resolving the
filename through staticfiles.

.. code-block:: html

   <script src="{% static filename %}"></script>


LinkProcessor
-------------

``LinkProcessor`` will output each asset as a link tag.  You can optionally
specify in the config the ``rel`` and ``type`` attributes to be used.

.. code-block:: html

   <link rel="{{ rel }}" type="{{ type }}" href="{% static filename %}">

.. py:class:: LinkProcessor

   .. py:attribute:: rel

      Default: 'stylesheet'

      The value to output for the rel attribute of the link element.

   .. py:attribute:: type

      Default: 'text/css'

      The value to output for the type attribute of the link element.

