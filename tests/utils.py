import unittest

from nbo2graph.edge import Edge
from nbo2graph.node import Node


class Utils():

    """Class for testing functions."""

    tc = unittest.TestCase()

    @staticmethod
    def assert_are_almost_equal(a, b, places=5):

        """Deep asserts almost equality between two objects."""

        # assert equal data types
        Utils.tc.assertEqual(type(a), type(b))

        # check data type and call appropriate comparison function
        comparison_function = Utils.get_comparison_function(type(a))
        comparison_function(a, b, places=places)

    @staticmethod
    def base_assert_are_almost_equal(a, b, places=5):

        """Deep asserts almost equality between two items (can be multidim lists or objects)."""

        # check if not list
        if a is None or type(a) in [str, int, float, bool]:
            Utils.tc.assertAlmostEqual(a, b, places=places)
            # return a == b
        else:

            # check length
            Utils.tc.assertEqual(len(a), len(b))

            # recursively call
            for a_, b_ in zip(a, b):
                Utils.assert_are_almost_equal(a_, b_, places=places)

    @staticmethod
    def get_comparison_function(data_type):

        if data_type == Node:
            return Utils.node_assert_are_almost_equal
        elif data_type == Edge:
            return Utils.edge_assert_are_almost_equal
        else:
            return Utils.base_assert_are_almost_equal

    @staticmethod
    def edge_assert_are_almost_equal(a: Edge, b: Edge, places=5):

        """Equality operator for edge objects."""

        Utils.assert_are_almost_equal(a.features, b.features, places=places)
        Utils.assert_are_almost_equal(a.node_indices, b.node_indices, places=places)
        Utils.assert_are_almost_equal(a.is_directed, b.is_directed, places=places)

    @staticmethod
    def node_assert_are_almost_equal(a: Node, b: Node, places=5):

        """Equality operator for node objects."""

        Utils.assert_are_almost_equal(a.features, b.features, places=places)
        Utils.assert_are_almost_equal(a.position, b.position, places=places)
        Utils.assert_are_almost_equal(a.label, b.label, places=places)
