import unittest
from parameterized import parameterized

from nbo2graph.enums.hydrogen_mode import HydrogenMode
from nbo2graph.enums.sopa_resolution_mode import SopaResolutionMode
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
                                   hydrogen_count_threshold=0.5,
                                   bond_threshold_metal=None,
                                   sopa_contribution_threshold=0.49,
                                   sopa_resolution_mode=SopaResolutionMode.AVERAGE)
        ],

        # [
        #     GraphGeneratorSettings.from_file('./tests/files/test.config'),
        #     GraphGeneratorSettings(node_features=[NodeFeature.ATOMIC_NUMBERS, NodeFeature.LMO_BOND_ORDER_TOTAL, NodeFeature.NATURAL_ELECTRON_CONFIGURATION_F, NodeFeature.LONE_PAIR_ENERGY_MIN_MAX_DIFFERENCE, NodeFeature.LONE_PAIR_MAX, NodeFeature.LONE_PAIRS_S, NodeFeature.LONE_VACANCIES_S],
        #                            edge_features=[EdgeFeature.NLMO_BOND_ORDER, EdgeFeature.BOND_ORBITAL_AVERAGE, EdgeFeature.BOND_ORBITAL_DATA_F, EdgeFeature.ANTIBOND_ENERGY_MIN_MAX_DIFFERENCE, EdgeFeature.ANTIBOND_ORBITAL_MIN, EdgeFeature.ANTIBOND_ORBITAL_AVERAGE],
        #                            graph_features=[GraphFeature.CHARGE],
        #                            targets=[QmTarget.POLARISABILITY, QmTarget.LOWEST_VIBRATIONAL_FREQUENCY],
        #                            bond_determination_mode=BondDeterminationMode.NLMO,
        #                            bond_threshold=0.123,
        #                            hydrogen_mode=HydrogenMode.OMIT,
        #                            hydrogen_count_threshold=0.456)
        # ],

    ])
    def test_graph_generator_settings_from_file(self, ggs, expected):
        self.assertEqual(ggs, expected)
