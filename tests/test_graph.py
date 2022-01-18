import unittest
import torch
from torch_geometric.data import Data
from parameterized import parameterized

from nbo2graph.node import Node
from nbo2graph.edge import Edge
from nbo2graph.graph import Graph
from tests.utils import Utils


class TestGraph(unittest.TestCase):

    @parameterized.expand([

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0]), Edge([0, 2], features=[0]), Edge([0, 3], features=[0]), Edge([3, 2], features=[0]), Edge([2, 4], features=[0])]),
            True
        ],

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0]), Edge([0, 2], features=[0]), Edge([0, 3], features=[0]), Edge([3, 2], features=[0])]),
            False
        ],

    ])
    def test_is_connected(self, graph, expected):

        self.assertEqual(graph.is_connected(), expected)

    @parameterized.expand([

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0]), Edge([0, 2], features=[0]), Edge([0, 3], features=[0]), Edge([3, 2], features=[0]), Edge([2, 4], features=[0])]),
            [[0, 1, 2, 3, 4]]
        ],

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0]), Edge([0, 2], features=[0]), Edge([0, 3], features=[0]), Edge([3, 2], features=[0])]),
            [[0, 1, 2, 3], [4]]
        ],

    ])
    def test_get_disjoint_sub_graphs(self, graph, expected):

        self.assertEqual(graph.get_disjoint_sub_graphs(), expected)

    @parameterized.expand([

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0]), Edge([0, 2], features=[0]), Edge([0, 3], features=[0]), Edge([3, 2], features=[0]), Edge([2, 4], features=[0])]),
            0,
            [1, 2, 3]
        ],

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0]), Edge([0, 2], features=[0]), Edge([0, 3], features=[0]), Edge([3, 2], features=[0]), Edge([2, 4], features=[0])]),
            4,
            [2]
        ],

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0]), Edge([0, 2], features=[0]), Edge([0, 3], features=[0]), Edge([3, 2], features=[0])]),
            4,
            []
        ],

    ])
    def test_get_adjacent_nodes_with_valid_input(self, graph, node, expected):

        self.assertEqual(graph.get_adjacent_nodes(node), expected)

    @parameterized.expand([

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0]), Edge([0, 2], features=[0]), Edge([0, 3], features=[0]), Edge([3, 2], features=[0])]),
            -1
        ],

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0]), Edge([0, 2], features=[0]), Edge([0, 3], features=[0]), Edge([3, 2], features=[0])]),
            7
        ]
    ])
    def test_get_adjacent_nodes_with_invalid_input(self, graph, node):

        self.assertRaises(ValueError, graph.get_adjacent_nodes, node)

    @parameterized.expand([

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0], is_directed=True), Edge([0, 2], features=[0], is_directed=True), Edge([0, 3], features=[0], is_directed=True), Edge([3, 2], features=[0], is_directed=True), Edge([2, 4], features=[0], is_directed=True)]),
            0,
            []
        ],

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0], is_directed=True), Edge([0, 2], features=[0], is_directed=True), Edge([0, 3], features=[0], is_directed=True), Edge([3, 2], features=[0], is_directed=True), Edge([2, 4], features=[0], is_directed=True)]),
            4,
            [2]
        ],

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0], is_directed=True), Edge([0, 2], features=[0], is_directed=True), Edge([0, 3], features=[0], is_directed=True), Edge([3, 2], features=[0], is_directed=True), Edge([2, 4], features=[0], is_directed=True)]),
            2,
            [0, 3]
        ],

    ])
    def test_get_incoming_adjacent_nodes_with_valid_input(self, graph, node, expected):

        self.assertEqual(graph.get_incoming_adjacent_nodes(node), expected)

    @parameterized.expand([

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0], is_directed=True), Edge([0, 2], features=[0], is_directed=True), Edge([0, 3], features=[0], is_directed=True), Edge([3, 2], features=[0], is_directed=True), Edge([2, 4], features=[0], is_directed=True)]),
            0,
            [1, 2, 3]
        ],

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0], is_directed=True), Edge([0, 2], features=[0], is_directed=True), Edge([0, 3], features=[0], is_directed=True), Edge([3, 2], features=[0], is_directed=True), Edge([2, 4], features=[0], is_directed=True)]),
            4,
            []
        ],

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0], is_directed=True), Edge([0, 2], features=[0], is_directed=True), Edge([0, 3], features=[0], is_directed=True), Edge([3, 2], features=[0], is_directed=True), Edge([2, 4], features=[0], is_directed=True)]),
            2,
            [4]
        ],

    ])
    def test_get_outgoing_adjacent_nodes_with_valid_input(self, graph: Graph, node, expected):

        self.assertEqual(graph.get_outgoing_adjacent_nodes(node), expected)

    @parameterized.expand([

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0], is_directed=True), Edge([0, 2], features=[0], is_directed=False), Edge([0, 3], features=[0], is_directed=True), Edge([3, 2], features=[0], is_directed=True), Edge([2, 4], features=[0], is_directed=False)]),
            [
                [0, 0, 1, 0, 0],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 1, 1],
                [1, 0, 0, 0, 0],
                [0, 0, 1, 0, 0]
            ]
        ],

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0], is_directed=False), Edge([0, 2], features=[0], is_directed=True), Edge([0, 3], features=[0], is_directed=False), Edge([3, 2], features=[0], is_directed=True), Edge([2, 4], features=[0], is_directed=False)]),
            [
                [0, 1, 0, 1, 0],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 1, 1],
                [1, 0, 0, 0, 0],
                [0, 0, 1, 0, 0]
            ]
        ],

    ])
    def test_get_adjacency_matrix(self, graph: Graph, expected):

        self.assertEqual(graph.get_adjacency_matrix(), expected)

    @parameterized.expand([

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0], is_directed=True), Edge([0, 2], features=[0], is_directed=False), Edge([0, 3], features=[0], is_directed=True), Edge([3, 2], features=[0], is_directed=True), Edge([2, 4], features=[0], is_directed=False)]),
            [1.61803399, 0.0, 0.0, -0.61803399, -1.0]
        ],

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0], is_directed=False), Edge([0, 2], features=[0], is_directed=True), Edge([0, 3], features=[0], is_directed=False), Edge([3, 2], features=[0], is_directed=True), Edge([2, 4], features=[0], is_directed=False)]),
            [1.41421356, 1.0, 0.0, -1.0, -1.41421356]
        ],

    ])
    def test_get_spectrum(self, graph: Graph, expected):

        Utils.assert_are_almost_equal(graph.get_spectrum(), expected, places=7)

    @parameterized.expand([

        [
            Graph(
                [Node(features=[0]), Node(features=[1]), Node(features=[3]), Node(features=[-2]), Node(features=[0])],
                [Edge([0, 1], features=[-2]), Edge([0, 2], features=[3]), Edge([0, 3], features=[4]), Edge([2, 3], features=[1]), Edge([2, 4], features=[10])],
                targets=[12.34]
            ),
            Data(
                x=torch.tensor([[0], [1], [3], [-2], [0]], dtype=torch.float),
                edge_index=torch.tensor([[0, 0, 0, 2, 2, 1, 2, 3, 3, 4],
                                         [1, 2, 3, 3, 4, 0, 0, 0, 2, 2]], dtype=torch.long),
                edge_attr=torch.tensor([[-2], [3], [4], [1], [10], [-2], [3], [4], [1], [10]], dtype=torch.float),
                y=torch.tensor([12.34], dtype=torch.float)
            )
        ],
    ])
    def test_get_pytorch_data_object(self, graph, expected):

        result = graph.get_pytorch_data_object()

        self.assertEqual(len(result.keys), len(expected.keys))
        for key in result.keys:
            self.assertTrue(torch.equal(result[key], expected[key]))

        # self.assertTrue(torch.equal(result.x, expected.x))
        # self.assertTrue(torch.equal(result.edge_index, expected.edge_index))
        # self.assertTrue(torch.equal(result.edge_attr, expected.edge_attr))

    @parameterized.expand([

        [
            Graph([Node(features=[0], position=[0, 1]), Node(features=[0], position=[2, 3]), Node(features=[0], position=[4, 7]),
                   Node(features=[0], position=[9, 0]), Node(features=[0], position=[2, 1])], []),

            {
                0: [0, 1],
                1: [2, 3],
                2: [4, 7],
                3: [9, 0],
                4: [2, 1]
            }
        ],

    ])
    def test_get_node_position_dict(self, graph, expected):

        self.assertEqual(graph.get_node_position_dict(), expected)

    @parameterized.expand([

        [
            Graph([Node(features=[0], label='C'), Node(features=[0], label='H'), Node(features=[0], label='O'),
                   Node(features=[0], label='N'), Node(features=[0], label='S')], []),

            {
                0: 'C',
                1: 'H',
                2: 'O',
                3: 'N',
                4: 'S'
            }
        ],

    ])
    def test_get_node_label_dict(self, graph, expected):

        self.assertEqual(graph.get_node_label_dict(), expected)
