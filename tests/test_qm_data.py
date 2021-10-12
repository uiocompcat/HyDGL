import unittest
from parameterized import parameterized

from nbo2graph.qm_data import QmData


class TestQmData(unittest.TestCase):

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
    def test_get_distance(self, a, b, expected):

        self.assertAlmostEqual(QmData._calculate_euclidean_distance(a, b), expected, places=5)

    @parameterized.expand([

        [
            [1, 2],
            [2, 4, 3],
            AssertionError
        ],

    ])
    def test_get_distance_with_invalid_input(self, a, b, expected_error):

        self.assertRaises(expected_error, QmData._calculate_euclidean_distance, a, b)
