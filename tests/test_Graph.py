import unittest
from parameterized import parameterized

from nbo2graph.graph import Graph


class TestGraph(unittest.TestCase):

    @parameterized.expand([

        [
            Graph([[0], [0], [0], [0], [0]], [[[0, 1], [0]], [[0, 2], [0]], [[0, 3], [0]], [[3, 2], [0]], [[2, 4], [0]]]),
            True
        ],

        [
            Graph([[0], [0], [0], [0], [0]], [[[0, 1], [0]], [[0, 2], [0]], [[0, 3], [0]], [[3, 2], [0]]]),
            False
        ],

    ])
    def test_is_connected(self, graph, expected):

        self.assertEqual(graph.is_connected(), expected)

    @parameterized.expand([

        [
            Graph([[0], [0], [0], [0], [0]], [[[0, 1], [0]], [[0, 2], [0]], [[0, 3], [0]], [[3, 2], [0]], [[2, 4], [0]]]),
            [[0, 1, 2, 3, 4]]
        ],

        [
            Graph([[0], [0], [0], [0], [0]], [[[0, 1], [0]], [[0, 2], [0]], [[0, 3], [0]], [[3, 2], [0]]]),
            [[0, 1, 2, 3], [4]]
        ],

    ])
    def test_get_disjoint_sub_graphs(self, graph, expected):

        self.assertEqual(graph.get_disjoint_sub_graphs(), expected)

    @parameterized.expand([

        [
            Graph([[0], [0], [0], [0], [0]], [[[0, 1], [0]], [[0, 2], [0]], [[0, 3], [0]], [[3, 2], [0]], [[2, 4], [0]]]),
            0,
            [1, 2, 3]
        ],

        [
            Graph([[0], [0], [0], [0], [0]], [[[0, 1], [0]], [[0, 2], [0]], [[0, 3], [0]], [[3, 2], [0]], [[2, 4], [0]]]),
            4,
            [2]
        ],

        [
            Graph([[0], [0], [0], [0], [0]], [[[0, 1], [0]], [[0, 2], [0]], [[0, 3], [0]], [[3, 2], [0]]]),
            4,
            []
        ],

    ])
    def test_get_adjacent_nodes_with_valid_input(self, graph, node, expected):

        self.assertEqual(graph.get_adjacent_nodes(node), expected)

    @parameterized.expand([

        [
            Graph([[0], [0], [0], [0], [0]], [[[0, 1], [0]], [[0, 2], [0]], [[0, 3], [0]], [[3, 2], [0]], [[2, 4], [0]]]),
            -1
        ],

        [
            Graph([[0], [0], [0], [0], [0]], [[[0, 1], [0]], [[0, 2], [0]], [[0, 3], [0]], [[3, 2], [0]], [[2, 4], [0]]]),
            7
        ]
    ])
    def test_get_adjacent_nodes_with_invalid_input(self, graph, node):

        self.assertRaises(ValueError, graph.get_adjacent_nodes, node)
