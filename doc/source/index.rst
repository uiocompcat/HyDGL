Welcome to the nbo2graph documentation!
===================================

`nbo2graph <https://github.com/hkneiding/nbo2graph>`_ is a Python library to generate descriptive graphs based on quantum chemistry data ready for use in Graph Neural Networks. In particular it provides the following features:

- adaptable generation of graph representations based on quantum chemistry data

    - connectivity based on NBO data or bond orders
    - features (both periodic table properties and quantum chemistry based)

- export of graphs as networkx objects or pytorch_geometric graphs

So far most graph representation learning approaches in quantum chemistry focus on organic molecules and build graphs based on geometry using basic features. For the accurate prediction of more complicated compounds (such as transition metal complexes) richer representations are required that include more of the relevant physics. This package provides the functionality to generate such graphs mainly based on Natural Bond Orbital (NBO) data and is the code associated with the paper `Deep Learning Metal Complex Properties with Natural Quantum Graphs <https://chemrxiv.org/engage/chemrxiv/article-details/62b8daaf7da6ce76b221a831>`_.

The package can be used for any types of molecules but is aimed at transition metal complexes, more precisely the tmQM data set.

.. note::

   This project is under active development. If you encounter any problems, errors or bugs please do not hesitate to open an issue or directly contact me via mail (hanneskn@uio.no).

Contents
--------

.. toctree::

   requirements
   installation
   usage
