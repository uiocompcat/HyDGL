===============================
nbo2graph
===============================


.. image:: https://circleci.com/gh/hkneiding/nbo2graph.svg?style=svg&circle-token=dcb019393b2ff6c2e7afef3f326541f79366f256
    :target: https://circleci.com/gh/hkneiding/nbo2graph
.. image:: https://codecov.io/gh/hkneiding/nbo2graph/branch/main/graph/badge.svg?token=UB88TKUCY7
    :target: https://codecov.io/gh/hkneiding/nbo2graph


nbo2graph is a Python parser to generate descriptive graphs from Natural Bond Orbital data ready for use in Graph Neural Networks. In particular it provides the following features:

- parsing of Gaussian data files
- adaptable generation of graph representations (features and labels can be adapted to ones needs)
- export graphs in pytorch_geometric format
- easy-to-use interface

The package can be used for any types of molecules but is aimed at transition metal complexes, more precisely for the tmQM data set.

How to use
-----------

Requirements
-----------

- Python 3.7 or higher
- pytorch 1.9
- pytorch_geometric (pyg) 2.0

What is under the hood?
-----------

There are three main parts in the nbo2graph package. The first is the DataParser class which extracts relevant QM data from Gaussian files. The second one is the GraphGenerator class that generates graphs based to specified parameters. Finally there is the Graph class which represents a full graph in terms of nodes, edges, their respective features, graph-level features and attributes/labels. Furthemore, it includes functionality to produce object in a format ready to use with the pytorch_geometric package. The remaining classes are mainly miscellaneous helper classes and enums.\
This general structure is displayed by the following UML diagram.

.. image:: ./doc/uml.png
