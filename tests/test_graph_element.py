import unittest
from parameterized import parameterized

from tests.utils import Utils
from HyDGL.graph_element import GraphElement


class TestGraphGeneratorSettings(unittest.TestCase):

    @parameterized.expand([

        [
            GraphElement(
                features={
                    'feature_0': 0,
                    'feature_1': 1,
                    'feature_2': 'str'
                }
            ),
            {
                'feature_0': 0,
                'feature_1': 1,
                'feature_2': 'str'
            }
        ],

    ])
    def test_graph_element_features(self, graph_element, expected):

        Utils.assert_are_almost_equal(graph_element.features, expected)

    @parameterized.expand([

        [
            GraphElement(
                features={
                    'feature_0': 0,
                    'feature_1': 1,
                    'feature_2': 'str'
                }
            ),
            [0, 1, 'str']
        ],

    ])
    def test_graph_element_feature_list(self, graph_element, expected):

        Utils.assert_are_almost_equal(graph_element.feature_list, expected)

    @parameterized.expand([

        [
            GraphElement(
                features={
                    'feature_0': 0,
                    'feature_1': 1,
                    'feature_2': 'str'
                }
            ),
            {'feature_2': ['str', 'int', 'float']},
            [0, 1, 1, 0, 0]
        ],

    ])
    def test_get_one_hot_encoded_feature_list(self, graph_element, class_feature_dict, expected):

        Utils.assert_are_almost_equal(graph_element.get_one_hot_encoded_feature_list(class_feature_dict), expected)
