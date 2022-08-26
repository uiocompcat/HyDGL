Requirements
=====

This package is developed and tested on a Python 3.9.x version but any higher version should also work without any problems. The package requires installations of the following packages:

- (`numpy <https://numpy.org/>`_)
- (`networkx <https://networkx.org/>`_)
- `pytorch <https://pytorch.org/>`_
- `pytorch_geometric <https://www.pyg.org/>`_
- `plotly <https://plotly.com/python/>`_

.. note::

   Both ``numpy`` and ``networkx`` are dependencies of ``pytorch`` and ``pytorch_geometric`` and will be automatically installed during the installation of these packages.

The packages should be installed in the order they are listed. Make sure to use a ``pytorch`` version that is supported by ``pytorch_geometric``. You can check the supported versions `here <https://pytorch-geometric.readthedocs.io/en/latest/notes/installation.html>`_.

.. tip::

   When installing ``pytorch`` and ``pytorch_geometric`` for GPU use, pay attention to the versions as some GPUs are only supported by specific versions.

