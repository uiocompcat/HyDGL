import unittest
from parameterized import parameterized

from nbo2graph.tools import Tools


class TestTools(unittest.TestCase):

    @parameterized.expand([

        [
            2,
            0,
            [1, 0]
        ],

        [
            2,
            1,
            [0, 1]
        ],

        [
            5,
            2,
            [0, 0, 1, 0, 0]
        ],

    ])
    def test_get_one_hot_encoding(self, n_classes, class_number, expected):

        result = Tools.get_one_hot_encoding(n_classes, class_number)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [
            4,
            5,
            ValueError
        ],


        [
            3,
            3,
            ValueError
        ],

    ])
    def test_get_one_hot_encoding_with_invalid_input(self, n_classes, class_number, expected_error):

        self.assertRaises(expected_error, Tools.get_one_hot_encoding, n_classes, class_number)

    @parameterized.expand([

        [
            ['C1', 'C2', 'C2', 'C4', 'C4', 'C1', 'C1', 'C4', 'C1', 'C4', 'C10'],
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [1, 0, 0, 0],
                [1, 0, 0, 0],
                [0, 0, 1, 0],
                [1, 0, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ]
        ],

        [
            ['1', '2', '3'],
            [
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
            ]
        ],

    ])
    def test_get_one_hot_encoded_list(self, input_list, expected):

        result = Tools.get_one_hot_encoded_list(input_list)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [
            [
                [1.54, 'C'],
                [2.15, 'C'],
                [1.97, 'N'],
                [2.52, 'C']
            ],
            [
                [1.54, 1, 0],
                [2.15, 1, 0],
                [1.97, 0, 1],
                [2.52, 1, 0]
            ]
        ],

        [
            [
                [1, 'C', 'T'],
                [2, 'C', 'S'],
                [2, 'N', 'T'],
                [3, 'C', 'O']
            ],
            [
                [1, 1, 0, 1, 0, 0],
                [2, 1, 0, 0, 1, 0],
                [2, 0, 1, 1, 0, 0],
                [3, 1, 0, 0, 0, 1]
            ]
        ],

    ])
    def test_get_one_hot_encoding_for_string_list(self, input_list, expected):

        result = Tools.get_one_hot_encoded_feature_lists(input_list)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [
            [1, 2, 1, 2, 6, 2, 7],
            [1, 2, 1, 2, 6, 2, 7]
        ],

        [
            [1, [2, 1], [2, 6, 2], [7]],
            [1, 2, 1, 2, 6, 2, 7]
        ],

    ])
    def test_flatten_list(self, input_list, expected):

        result = Tools.flatten_list(input_list)

        self.assertEqual(result, expected)
