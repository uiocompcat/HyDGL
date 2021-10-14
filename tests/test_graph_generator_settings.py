import unittest
from parameterized import parameterized

from nbo2graph.enums.node_feature import NodeFeature
from nbo2graph.enums.edge_feature import EdgeFeature
from nbo2graph.enums.graph_feature import GraphFeature
from nbo2graph.enums.qm_target import QmTarget
from nbo2graph.enums.hydrogen_mode import HydrogenMode
from nbo2graph.enums.bond_determination_mode import BondDeterminationMode
from nbo2graph.graph_generator_settings import GraphGeneratorSettings


class TestGraphGeneratorSettings(unittest.TestCase):

    @parameterized.expand([

        [
            GraphGeneratorSettings.default(),
            GraphGeneratorSettings(node_features=[],
                                   edge_features=[],
                                   graph_features=[],
                                   targets=[],
                                   bond_determination_mode=BondDeterminationMode.WIBERG,
                                   bond_threshold=0.3,
                                   hydrogen_mode=HydrogenMode.EXPLICIT,
                                   hydrogen_count_threshold=0.5)
        ],

        [
            GraphGeneratorSettings.from_file('./tests/files/test.config'),
            GraphGeneratorSettings(node_features=[NodeFeature.ATOMIC_NUMBERS, NodeFeature.NATURAL_ELECTRON_CONFIGURATION_F, NodeFeature.LONE_PAIRS_S, NodeFeature.LONE_VACANCIES_S],
                                   edge_features=[EdgeFeature.BOND_ORDER, EdgeFeature.BOND_ORBITAL_DATA_F],
                                   graph_features=[GraphFeature.CHARGE, GraphFeature.POLARISABILITY],
                                   targets=[QmTarget.LOWEST_VIBRATIONAL_FREQUENCY],
                                   bond_determination_mode=BondDeterminationMode.NLMO,
                                   bond_threshold=0.123,
                                   hydrogen_mode=HydrogenMode.OMIT,
                                   hydrogen_count_threshold=0.456)
        ],

    ])
    def test_graph_generator_settings_from_file(self, ggs, expected):
        self.assertEqual(ggs, expected)
