import unittest
from parameterized import parameterized
import torch
from torch_geometric.data import Data

from nbo2graph.node import Node
from nbo2graph.edge import Edge
from nbo2graph.graph import Graph


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
