===============================
nbo2graph
===============================


.. image:: https://circleci.com/gh/hkneiding/nbo2graph.svg?style=svg&circle-token=dcb019393b2ff6c2e7afef3f326541f79366f256
    :target: https://circleci.com/gh/hkneiding/nbo2graph
.. image:: https://codecov.io/gh/hkneiding/nbo2graph/branch/main/graph/badge.svg?token=UB88TKUCY7
    :target: https://codecov.io/gh/hkneiding/nbo2graph


nbo2graph is a Python parser to generate descriptive graphs based on quantum chemistry data ready for use in Graph Neural Networks. In particular it provides the following features:

- adaptable generation of graph representations based on quantum chemistry data

    - connectivity based on NBO data or bond orders
    - features (both periodic table properties and quantum chemistry based)

- export of graphs as networkx objects or pytorch_geometric graphs

So far most graph representation learning approaches in quantum chemistry focus on organic molecules and build graphs based on geometry using basic features. For the accurate prediction of more complicated compounds (such as transition metal complexes) richer representations are required that include more of the relevant physics. This package provides the functionality to generate such graphs mainly based on Natural Bond Orbital (NBO) data and is the code associated with the paper `Deep Learning Metal Complex Properties with Natural Quantum Graphs`_.

.. _Deep Learning Metal Complex Properties with Natural Quantum Graphs: https://chemrxiv.org/engage/chemrxiv/article-details/62b8daaf7da6ce76b221a831 

The package can be used for any types of molecules but is aimed at transition metal complexes, more precisely the tmQM data set.

Requirements
-----------

- Python 3.7 or higher
- pytorch 1.9
- pytorch_geometric (pyg) 2.0
- plotly 5.0.0 or higher

How to use
-----------

After cloning this repository navigate into its root directory and run::
    python3 setup.py install

What is under the hood?
-----------

There are two main parts in the nbo2graph package. The first one is the GraphGenerator class that generates graphs based to specified parameters. Secondly there is the Graph class which represents a full graph in terms of nodes, edges, their respective features, graph-level features and attributes/labels. Furthemore, it includes functionality to produce object in a format ready to use with the pytorch_geometric package. The remaining classes are mainly miscellaneous helper classes and enums.\
This general structure is displayed by the following UML diagram.

.. image:: ./doc/uml.png


Difficulties?
-----------

If you encounter any problems, errors or bugs please do not hesitate to open an issue or directly contact me via mail (hanneskn@uio.no).
