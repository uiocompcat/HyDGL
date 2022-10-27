import unittest
from parameterized import parameterized

from HyDGL.enums.hydrogen_mode import HydrogenMode
from HyDGL.enums.sopa_resolution_mode import SopaResolutionMode
from HyDGL.enums.bond_order_type import BondOrderType
from HyDGL.graph_generator_settings import GraphGeneratorSettings


class TestGraphGeneratorSettings(unittest.TestCase):

    @parameterized.expand([

        [
            GraphGeneratorSettings.default(),
            GraphGeneratorSettings(node_features=[],
                                   edge_features=[],
                                   sopa_edge_features=[],
                                   graph_features=[],
                                   targets=[],
                                   edge_types=[],
                                   bond_order_mode=BondOrderType.WIBERG,
                                   bond_threshold=0.3,
                                   hydrogen_mode=HydrogenMode.EXPLICIT,
                                   hydrogen_count_threshold=0.5,
                                   bond_threshold_metal=None,
                                   sopa_interaction_threshold=0,
                                   sopa_contribution_threshold=0.5,
                                   sopa_resolution_mode=SopaResolutionMode.AVERAGE,
                                   max_bond_distance=3.0)
        ],

        # [
        #     GraphGeneratorSettings.from_file('./tests/files/test.config'),
        #     GraphGeneratorSettings(node_features=[NodeFeature.ATOMIC_NUMBERS, NodeFeature.LMO_BOND_ORDER_TOTAL, NodeFeature.NATURAL_ELECTRON_CONFIGURATION_F_SYMMETRY, NodeFeature.LONE_PAIR_ENERGY_MIN_MAX_DIFFERENCE, NodeFeature.LONE_PAIR_MAX, NodeFeature.LONE_PAIRS_S, NodeFeature.LONE_VACANCIES_S],
        #                            edge_features=[EdgeFeature.NLMO_BOND_ORDER, EdgeFeature.BOND_ORBITAL_AVERAGE, EdgeFeature.BOND_ORBITAL_F_SYMMETRY, EdgeFeature.ANTIBOND_ENERGY_MIN_MAX_DIFFERENCE, EdgeFeature.ANTIBOND_ORBITAL_MIN, EdgeFeature.ANTIBOND_ORBITAL_AVERAGE],
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
