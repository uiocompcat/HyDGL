import unittest
from parameterized import parameterized

from tests.utils import Utils
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

    @parameterized.expand([

        [
            {'a': 1, 'b': 0.2, 'c': 'class', 'd': 1.154, 'e': 0},
            ['c']
        ],

        [
            {'a': 1, 'b': 0.2, 'c': 12, 'd': 1.154, 'e': 0},
            []
        ],

    ])
    def test_get_class_feature_keys(self, feature_dict, expected):

        result = Tools.get_class_feature_keys(feature_dict)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [
            [1.5, 'A', 5, 7.123, 7., 'fC', 53, 1.21],
            [1, 5]
        ],

    ])
    def test_get_class_feature_indices(self, feature_list, expected):

        result = Tools.get_class_feature_indices(feature_list)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [
            {'feature_a': 1.5, 'feature_b': 'A', 'feature_c': 5, 'feature_d': 7.123, 'feature_e': 'fC'},
            {'feature_b': ['A', 'B', 'C'], 'feature_e': ['gC', 'fC', 'dC']},
            {'feature_a': 1.5, 'feature_b': [1, 0, 0], 'feature_c': 5, 'feature_d': 7.123, 'feature_e': [0, 1, 0]}
        ],

        [
            {'feature_a': 1.5, 'feature_b': 'A', 'feature_c': 5, 'feature_d': 7.123, 'feature_e': 'fC'},
            {'feature_b': ['A'], 'feature_e': ['gC', 'dC', 'fC']},
            {'feature_a': 1.5, 'feature_b': [], 'feature_c': 5, 'feature_d': 7.123, 'feature_e': [0, 0, 1]}
        ],

        [
            {'feature_a': 1.5, 'feature_c': 5, 'feature_d': 7.123, 'feature_e': 1.21},
            {},
            {'feature_a': 1.5, 'feature_c': 5, 'feature_d': 7.123, 'feature_e': 1.21},
        ],

    ])
    def test_get_one_hot_encoded_feature_dict(self, feature_list, class_feature_dict, expected):

        result = Tools.get_one_hot_encoded_feature_dict(feature_list, class_feature_dict)
        print(result)
        Utils.assert_are_almost_equal(result, expected)

    @parameterized.expand([

        [
            {'feature_a': 1.5, 'feature_b': 'A', 'feature_c': 5, 'feature_d': 7.123, 'feature_e': 'fC'},
            {'feature_b': ['A', 'B', 'C'], 'feature_e': ['gC', 'fC', 'dC']},
            [1.5, 1, 0, 0, 5, 7.123, 0, 1, 0]
        ],

        [
            {'feature_a': 1.5, 'feature_b': 'A', 'feature_c': 5, 'feature_d': 7.123, 'feature_e': 'fC'},
            {'feature_b': ['A'], 'feature_e': ['gC', 'dC', 'fC']},
            [1.5, 5, 7.123, 0, 0, 1]
        ],

        [
            {'feature_a': 1.5, 'feature_c': 5, 'feature_d': 7.123, 'feature_e': 1.21},
            {},
            [1.5, 5, 7.123, 1.21]
        ],

    ])
    def test_get_one_hot_encoded_feature_list(self, feature_list, class_feature_dict, expected):

        result = Tools.get_one_hot_encoded_feature_list(feature_list, class_feature_dict)
        print(result)
        Utils.assert_are_almost_equal(result, expected)

    @parameterized.expand([

        [
            [1],
            [1.9],
            0.9
        ],

        [
            [1, 2],
            [2, 4],
            2.236068
        ],

        [
            [5, 8, 10],
            [0.5, 90, 13],
            82.17816
        ],

    ])
    def test_calculate_euclidean_distance(self, a, b, expected):

        self.assertAlmostEqual(Tools.calculate_euclidean_distance(a, b), expected, places=5)

    @parameterized.expand([

        [
            [1, 2],
            [2, 4, 3],
            AssertionError
        ],

    ])
    def test_calculate_euclidean_distance_with_invalid_input(self, a, b, expected_error):

        self.assertRaises(expected_error, Tools.calculate_euclidean_distance, a, b)

    @parameterized.expand([

        [
            [[1, 2], [2, 3], [5, 1]],
            [
                [0, 1.414214, 4.123106],
                [1.414214, 0, 3.605551],
                [4.123106, 3.605551, 0]
            ]
        ]

    ])
    def test_calculate_distance_matrix(self, points, expected):

        Utils.assert_are_almost_equal(Tools.calculate_distance_matrix(points), expected)

    @parameterized.expand([

        [
            [[1, 2], [2, 3], [5, 1, 2]],
            AssertionError
        ],

    ])
    def test_calculate_distance_matrix_with_invalid_input(self, points, expected_error):

        self.assertRaises(expected_error, Tools.calculate_distance_matrix, points)

    @parameterized.expand([

        [
            2,
            2,
            4,
            0.0
        ],

        [
            3,
            2,
            4,
            0.5
        ],

        [
            4.27,
            3.14,
            10.99,
            0.14394904459
        ],

        [
            'test',
            3.14,
            10.99,
            'test'
        ],

    ])
    def test_min_max_scale(self, value, min_value, max_value, expected):

        Utils.assert_are_almost_equal(Tools.min_max_scale(value, min_value, max_value), expected)

    @parameterized.expand([

        [
            1,
            2,
            4,
            ValueError
        ],

        [
            5,
            2,
            4,
            ValueError
        ],
    ])
    def test_min_max_scale_with_invalid_input(self, value, min_value, max_value, expected_error):

        self.assertRaises(expected_error, Tools.min_max_scale, value, min_value, max_value)
