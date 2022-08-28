Usage
=====

To generate graphs we need to setup a ``GraphGenerator`` object that operates based on a set of settings that correspond to a specific representation. The easiest way to do so is to use one of the implemented settings used in the `publication <>`_. In the example below we use the ``baseline`` representation. After the ``GraphGenerator`` is set up we can use it to generate graphs of molecules. For this we need to call the ``.generate_graph()`` function providing it with a dictionary of the relevant QM data. The required information and correct formatting of this dictionary is detailed in section <>.

.. code-block:: python
   :linenos:

    import nbo2graph as n2g

    # get the default settings for baseline graphs 
    ggs = n2g.GraphGeneratorSettings.baseline()
    # setup the graph generator with these settings
    gg = n2g.GraphGenerator(settings=ggs)
    # generate a graph according to these settings using a
    # dict of the relevant QM data of a specific molecule
    graph = gg.generate_graph(n2g.QmData.from_dict(qm_data_dict))


Aside from ``.baseline()`` there are also ``.uNatQ()`` ``.dNatQ()`` implemented.  Their exact specifications can be found in the `publication <>`_.

=================
Custom graph generator settings
=================

