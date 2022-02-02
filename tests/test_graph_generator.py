import unittest
from parameterized import parameterized
from nbo2graph.file_handler import FileHandler

from nbo2graph.node import Node
from nbo2graph.edge import Edge
from nbo2graph.enums.edge_feature import EdgeFeature
from nbo2graph.enums.node_feature import NodeFeature
from nbo2graph.enums.graph_feature import GraphFeature
from nbo2graph.enums.hydrogen_mode import HydrogenMode
from nbo2graph.enums.qm_target import QmTarget
from nbo2graph.graph_generator import GraphGenerator
from nbo2graph.enums.bond_order_type import BondOrderType
from nbo2graph.enums.edge_type import EdgeType
from nbo2graph.graph_generator_settings import GraphGeneratorSettings
from nbo2graph.enums.orbital_occupation_type import OrbitalOccupationType
from nbo2graph.enums.sopa_edge_feature import SopaEdgeFeature
from nbo2graph.enums.sopa_resolution_mode import SopaResolutionMode
from nbo2graph.qm_data import QmData
from tests.utils import Utils, TEST_FILE_LALMER, TEST_FILE_OREDIA, TEST_FILE_ZUYHEG


class TestGraphGenerator(unittest.TestCase):

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            HydrogenMode.EXPLICIT,
            BondOrderType.WIBERG,
            [NodeFeature.ATOMIC_NUMBER],
            [
                Node(features=[48]),
                Node(features=[8]),
                Node(features=[7]),
                Node(features=[6]),
                Node(features=[16]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[7]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[7]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[7]),
                Node(features=[6]),
                Node(features=[16]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[17]),
                Node(features=[8]),
                Node(features=[8]),
                Node(features=[8]),
                Node(features=[8]),
                Node(features=[1]),
                Node(features=[1]),
                Node(features=[1]),
                Node(features=[1]),
                Node(features=[1]),
                Node(features=[1]),
                Node(features=[1]),
                Node(features=[1]),
                Node(features=[1]),
                Node(features=[1]),
                Node(features=[1]),
                Node(features=[1]),
                Node(features=[1]),
                Node(features=[1]),
                Node(features=[1]),
                Node(features=[1])
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.OMIT,
            BondOrderType.WIBERG,
            [NodeFeature.ATOMIC_NUMBER],
            [
                Node(features=[48]),
                Node(features=[8]),
                Node(features=[7]),
                Node(features=[6]),
                Node(features=[16]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[7]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[7]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[7]),
                Node(features=[6]),
                Node(features=[16]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[17]),
                Node(features=[8]),
                Node(features=[8]),
                Node(features=[8]),
                Node(features=[8])
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.IMPLICIT,
            BondOrderType.WIBERG,
            [NodeFeature.ATOMIC_NUMBER],
            [
                Node(features=[48, 0]),
                Node(features=[8, 2]),
                Node(features=[7, 0]),
                Node(features=[6, 0]),
                Node(features=[16, 0]),
                Node(features=[6, 1]),
                Node(features=[6, 0]),
                Node(features=[6, 3]),
                Node(features=[7, 0]),
                Node(features=[6, 0]),
                Node(features=[6, 1]),
                Node(features=[6, 1]),
                Node(features=[6, 1]),
                Node(features=[6, 0]),
                Node(features=[7, 0]),
                Node(features=[6, 0]),
                Node(features=[6, 1]),
                Node(features=[6, 1]),
                Node(features=[6, 1]),
                Node(features=[6, 0]),
                Node(features=[7, 0]),
                Node(features=[6, 0]),
                Node(features=[16, 0]),
                Node(features=[6, 1]),
                Node(features=[6, 0]),
                Node(features=[6, 3]),
                Node(features=[17, 0]),
                Node(features=[8, 0]),
                Node(features=[8, 0]),
                Node(features=[8, 0]),
                Node(features=[8, 0])
            ]
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            BondOrderType.WIBERG,
            [NodeFeature.ATOMIC_NUMBER],
            [
                Node(features=[77]),
                Node(features=[1]),
                Node(features=[7]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[7]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[8]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[8]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[8]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[6]),
                Node(features=[8]),
                Node(features=[6]),
                Node(features=[6])
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.EXPLICIT,
            BondOrderType.WIBERG,
            [NodeFeature.WIBERG_BOND_ORDER_TOTAL],
            [
                Node(features=[0.5922]),
                Node(features=[1.5640]),
                Node(features=[3.1352]),
                Node(features=[4.0037]),
                Node(features=[2.7551]),
                Node(features=[3.9207]),
                Node(features=[3.9888]),
                Node(features=[3.8371]),
                Node(features=[3.1270]),
                Node(features=[3.9977]),
                Node(features=[3.9509]),
                Node(features=[3.9440]),
                Node(features=[3.9536]),
                Node(features=[3.9935]),
                Node(features=[3.1278]),
                Node(features=[3.9975]),
                Node(features=[3.9509]),
                Node(features=[3.9445]),
                Node(features=[3.9542]),
                Node(features=[3.9953]),
                Node(features=[3.1300]),
                Node(features=[4.0056]),
                Node(features=[2.7623]),
                Node(features=[3.9225]),
                Node(features=[3.9905]),
                Node(features=[3.8393]),
                Node(features=[4.5847]),
                Node(features=[1.4772]),
                Node(features=[1.5452]),
                Node(features=[1.7228]),
                Node(features=[1.7681]),
                Node(features=[0.7499]),
                Node(features=[0.9248]),
                Node(features=[0.7511]),
                Node(features=[0.9401]),
                Node(features=[0.9277]),
                Node(features=[0.9395]),
                Node(features=[0.9432]),
                Node(features=[0.9423]),
                Node(features=[0.9257]),
                Node(features=[0.9439]),
                Node(features=[0.9392]),
                Node(features=[0.9400]),
                Node(features=[0.9473]),
                Node(features=[0.9272]),
                Node(features=[0.9445]),
                Node(features=[0.9420])
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.EXPLICIT,
            BondOrderType.NLMO,
            [NodeFeature.NLMO_BOND_ORDER_TOTAL],
            [
                Node(features=[0.5744]),
                Node(features=[1.022]),
                Node(features=[2.2828]),
                Node(features=[3.3946]),
                Node(features=[1.9874]),
                Node(features=[3.3227]),
                Node(features=[3.5845]),
                Node(features=[3.1819]),
                Node(features=[2.2794]),
                Node(features=[3.5223]),
                Node(features=[3.5658]),
                Node(features=[3.7724]),
                Node(features=[3.5903]),
                Node(features=[3.7262]),
                Node(features=[2.2683]),
                Node(features=[3.532]),
                Node(features=[3.5804]),
                Node(features=[3.7722]),
                Node(features=[3.5926]),
                Node(features=[3.7325]),
                Node(features=[2.27]),
                Node(features=[3.3969]),
                Node(features=[1.993]),
                Node(features=[3.3239]),
                Node(features=[3.5949]),
                Node(features=[3.1929]),
                Node(features=[4.1104]),
                Node(features=[0.7012]),
                Node(features=[0.7221]),
                Node(features=[0.7784]),
                Node(features=[0.8416]),
                Node(features=[0.498]),
                Node(features=[0.7029]),
                Node(features=[0.4975]),
                Node(features=[0.755]),
                Node(features=[0.7378]),
                Node(features=[0.744]),
                Node(features=[0.7555]),
                Node(features=[0.7705]),
                Node(features=[0.7003]),
                Node(features=[0.7588]),
                Node(features=[0.7436]),
                Node(features=[0.7536]),
                Node(features=[0.7619]),
                Node(features=[0.735]),
                Node(features=[0.7559]),
                Node(features=[0.7702])
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.EXPLICIT,
            BondOrderType.WIBERG,
            [NodeFeature.NATURAL_ATOMIC_CHARGE],
            [
                Node(features=[1.68876]),
                Node(features=[-0.97287]),
                Node(features=[-0.5208]),
                Node(features=[-0.00055]),
                Node(features=[0.50384]),
                Node(features=[-0.42569]),
                Node(features=[0.16518]),
                Node(features=[-0.67147]),
                Node(features=[-0.49808]),
                Node(features=[0.15474]),
                Node(features=[-0.20643]),
                Node(features=[-0.14183]),
                Node(features=[-0.20915]),
                Node(features=[0.18]),
                Node(features=[-0.49346]),
                Node(features=[0.16092]),
                Node(features=[-0.20272]),
                Node(features=[-0.14315]),
                Node(features=[-0.20931]),
                Node(features=[0.17315]),
                Node(features=[-0.52989]),
                Node(features=[0.00237]),
                Node(features=[0.50834]),
                Node(features=[-0.42223]),
                Node(features=[0.1705]),
                Node(features=[-0.67088]),
                Node(features=[2.36189]),
                Node(features=[-0.9251]),
                Node(features=[-0.87318]),
                Node(features=[-0.75172]),
                Node(features=[-0.7181]),
                Node(features=[0.50206]),
                Node(features=[0.27661]),
                Node(features=[0.50076]),
                Node(features=[0.24647]),
                Node(features=[0.27044]),
                Node(features=[0.24758]),
                Node(features=[0.24012]),
                Node(features=[0.24114]),
                Node(features=[0.27532]),
                Node(features=[0.23865]),
                Node(features=[0.2482]),
                Node(features=[0.24659]),
                Node(features=[0.23192]),
                Node(features=[0.27127]),
                Node(features=[0.23798]),
                Node(features=[0.24182])
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.EXPLICIT,
            BondOrderType.WIBERG,
            [NodeFeature.NATURAL_ELECTRON_CONFIGURATION_S, NodeFeature.NATURAL_ELECTRON_CONFIGURATION_P, NodeFeature.NATURAL_ELECTRON_CONFIGURATION_D, NodeFeature.NATURAL_ELECTRON_CONFIGURATION_F],
            [
                Node(features=[0.31, 0.01, 9.98, 0.0]),
                Node(features=[1.75, 5.21, 0.01, 0.0]),
                Node(features=[1.37, 4.13, 0.01, 0.0]),
                Node(features=[0.97, 3.01, 0.01, 0.0]),
                Node(features=[1.65, 3.82, 0.03, 0.0]),
                Node(features=[1.10, 3.32, 0.01, 0.0]),
                Node(features=[0.91, 2.92, 0.0, 0.0]),
                Node(features=[1.13, 3.53, 0.01, 0.0]),
                Node(features=[1.34, 4.14, 0.01, 0.0]),
                Node(features=[0.89, 2.94, 0.0, 0.0]),
                Node(features=[1.00, 3.2, 0.0, 0.0]),
                Node(features=[1.00, 3.13, 0.0, 0.0]),
                Node(features=[1.00, 3.2, 0.0, 0.0]),
                Node(features=[0.89, 2.91, 0.0, 0.0]),
                Node(features=[1.34, 4.13, 0.01, 0.0]),
                Node(features=[0.89, 2.94, 0.0, 0.0]),
                Node(features=[1.00, 3.2, 0.0, 0.0]),
                Node(features=[1.00, 3.13, 0.0, 0.0]),
                Node(features=[1.00, 3.2, 0.0, 0.0]),
                Node(features=[0.89, 2.92, 0.0, 0.0]),
                Node(features=[1.37, 4.14, 0.02, 0.0]),
                Node(features=[0.96, 3.01, 0.01, 0.0]),
                Node(features=[1.65, 3.82, 0.03, 0.0]),
                Node(features=[1.10, 3.31, 0.01, 0.0]),
                Node(features=[0.91, 2.91, 0.0, 0.0]),
                Node(features=[1.13, 3.53, 0.01, 0.0]),
                Node(features=[1.25, 3.08, 0.3, 0.01]),
                Node(features=[1.89, 5.01, 0.02, 0.0]),
                Node(features=[1.89, 4.96, 0.02, 0.0]),
                Node(features=[1.87, 4.85, 0.02, 0.0]),
                Node(features=[1.87, 4.82, 0.02, 0.0]),
                Node(features=[0.5, 0.0, 0.0, 0.0]),
                Node(features=[0.72, 0.0, 0.0, 0.0]),
                Node(features=[0.5, 0.0, 0.0, 0.0]),
                Node(features=[0.75, 0.0, 0.0, 0.0]),
                Node(features=[0.73, 0.0, 0.0, 0.0]),
                Node(features=[0.75, 0.0, 0.0, 0.0]),
                Node(features=[0.76, 0.0, 0.0, 0.0]),
                Node(features=[0.76, 0.0, 0.0, 0.0]),
                Node(features=[0.72, 0.0, 0.0, 0.0]),
                Node(features=[0.76, 0.0, 0.0, 0.0]),
                Node(features=[0.75, 0.0, 0.0, 0.0]),
                Node(features=[0.75, 0.0, 0.0, 0.0]),
                Node(features=[0.77, 0.0, 0.0, 0.0]),
                Node(features=[0.73, 0.0, 0.0, 0.0]),
                Node(features=[0.76, 0.0, 0.0, 0.0]),
                Node(features=[0.76, 0.0, 0.0, 0.0])
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.OMIT,
            BondOrderType.WIBERG,
            [NodeFeature.LONE_PAIR_MAX, NodeFeature.LONE_PAIR_S, NodeFeature.LONE_PAIR_P, NodeFeature.LONE_PAIR_D, NodeFeature.LONE_PAIR_F],
            [
                Node(features=[5, -0.62573, 1.99593, 0.0001, 0.0, 0.9998, 0.0]),
                Node(features=[2, -0.56001, 1.99619, 0.1619, 0.8369, 0.0011, 0.0]),
                Node(features=[1, -0.50043, 1.86184, 0.3127, 0.6867, 0.0005, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[2, -0.37741, 1.55738, 0.0, 0.9979, 0.002, 0.0001]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[1, -0.48921, 1.87884, 0.2791, 0.7203, 0.0005, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[1, -0.48483, 1.87975, 0.2796, 0.7198, 0.0006, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[1, -0.49310, 1.86490, 0.3133, 0.6860, 0.0006, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[2, -0.36939, 1.55195, 0.0001, 0.9978, 0.002, 0.0001]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[3, -0.41714, 1.88616, 0.0003, 0.9976, 0.002, 0.0001]),
                Node(features=[3, -0.4117, 1.86643, 0.0002, 0.9972, 0.0025, 0.0001]),
                Node(features=[3, -0.4003, 1.79398, 0.0, 0.9964, 0.0035, 0.0001]),
                Node(features=[3, -0.39761, 1.77785, 0.0, 0.9961, 0.0038, 0.0001])
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.OMIT,
            BondOrderType.WIBERG,
            [NodeFeature.LONE_PAIR_AVERAGE, NodeFeature.LONE_PAIR_S, NodeFeature.LONE_PAIR_P, NodeFeature.LONE_PAIR_D, NodeFeature.LONE_PAIR_F],
            [
                Node(features=[5, -0.627936, 1.996892, 0.00014, 0.0, 0.99984, 0.0]),
                Node(features=[2, -0.61476, 1.9834, 0.26065, 0.73855, 0.00075, 0.0]),
                Node(features=[1, -0.50043, 1.86184, 0.3127, 0.6867, 0.0005, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[2, -0.51211, 1.76919, 0.32825, 0.6705, 0.0012, 0.00005]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[1, -0.48921, 1.87884, 0.2791, 0.7203, 0.0005, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[1, -0.48483, 1.87975, 0.2796, 0.7198, 0.0006, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[1, -0.49310, 1.86490, 0.3133, 0.6860, 0.0006, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[2, -0.504135, 1.766285, 0.32715, 0.6716, 0.0012, 0.00005]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[3, -0.5798866, 1.91078, 0.2991, 0.6994333, 0.0014, 0.0000333]),
                Node(features=[3, -0.5712033, 1.89843666666667, 0.2962666, 0.7019, 0.0017666, 0.0000666]),
                Node(features=[3, -0.55052, 1.863, 0.2877333, 0.70986666, 0.002333, 0.00006666]),
                Node(features=[3, -0.5467866, 1.85364, 0.2865666, 0.7108333, 0.0025333, 0.0000666])
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.OMIT,
            BondOrderType.WIBERG,
            [NodeFeature.LONE_VACANCY_MIN, NodeFeature.LONE_VACANCY_S, NodeFeature.LONE_VACANCY_P, NodeFeature.LONE_VACANCY_D, NodeFeature.LONE_VACANCY_F],
            [
                Node(features=[1, -0.04626, 0.30391, 0.9988, 0.0002, 0.001, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.OMIT,
            BondOrderType.WIBERG,
            [NodeFeature.LONE_VACANCY_AVERAGE, NodeFeature.LONE_VACANCY_S, NodeFeature.LONE_VACANCY_P, NodeFeature.LONE_VACANCY_D, NodeFeature.LONE_VACANCY_F],
            [
                Node(features=[1, -0.04626, 0.30391, 0.9988, 0.0002, 0.001, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            ]
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            BondOrderType.WIBERG,
            [NodeFeature.LONE_VACANCY_MIN, NodeFeature.LONE_VACANCY_S, NodeFeature.LONE_VACANCY_P, NodeFeature.LONE_VACANCY_D, NodeFeature.LONE_VACANCY_F],
            [
                Node(features=[2, -0.16639, 0.76906, 0.0015, 0.0001, 0.9984, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[1, -0.12926, 0.9643, 0.0, 00.9995, 0.0, 0.0005]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            ]
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            BondOrderType.WIBERG,
            [NodeFeature.LONE_VACANCY_AVERAGE, NodeFeature.LONE_VACANCY_S, NodeFeature.LONE_VACANCY_P, NodeFeature.LONE_VACANCY_D, NodeFeature.LONE_VACANCY_F],
            [
                Node(features=[2, 0.4279, 0.570795, 0.43415, 0.0003, 0.5655, 0.00005]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[1, -0.12926, 0.9643, 0.0, 0.9995, 0.0, 0.0005]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                Node(features=[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            ]
        ],

    ])
    def test_get_nodes(self, file_path, hydrogen_mode, bond_order_mode, node_features, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator settings
        ggs = GraphGeneratorSettings.default(node_features=node_features,
                                             edge_features=[],
                                             hydrogen_mode=hydrogen_mode,
                                             bond_order_mode=bond_order_mode)

        # set up graph generator with variable node feature list
        gg = GraphGenerator(ggs)

        # get nodes
        result = gg._get_nodes(qm_data, include_misc_data=False)

        print(result[0].features)

        # test
        Utils.assert_are_almost_equal(result, expected, places=3)

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            HydrogenMode.OMIT,
            BondOrderType.NLMO,
            [NodeFeature.ATOMIC_NUMBER, NodeFeature.NLMO_BOND_ORDER_TOTAL],
            4,
            Node(features=[16, 1.9874], position=[-4.918379, -0.662092, -0.151817], label='S')
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.IMPLICIT,
            BondOrderType.NLMO,
            [],
            0,
            Node(features=[0], position=[-1.339211, 0.079206, -0.361021], label='Ir')
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            BondOrderType.NLMO,
            [NodeFeature.NATURAL_ATOMIC_CHARGE],
            1,
            Node(features=[-0.05261], position=[-1.744384, 0.823097, -1.698982], label='H')
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            BondOrderType.NLMO,
            [NodeFeature.LONE_PAIR_ENERGY_MIN_MAX_DIFFERENCE],
            0,
            Node(features=[3, 0.00634], position=[-1.339211, 0.079206, -0.361021], label='Ir')
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            BondOrderType.NLMO,
            [NodeFeature.LONE_PAIR_ENERGY_MIN_MAX_DIFFERENCE],
            2,
            Node(features=[1, 0.0], position=[0.559518, 0.732394, -0.460712], label='N')
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            BondOrderType.NLMO,
            [NodeFeature.LONE_PAIR_ENERGY_MIN_MAX_DIFFERENCE],
            1,
            Node(features=[0, 0.0], position=[-1.744384, 0.823097, -1.698982], label='H')
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            BondOrderType.NLMO,
            [NodeFeature.LONE_VACANCY_ENERGY_MIN_MAX_DIFFERENCE],
            0,
            Node(features=[2, 1.18858], position=[-1.339211, 0.079206, -0.361021], label='Ir')
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            BondOrderType.NLMO,
            [NodeFeature.LONE_VACANCY_ENERGY_MIN_MAX_DIFFERENCE],
            7,
            Node(features=[1, 0.0], position=[2.376961, 2.324297, -0.765855], label='C')
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            BondOrderType.NLMO,
            [NodeFeature.LONE_VACANCY_ENERGY_MIN_MAX_DIFFERENCE],
            1,
            Node(features=[0, 0.0], position=[-1.744384, 0.823097, -1.698982], label='H')
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            BondOrderType.NLMO,
            [NodeFeature.LONE_PAIR_ENERGY_MIN_MAX_DIFFERENCE, NodeFeature.LONE_VACANCY_ENERGY_MIN_MAX_DIFFERENCE],
            0,
            Node(features=[3, 0.00634, 2, 1.18858], position=[-1.339211, 0.079206, -0.361021], label='Ir')
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            BondOrderType.NLMO,
            [NodeFeature.NATURAL_ELECTRON_POPULATION_TOTAL, NodeFeature.NATURAL_ELECTRON_POPULATION_CORE, NodeFeature.NATURAL_ELECTRON_POPULATION_VALENCE, NodeFeature.NATURAL_ELECTRON_POPULATION_RYDBERG],
            0,
            Node(features=[67.99971, 8.01992, 0.03702, 76.05666], position=[-1.339211, 0.079206, -0.361021], label='Ir')
        ],

    ])
    def test_get_individual_node(self, file_path, hydrogen_mode, bond_order_mode, node_features, atom_index, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator settings
        ggs = GraphGeneratorSettings.default(node_features=node_features,
                                             edge_features=[],
                                             hydrogen_mode=hydrogen_mode,
                                             bond_order_mode=bond_order_mode)

        # set up graph generator with variable node feature list
        gg = GraphGenerator(ggs)

        # get nodes
        result = gg._get_individual_node(qm_data, atom_index)

        Utils.assert_are_almost_equal(result, expected, places=3)

    @parameterized.expand([

        [
            HydrogenMode.EXPLICIT,
            [EdgeType.BOND_ORDER_METAL, EdgeType.BOND_ORDER_NON_METAL],
            BondOrderType.WIBERG,
            [EdgeFeature.WIBERG_BOND_ORDER],
            1,
            [
                Edge([2, 3], [1.4785]), Edge([2, 6], [1.2435]), Edge([3, 4], [1.2259]), Edge([3, 9], [1.0752]),
                Edge([4, 5], [1.2267]), Edge([5, 6], [1.5581]), Edge([6, 7], [1.0438]), Edge([8, 9], [1.3553]),
                Edge([8, 13], [1.3698]), Edge([9, 10], [1.3595]), Edge([10, 11], [1.4483]), Edge([11, 12], [1.4358]),
                Edge([12, 13], [1.3751]), Edge([13, 19], [1.0384]), Edge([14, 15], [1.3568]), Edge([14, 19], [1.3691]),
                Edge([15, 16], [1.3538]), Edge([15, 21], [1.0775]), Edge([16, 17], [1.4541]), Edge([17, 18], [1.4305]),
                Edge([18, 19], [1.3784]), Edge([20, 21], [1.4728]), Edge([20, 24], [1.2457]), Edge([21, 22], [1.2279]),
                Edge([22, 23], [1.2305]), Edge([23, 24], [1.554]), Edge([24, 25], [1.0439]), Edge([26, 28], [1.0553]),
                Edge([26, 29], [1.2463]), Edge([26, 30], [1.2875])
            ]
        ],

        [
            HydrogenMode.EXPLICIT,
            [EdgeType.BOND_ORDER_METAL, EdgeType.BOND_ORDER_NON_METAL],
            BondOrderType.WIBERG,
            [EdgeFeature.BOND_DISTANCE],
            1,
            [
                Edge([2, 3], features=[1.327352]), Edge([2, 6], [1.376780]), Edge([3, 4], [1.738008]), Edge([3, 9], [1.470177]),
                Edge([4, 5], [1.724577]), Edge([5, 6], [1.388826]), Edge([6, 7], [1.493880]), Edge([8, 9], [1.345686]),
                Edge([8, 13], [1.344363]), Edge([9, 10], [1.410199]), Edge([10, 11], [1.399380]), Edge([11, 12], [1.402615]),
                Edge([12, 13], [1.409355]), Edge([13, 19], [1.495214]), Edge([14, 15], [1.345307]), Edge([14, 19], [1.343885]),
                Edge([15, 16], [1.411362]), Edge([15, 21], [1.468893]), Edge([16, 17], [1.398391]), Edge([17, 18], [1.403130]),
                Edge([18, 19], [1.408509]), Edge([20, 21], [1.327983]), Edge([20, 24], [1.376516]), Edge([21, 22], [1.737262]),
                Edge([22, 23], [1.722296]), Edge([23, 24], [1.388434]), Edge([24, 25], [1.493701]), Edge([26, 28], [1.544322]),
                Edge([26, 29], [1.482748]), Edge([26, 30], [1.471084])
            ]
        ],

        [
            HydrogenMode.EXPLICIT,
            [EdgeType.BOND_ORDER_METAL, EdgeType.BOND_ORDER_NON_METAL],
            BondOrderType.WIBERG,
            [EdgeFeature.BOND_ORBITAL_MAX, EdgeFeature.BOND_ORBITAL_DATA_D],
            1,
            [
                Edge([2, 3], [2, -0.47335, 1.86181, 0.00125]), Edge([2, 6], [1, -0.83628, 1.98204, 0.0024]), Edge([3, 4], [1, -0.71751, 1.97740, 0.0048]), Edge([3, 9], [1, -0.75230, 1.97911, 0.00075]),
                Edge([4, 5], [1, -0.70950, 1.97628, 0.0055]), Edge([5, 6], [2, -0.40546, 1.80326, 0.0011]), Edge([6, 7], [1, -0.68826, 1.98282, 0.0011]), Edge([8, 9], [2, -0.46423, 1.73906, 0.00115]),
                Edge([8, 13], [1, -0.87779, 1.98407, 0.0021]), Edge([9, 10], [1, -0.75976, 1.98302, 0.0011]), Edge([10, 11], [2, -0.39926, 1.61498, 0.00055]), Edge([11, 12], [1, -0.75330, 1.98387, 0.00135]),
                Edge([12, 13], [2, -0.40128, 1.58771, 0.0003]), Edge([13, 19], [1, -0.72173, 1.97437, 0.0007]), Edge([14, 15], [2, -0.45893, 1.73616, 0.00115]), Edge([14, 19], [1, -0.87405, 1.98390, 0.0021]),
                Edge([15, 16], [1, -0.75425, 1.98305, 0.00105]), Edge([15, 21], [1, -0.74646, 1.97899, 0.00075]), Edge([16, 17], [2, -0.39528, 1.61781, 0.00055]), Edge([17, 18], [1, -0.74945, 1.98371, 0.00135]),
                Edge([18, 19], [2, -0.39886, 1.59508, 0.0003]), Edge([20, 21], [2, -0.46620, 1.86014, 0.00085]), Edge([20, 24], [1, -0.82945, 1.98174, 0.0024]), Edge([21, 22], [1, -0.71051, 1.97741, 0.0048]),
                Edge([22, 23], [1, -0.70280, 1.97615, 0.00545]), Edge([23, 24], [2, -0.39736, 1.79809, 0.0011]), Edge([24, 25], [1, -0.68261, 1.98279, 0.00105]), Edge([26, 28], [1, -0.92396, 1.98066, 0.01155]),
                Edge([26, 29], [1, -0.97513, 1.98174, 0.0112]), Edge([26, 30], [1, -0.98492, 1.98216, 0.011])
            ]
        ],
    ])
    def test_get_edges(self, hydrogen_mode, edge_types, bond_order_mode, edge_features, bond_threshold, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(TEST_FILE_LALMER))

        # set up graph generator settings
        ggs = GraphGeneratorSettings.default(node_features=[],
                                             edge_features=edge_features,
                                             hydrogen_mode=hydrogen_mode,
                                             bond_order_mode=bond_order_mode,
                                             edge_types=edge_types,
                                             bond_threshold=bond_threshold)

        # set up graph generator with variable node feature list
        gg = GraphGenerator(ggs)

        # get edges
        result = gg._get_edges(qm_data)

        # compare to expected
        Utils.assert_are_almost_equal(result, expected, places=3)

    @parameterized.expand([

        [0, 0.1, []],

        [11, 0.1, [10, 12, 41]],

    ])
    def test_get_bound_atom_indices(self, atom_index, threshold, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(TEST_FILE_LALMER))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default())

        # get result
        result = gg._get_bound_atom_indices(atom_index, qm_data, threshold)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [-1, 0.1],

        [47, 0.1],

    ])
    def test_get_bound_atom_indices_with_invalid_input(self, atom_index, threshold):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(TEST_FILE_LALMER))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default())

        # get result
        self.assertRaises(ValueError, gg._get_bound_atom_indices, atom_index, qm_data, threshold)

    @parameterized.expand([

        [2, 0.1, []],

        [7, 0.1, [32, 45, 46]]

    ])
    def test_get_bound_h_indices(self, atom_index, threshold, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(TEST_FILE_LALMER))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default())

        # get result
        result = gg._get_bound_h_atom_indices(atom_index, qm_data, threshold)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [-1, 0.1],

        [47, 0.1],

    ])
    def test_get_bound_h_indices_with_invalid_input(self, atom_index, threshold):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(TEST_FILE_LALMER))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default())

        # get result
        self.assertRaises(ValueError, gg._get_bound_h_atom_indices, atom_index, qm_data, threshold)

    @parameterized.expand([

        [15, 0],

        [18, 1],

    ])
    def test_determine_hydrogen_count(self, atom_index, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(TEST_FILE_LALMER))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default())

        # get result
        result = gg._determine_hydrogen_count(atom_index, qm_data)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [
            [GraphFeature.MOLECULAR_MASS],
            [580.92867]
        ],

        [
            [GraphFeature.N_ATOMS],
            [47]
        ],

        [
            [GraphFeature.CHARGE],
            [1]
        ],
    ])
    def test_get_graph_features(self, graph_features, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(TEST_FILE_LALMER))

        # set up graph generator settings
        ggs = GraphGeneratorSettings.default(graph_features=graph_features)

        # set up graph generator (default values)
        gg = GraphGenerator(ggs)

        # get result
        result = gg._get_graph_features(qm_data)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            [QmTarget.SVP_ELECTRONIC_ENERGY],
            [-2711.31113930]
        ],

        [
            TEST_FILE_LALMER,
            [QmTarget.TZVP_ELECTRONIC_ENERGY],
            [-2713.37704931]
        ],

        [
            TEST_FILE_LALMER,
            [QmTarget.ELECTRONIC_ENERGY_DELTA],
            [2.06591001000015]
        ],

        [
            TEST_FILE_LALMER,
            [QmTarget.SVP_HOMO_ENERGY],
            [-0.31642]
        ],

        [
            TEST_FILE_LALMER,
            [QmTarget.SVP_LUMO_ENERGY],
            [-0.22836]
        ],

        [
            TEST_FILE_LALMER,
            [QmTarget.TZVP_HOMO_ENERGY],
            [-0.35379]
        ],

        [
            TEST_FILE_LALMER,
            [QmTarget.TZVP_LUMO_ENERGY],
            [-0.20437]
        ],

        [
            TEST_FILE_LALMER,
            [QmTarget.POLARISABILITY],
            [334.01]
        ],

        [
            TEST_FILE_LALMER,
            [QmTarget.SVP_DISPERSION_ENERGY],
            [-0.0815876275]
        ],

        [
            TEST_FILE_LALMER,
            [QmTarget.TZVP_DISPERSION_ENERGY],
            [-0.0751559981]
        ],

        [
            TEST_FILE_LALMER,
            [QmTarget.DISPERSION_ENERGY_DELTA],
            [0.0064316294]
        ],

        [
            TEST_FILE_LALMER,
            [QmTarget.LOWEST_VIBRATIONAL_FREQUENCY],
            [19.9016]
        ],

        [
            TEST_FILE_LALMER,
            [QmTarget.HIGHEST_VIBRATIONAL_FREQUENCY],
            [3786.4682]
        ],

        [
            TEST_FILE_LALMER,
            [QmTarget.HEAT_CAPACITY],
            [116.184]
        ],

        [
            TEST_FILE_LALMER,
            [QmTarget.ENTROPY],
            [205.610]
        ],

        [
            TEST_FILE_LALMER,
            [QmTarget.ZPE_CORRECTION],
            [0.318790]
        ],

        [
            TEST_FILE_LALMER,
            [QmTarget.ENTHALPY_ENERGY],
            [-2710.959666]
        ],

        [
            TEST_FILE_LALMER,
            [QmTarget.GIBBS_ENERGY],
            [-2711.057358]
        ],

        [
            TEST_FILE_LALMER,
            [QmTarget.ENTHALPY_ENERGY_CORRECTION],
            [0.351473]
        ],

        [
            TEST_FILE_LALMER,
            [QmTarget.GIBBS_ENERGY_CORRECTION],
            [0.253781]
        ],

        [
            TEST_FILE_LALMER,
            [QmTarget.SVP_HOMO_LUMO_GAP],
            [0.08806]
        ],

        [
            TEST_FILE_LALMER,
            [QmTarget.TZVP_HOMO_LUMO_GAP],
            [0.14942]
        ],

        [
            TEST_FILE_LALMER,
            [QmTarget.HOMO_LUMO_GAP_DELTA],
            [0.06136]
        ],

        [
            TEST_FILE_LALMER,
            [QmTarget.SVP_DIPOLE_MOMENT],
            [11.3194]
        ],

        [
            TEST_FILE_LALMER,
            [QmTarget.TZVP_DIPOLE_MOMENT],
            [11.8657]
        ],

        [
            TEST_FILE_LALMER,
            [QmTarget.DIPOLE_MOMENT_DELTA],
            [0.5463]
        ],

    ])
    def test_get_targets(self, file_path, targets, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator settings
        ggs = GraphGeneratorSettings.default(targets=targets)

        # set up graph generator (default values)
        gg = GraphGenerator(ggs)

        # get result
        result = gg._get_targets(qm_data)

        Utils.assert_are_almost_equal(result, expected, places=5)

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            HydrogenMode.EXPLICIT,
            [EdgeType.BOND_ORDER_METAL, EdgeType.BOND_ORDER_NON_METAL],
            BondOrderType.WIBERG,
            1,
            1,
            [
                [2, 3], [2, 6], [3, 4], [3, 9], [4, 5], [5, 6], [6, 7],
                [8, 9], [8, 13], [9, 10], [10, 11], [11, 12], [12, 13],
                [13, 19], [14, 15], [14, 19], [15, 16], [15, 21], [16, 17],
                [17, 18], [18, 19], [20, 21], [20, 24], [21, 22], [22, 23],
                [23, 24], [24, 25], [26, 28], [26, 29], [26, 30]
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.EXPLICIT,
            [EdgeType.BOND_ORDER_METAL, EdgeType.BOND_ORDER_NON_METAL],
            BondOrderType.LMO,
            1,
            1,
            [
                [2, 3], [3, 4], [3, 9], [4, 5], [5, 6], [8, 9], [8, 13],
                [9, 10], [10, 11], [11, 12], [12, 13], [13, 19], [14, 15],
                [14, 19], [15, 16], [15, 21], [16, 17], [17, 18], [18, 19],
                [20, 21], [21, 22], [22, 23], [23, 24], [26, 29], [26, 30]
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.IMPLICIT,
            [EdgeType.BOND_ORDER_METAL, EdgeType.BOND_ORDER_NON_METAL],
            BondOrderType.LMO,
            1,
            1,
            [
                [2, 3], [3, 4], [3, 9], [4, 5], [5, 6], [8, 9], [8, 13],
                [9, 10], [10, 11], [11, 12], [12, 13], [13, 19], [14, 15],
                [14, 19], [15, 16], [15, 21], [16, 17], [17, 18], [18, 19],
                [20, 21], [21, 22], [22, 23], [23, 24], [26, 29], [26, 30]
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.EXPLICIT,
            [EdgeType.BOND_ORDER_METAL, EdgeType.BOND_ORDER_NON_METAL],
            BondOrderType.NLMO,
            1,
            1,
            [
                [2, 3], [3, 4], [3, 9], [4, 5], [5, 6], [8, 9], [8, 13],
                [9, 10], [10, 11], [11, 12], [12, 13], [13, 19], [14, 15],
                [14, 19], [15, 16], [15, 21], [16, 17], [17, 18], [18, 19],
                [20, 21], [21, 22], [22, 23], [23, 24], [26, 29], [26, 30]
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.EXPLICIT,
            [EdgeType.NBO_BONDING_ORBITALS],
            BondOrderType.WIBERG,
            1,
            1,
            [
                [1, 31], [1, 33], [2, 3], [2, 6], [3, 4], [3, 9], [4, 5],
                [5, 6], [5, 44], [6, 7], [7, 32], [7, 45], [7, 46], [8, 9],
                [8, 13], [9, 10], [10, 11], [10, 42], [11, 12], [11, 41],
                [12, 13], [12, 37], [13, 19], [14, 15], [14, 19], [15, 16],
                [15, 21], [16, 17], [16, 34], [17, 18], [17, 36], [18, 19],
                [18, 40], [20, 21], [20, 24], [21, 22], [22, 23], [23, 24],
                [23, 35], [24, 25], [25, 38], [25, 39], [25, 43], [26, 27],
                [26, 28], [26, 29], [26, 30]
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.IMPLICIT,
            [EdgeType.NBO_BONDING_ORBITALS],
            BondOrderType.WIBERG,
            1,
            1,
            [
                [2, 3], [2, 6], [3, 4], [3, 9], [4, 5], [5, 6], [6, 7], [8, 9],
                [8, 13], [9, 10], [10, 11], [11, 12], [12, 13], [13, 19], [14, 15],
                [14, 19], [15, 16], [15, 21], [16, 17], [17, 18], [18, 19], [20, 21],
                [20, 24], [21, 22], [22, 23], [23, 24], [24, 25], [26, 27], [26, 28],
                [26, 29], [26, 30]
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.EXPLICIT,
            [EdgeType.BOND_ORDER_METAL, EdgeType.BOND_ORDER_NON_METAL],
            BondOrderType.WIBERG,
            1,
            0.07,
            [
                [0, 2], [0, 8], [0, 14], [0, 20], [0, 27],
                [2, 3], [2, 6], [3, 4], [3, 9], [4, 5], [5, 6], [6, 7],
                [8, 9], [8, 13], [9, 10], [10, 11], [11, 12], [12, 13],
                [13, 19], [14, 15], [14, 19], [15, 16], [15, 21], [16, 17],
                [17, 18], [18, 19], [20, 21], [20, 24], [21, 22], [22, 23],
                [23, 24], [24, 25], [26, 28], [26, 29], [26, 30]
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.EXPLICIT,
            [EdgeType.BOND_ORDER_METAL, EdgeType.BOND_ORDER_NON_METAL],
            BondOrderType.NLMO,
            1,
            0.05,
            [
                [0, 2], [0, 20],
                [2, 3], [3, 4], [3, 9], [4, 5], [5, 6], [8, 9], [8, 13],
                [9, 10], [10, 11], [11, 12], [12, 13], [13, 19], [14, 15],
                [14, 19], [15, 16], [15, 21], [16, 17], [17, 18], [18, 19],
                [20, 21], [21, 22], [22, 23], [23, 24], [26, 29], [26, 30]
            ]
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.EXPLICIT,
            [EdgeType.BOND_ORDER_METAL, EdgeType.BOND_ORDER_NON_METAL],
            BondOrderType.WIBERG,
            1,
            1,
            [
                [2, 3], [2, 16], [3, 5], [5, 6], [5, 17], [6, 7], [7, 8],
                [7, 16], [8, 10], [10, 12], [12, 14], [14, 16], [17, 18],
                [17, 26], [18, 20], [20, 22], [22, 24], [24, 26], [28, 29],
                [29, 30], [29, 34], [30, 32], [32, 33], [32, 38], [42, 43],
                [43, 44], [43, 48], [44, 46], [46, 47], [46, 52], [1, 0]
            ]
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.EXPLICIT,
            [EdgeType.BOND_ORDER_METAL, EdgeType.BOND_ORDER_NON_METAL],
            BondOrderType.WIBERG,
            1,
            0.3,
            [
                [0, 1], [0, 2], [0, 28], [0, 33], [0, 42],
                [2, 3], [2, 16], [3, 5], [5, 6], [5, 17], [6, 7], [7, 8],
                [7, 16], [8, 10], [10, 12], [12, 14], [14, 16], [17, 18],
                [17, 26], [18, 20], [20, 22], [22, 24], [24, 26], [28, 29],
                [29, 30], [29, 34], [30, 32], [32, 33], [32, 38], [42, 43],
                [43, 44], [43, 48], [44, 46], [46, 47], [46, 52]
            ]
        ],

        [
            TEST_FILE_ZUYHEG,
            HydrogenMode.EXPLICIT,
            [EdgeType.NBO_BONDING_ORBITALS],
            BondOrderType.WIBERG,
            1,
            0.3,
            [
                [0, 12], [0, 14], [1, 2], [1, 5], [1, 10], [1, 22], [2, 3],
                [2, 7], [2, 23], [3, 4], [3, 7], [3, 16], [4, 5], [4, 8], [4, 24],
                [5, 9], [5, 25], [6, 7], [6, 10], [6, 26], [7, 8], [7, 11],
                [7, 27], [8, 9], [8, 28], [9, 10], [9, 11], [9, 29], [10, 11],
                [10, 30], [11, 31], [12, 13], [14, 15], [16, 17], [16, 32],
                [17, 18], [17, 33], [18, 19], [18, 20], [18, 21], [19, 34],
                [19, 35], [19, 36], [20, 37], [20, 38], [20, 39], [21, 40],
                [21, 41], [21, 42]
            ]
        ],

        [
            TEST_FILE_ZUYHEG,
            HydrogenMode.IMPLICIT,
            [EdgeType.NBO_BONDING_ORBITALS],
            BondOrderType.WIBERG,
            1,
            0.3,
            [
                [0, 12], [0, 14], [1, 2], [1, 5], [1, 10], [2, 3], [2, 7], [3, 4],
                [3, 7], [3, 16], [4, 5], [4, 8], [5, 9], [6, 7], [6, 10], [7, 8],
                [7, 11], [8, 9], [9, 10], [9, 11], [10, 11], [12, 13], [14, 15],
                [16, 17], [17, 18], [18, 19], [18, 20], [18, 21]
            ]
        ],

    ])
    def test_get_adjacency_list(self, file_path, hydrogen_mode, edge_types, bond_order_mode, bond_threshold, bond_threshold_metal, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator settings
        ggs = GraphGeneratorSettings.default(edge_types=edge_types, bond_order_mode=bond_order_mode, bond_threshold=bond_threshold, bond_threshold_metal=bond_threshold_metal, hydrogen_mode=hydrogen_mode)

        # set up graph generator (default values)
        gg = GraphGenerator(ggs)

        # get result
        result = gg._get_adjacency_list(qm_data)
        print(result)
        self.assertEqual(result, expected)

    @parameterized.expand([

        [
            [15, 21],
            [EdgeFeature.BOND_ORBITAL_MAX, EdgeFeature.BOND_DISTANCE, EdgeFeature.BOND_ORBITAL_DATA_S],
            Edge([15, 21], features=[1.468893, 1, -0.74646, 1.97899, 0.34105])
        ],

        [
            [15, 21],
            [EdgeFeature.BOND_ORBITAL_AVERAGE, EdgeFeature.BOND_DISTANCE, EdgeFeature.BOND_ORBITAL_DATA_S],
            Edge([15, 21], [1.468893, 1, -0.74646, 1.97899, 0.34105])
        ],

        [
            [2, 3],
            [EdgeFeature.BOND_ORBITAL_MAX, EdgeFeature.BOND_ORBITAL_DATA_S, EdgeFeature.BOND_ORBITAL_DATA_P, EdgeFeature.BOND_ORBITAL_DATA_D, EdgeFeature.  BOND_ORBITAL_DATA_F],
            Edge([2, 3], [2, -0.47335, 1.86181, 0.0, 0.9983, 0.00125, 0.0004])
        ],

        [
            [2, 3],
            [EdgeFeature.BOND_ORBITAL_AVERAGE, EdgeFeature.BOND_ORBITAL_DATA_S, EdgeFeature.BOND_ORBITAL_DATA_P, EdgeFeature.BOND_ORBITAL_DATA_D, EdgeFeature.  BOND_ORBITAL_DATA_F],
            Edge([2, 3], [2, -0.68039, 1.924115, 0.174625, 0.823025, 0.00195, 0.00035])
        ],

        [
            [2, 3],
            [EdgeFeature.ANTIBOND_ORBITAL_MIN, EdgeFeature.ANTIBOND_ORBITAL_DATA_S, EdgeFeature.ANTIBOND_ORBITAL_DATA_P, EdgeFeature.ANTIBOND_ORBITAL_DATA_D, EdgeFeature.ANTIBOND_ORBITAL_DATA_F],
            Edge([2, 3], [2, -0.15285, 0.47234, 0.0, 0.9983, 0.00125, 0.0004])
        ],

        [
            [2, 3],
            [EdgeFeature.ANTIBOND_ORBITAL_AVERAGE, EdgeFeature.ANTIBOND_ORBITAL_DATA_S, EdgeFeature.ANTIBOND_ORBITAL_DATA_P, EdgeFeature.ANTIBOND_ORBITAL_DATA_D, EdgeFeature.ANTIBOND_ORBITAL_DATA_F],
            Edge([2, 3], [2, 0.110375, 0.247345, 0.174625, 0.823025, 0.00195, 0.00035])
        ],

        [
            [2, 3],
            [EdgeFeature.ANTIBOND_ORBITAL_MIN, EdgeFeature.ANTIBOND_ORBITAL_AVERAGE, EdgeFeature.ANTIBOND_ORBITAL_DATA_S, EdgeFeature.ANTIBOND_ORBITAL_DATA_P, EdgeFeature.ANTIBOND_ORBITAL_DATA_D, EdgeFeature.ANTIBOND_ORBITAL_DATA_F],
            Edge([2, 3], [2, -0.15285, 0.47234, 0.0, 0.9983, 0.00125, 0.0004, 0.110375, 0.247345, 0.174625, 0.823025, 0.00195, 0.00035])
        ],

        [
            [0, 4],
            [EdgeFeature.BOND_ORBITAL_AVERAGE, EdgeFeature.BOND_ORBITAL_DATA_S, EdgeFeature.BOND_ORBITAL_DATA_P, EdgeFeature.BOND_ORBITAL_DATA_D, EdgeFeature.BOND_ORBITAL_DATA_F],
            Edge([0, 4], [0, 0.0, 0.0, 0.3458798245614035, 0.6517228070175439, 0.0020701754385964913, 0.0003280701754385965])
        ],

        [
            [0, 5],
            [EdgeFeature.ANTIBOND_ORBITAL_AVERAGE, EdgeFeature.ANTIBOND_ORBITAL_DATA_S, EdgeFeature.ANTIBOND_ORBITAL_DATA_P, EdgeFeature.ANTIBOND_ORBITAL_DATA_D, EdgeFeature.ANTIBOND_ORBITAL_DATA_F],
            Edge([0, 5], [0, 0.0, 0.0, 0.3458798245614035, 0.6517228070175439, 0.0020701754385964913, 0.0003280701754385965])
        ],

        [
            [2, 3],
            [EdgeFeature.BOND_ENERGY_MIN_MAX_DIFFERENCE],
            Edge([2, 3], [2, 0.41408])
        ],

        [
            [2, 3],
            [EdgeFeature.ANTIBOND_ENERGY_MIN_MAX_DIFFERENCE],
            Edge([2, 3], [2, 0.52645])
        ],

        [
            [0, 5],
            [EdgeFeature.BOND_ENERGY_MIN_MAX_DIFFERENCE],
            Edge([0, 5], [0, 0.0])
        ],

        [
            [0, 5],
            [EdgeFeature.ANTIBOND_ENERGY_MIN_MAX_DIFFERENCE],
            Edge([0, 5], [0, 0.0])
        ],

        [
            [2, 3],
            [EdgeFeature.BOND_ENERGY_MIN_MAX_DIFFERENCE, EdgeFeature.ANTIBOND_ENERGY_MIN_MAX_DIFFERENCE],
            Edge([2, 3], [2, 0.41408, 0.52645])
        ],

        [
            [2, 6],
            [EdgeFeature.BOND_ENERGY_MIN_MAX_DIFFERENCE],
            Edge([2, 6], [1, 0.0])
        ],

    ])
    def test_get_featurised_edge(self, bond_indices, edge_features, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(TEST_FILE_LALMER))

        # set up graph generator settings
        ggs = GraphGeneratorSettings.default(edge_features=edge_features)

        # set up graph generator (default values)
        gg = GraphGenerator(ggs)

        # get result
        result = gg._get_featurised_edge(bond_indices, qm_data)

        Utils.assert_are_almost_equal(result, expected, places=5)

    @parameterized.expand([

        [
            TEST_FILE_OREDIA,
            [2, 5],
            [EdgeFeature.LMO_BOND_ORDER],
            [-0.0394236]
        ],

        [
            TEST_FILE_OREDIA,
            [2, 5],
            [EdgeFeature.NLMO_BOND_ORDER],
            [-0.0471]
        ],

        [
            TEST_FILE_ZUYHEG,
            [3, 7],
            [EdgeFeature.BOND_ENERGY_MIN_MAX_DIFFERENCE, EdgeFeature.BOND_ORBITAL_AVERAGE, EdgeFeature.BOND_ORBITAL_MAX,
             EdgeFeature.BOND_ORBITAL_DATA_S, EdgeFeature.BOND_ORBITAL_DATA_P, EdgeFeature.BOND_ORBITAL_DATA_D, EdgeFeature.BOND_ORBITAL_DATA_F],
            [1, 0.0, -0.41717, 1.76966, 0.20673333333333332, 0.7872, 0.005666666666666667, 0.0004, -0.41717, 1.76966, 0.20673333333333332, 0.7872, 0.005666666666666667, 0.0004]
        ],

        [
            TEST_FILE_ZUYHEG,
            [7, 8],
            [EdgeFeature.BOND_ENERGY_MIN_MAX_DIFFERENCE, EdgeFeature.BOND_ORBITAL_AVERAGE, EdgeFeature.BOND_ORBITAL_MAX,
             EdgeFeature.BOND_ORBITAL_DATA_S, EdgeFeature.BOND_ORBITAL_DATA_P, EdgeFeature.BOND_ORBITAL_DATA_D, EdgeFeature.BOND_ORBITAL_DATA_F],
            [1, 0.0, -0.41717, 1.76966, 0.20673333333333332, 0.7872, 0.005666666666666667, 0.0004, -0.41717, 1.76966, 0.20673333333333332, 0.7872, 0.005666666666666667, 0.0004]
        ],

        [
            TEST_FILE_ZUYHEG,
            [8, 9],
            [EdgeFeature.ANTIBOND_ENERGY_MIN_MAX_DIFFERENCE, EdgeFeature.ANTIBOND_ORBITAL_AVERAGE, EdgeFeature.ANTIBOND_ORBITAL_MIN,
             EdgeFeature.ANTIBOND_ORBITAL_DATA_S, EdgeFeature.ANTIBOND_ORBITAL_DATA_P, EdgeFeature.ANTIBOND_ORBITAL_DATA_D, EdgeFeature.ANTIBOND_ORBITAL_DATA_F],
            [1, 0.0, 0.27167, 0.11428, 0.34376666666666666, 0.6507333333333333, 0.005166666666666666, 0.00036666666666666667, 0.27167, 0.11428, 0.34376666666666666, 0.6507333333333333, 0.005166666666666666, 0.00036666666666666667]
        ],

        [
            TEST_FILE_ZUYHEG,
            [9, 11],
            [EdgeFeature.ANTIBOND_ENERGY_MIN_MAX_DIFFERENCE, EdgeFeature.ANTIBOND_ORBITAL_AVERAGE, EdgeFeature.ANTIBOND_ORBITAL_MIN,
             EdgeFeature.ANTIBOND_ORBITAL_DATA_S, EdgeFeature.ANTIBOND_ORBITAL_DATA_P, EdgeFeature.ANTIBOND_ORBITAL_DATA_D, EdgeFeature.ANTIBOND_ORBITAL_DATA_F],
            [1, 0.0, 0.27167, 0.11428, 0.34376666666666666, 0.6507333333333333, 0.005166666666666666, 0.00036666666666666667, 0.27167, 0.11428, 0.34376666666666666, 0.6507333333333333, 0.005166666666666666, 0.00036666666666666667]
        ],

        [
            TEST_FILE_ZUYHEG,
            [0, 21],
            [EdgeFeature.NBO_TYPE],
            ['None']
        ],

        [
            TEST_FILE_ZUYHEG,
            [17, 18],
            [EdgeFeature.NBO_TYPE],
            ['BD']
        ],

        [
            TEST_FILE_ZUYHEG,
            [9, 10],
            [EdgeFeature.NBO_TYPE],
            ['3C']
        ],
    ])
    def test_get_edge_features(self, file_path, bond_indices, edge_features, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator settings
        ggs = GraphGeneratorSettings.default(edge_features=edge_features)

        # set up graph generator (default values)
        gg = GraphGenerator(ggs)

        # get result
        result = gg._get_edge_features(bond_indices, qm_data)
        print(result)
        Utils.assert_are_almost_equal(result, expected, places=5)

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            []
        ],

        [
            TEST_FILE_OREDIA,
            [1]
        ],

    ])
    def test_get_hydride_hydrogen_indices(self, file_path, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default())

        # get result
        result = gg._get_hydride_hydrogen_indices(qm_data)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            []
        ],

        [
            TEST_FILE_OREDIA,
            [[1, 0]]
        ],

    ])
    def test_get_hydride_bonds_indices(self, file_path, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default())

        # get result
        result = gg._get_hydride_bond_indices(qm_data)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [
            [Node(features=[1, 2, 3]), Node(features=[1, 2, 3]), Node(features=[1, 2])],
            AssertionError
        ],

    ])
    def test_validate_node_list_with_faulty_nodes(self, nodes, expected_error):

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default())

        self.assertRaises(expected_error, gg._validate_node_list, nodes)

    @parameterized.expand([

        [
            [
                Edge([1, 2, 3], features=[1]),
                Edge([2, 3], features=[1]),
                Edge([3, 4], features=[1])
            ],
            5,
            AssertionError
        ],

        [
            [
                Edge([1, 2], features=[1]),
                Edge([2, 3], features=[1, 3]),
                Edge([3, 4], features=[1])
            ],
            5,
            AssertionError
        ],

        # [
        #     [
        #         Edge([1, 1], features=[1]),
        #         Edge([2, 3], features=[1]),
        #         Edge([3, 4], features=[1])
        #     ],
        #     5,
        #     AssertionError
        # ],

        [
            [
                Edge([1, 2], features=[1]),
                Edge([2, 3], features=[1]),
                Edge([3, 4], features=[1])
            ],
            4,
            AssertionError
        ],

        [
            [
                Edge([1, 2], features=[1]),
                Edge([2, 3], features=[1]),
                Edge([4, 3], features=[1])
            ],
            4,
            AssertionError
        ],

    ])
    def test_validate_edge_list_with_faulty_input(self, edges, n_nodes, expected_error):

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default())

        self.assertRaises(expected_error, gg._validate_edge_list, edges, n_nodes)

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            10,
            0
        ],

        [
            TEST_FILE_OREDIA,
            10,
            2
        ],

    ])
    def test_determine_hydrogen_position_offset(self, file_path, atom_index, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default())

        # get result
        result = gg._determine_hydrogen_position_offset(atom_index, qm_data)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [
            TEST_FILE_OREDIA,
            [
                Edge([2, 3], features=[]),
                Edge([2, 11], features=[]),
                Edge([3, 4], features=[]),
                Edge([4, 5], features=[]),
                Edge([4, 12], features=[]),
                Edge([5, 6], features=[]),
                Edge([6, 7], features=[]),
                Edge([6, 11], features=[]),
                Edge([7, 8], features=[]),
                Edge([8, 9], features=[]),
                Edge([9, 10], features=[]),
                Edge([10, 11], features=[]),
                Edge([12, 13], features=[]),
                Edge([12, 17], features=[]),
                Edge([13, 14], features=[]),
                Edge([14, 15], features=[]),
                Edge([15, 16], features=[]),
                Edge([16, 17], features=[]),
                Edge([18, 19], features=[]),
                Edge([19, 20], features=[]),
                Edge([19, 23], features=[]),
                Edge([20, 21], features=[]),
                Edge([21, 22], features=[]),
                Edge([21, 24], features=[]),
                Edge([25, 26], features=[]),
                Edge([26, 27], features=[]),
                Edge([26, 30], features=[]),
                Edge([27, 28], features=[]),
                Edge([28, 29], features=[]),
                Edge([28, 31], features=[]),
                Edge([1, 0], features=[])
            ]
        ],

    ])
    def test_adjust_node_references(self, file_path, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default(hydrogen_mode=HydrogenMode.OMIT,
                                                           edge_types=[EdgeType.NBO_BONDING_ORBITALS]))

        # get result
        edges = gg._get_edges(qm_data)
        result = gg._adjust_node_references(edges, qm_data)

        Utils.assert_are_almost_equal(result, expected)

    @parameterized.expand([

        [
            TEST_FILE_LALMER
        ],

    ])
    def test_get_index_matrix(self, file_path):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default(bond_order_mode=BondOrderType.WIBERG))

        # get result
        result = gg._get_index_matrix(qm_data, gg._settings.bond_order_mode)

        self.assertEqual(result, qm_data.wiberg_bond_order_matrix)

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            HydrogenMode.EXPLICIT,
            [i for i in range(47)]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.OMIT,
            [i for i in range(31)]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.IMPLICIT,
            [i for i in range(31)]
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.EXPLICIT,
            [i for i in range(56)]
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            [i for i in range(56) if i not in [4, 9, 11, 13, 15, 19, 21, 23, 25, 27, 31, 35, 36, 37, 39, 40, 41, 45, 49, 50, 51, 53, 54, 55]]
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.IMPLICIT,
            [i for i in range(56) if i not in [4, 9, 11, 13, 15, 19, 21, 23, 25, 27, 31, 35, 36, 37, 39, 40, 41, 45, 49, 50, 51, 53, 54, 55]]
        ],

    ])
    def test_get_nodes_to_extract_indices(self, file_path, hydrogen_mode, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default(hydrogen_mode=hydrogen_mode))

        # get result
        result = gg._get_nodes_to_extract_indices(qm_data)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            HydrogenMode.EXPLICIT,
            ['Cd', 'O', 'N', 'C', 'S', 'C', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'C', 'N', 'C',
             'C', 'C', 'C', 'C', 'N', 'C', 'S', 'C', 'C', 'C', 'Cl', 'O', 'O', 'O', 'O', 'H',
             'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H']
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.OMIT,
            ['Cd', 'O', 'N', 'C', 'S', 'C', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'C', 'N', 'C',
             'C', 'C', 'C', 'C', 'N', 'C', 'S', 'C', 'C', 'C', 'Cl', 'O', 'O', 'O', 'O']
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.IMPLICIT,
            ['Cd', 'O', 'N', 'C', 'S', 'C', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'C', 'N', 'C',
             'C', 'C', 'C', 'C', 'N', 'C', 'S', 'C', 'C', 'C', 'Cl', 'O', 'O', 'O', 'O']
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.EXPLICIT,
            ['Ir', 'H', 'N', 'C', 'H', 'C', 'N', 'C', 'C', 'H', 'C', 'H', 'C', 'H', 'C', 'H', 'C',
             'C', 'C', 'H', 'C', 'H', 'C', 'H', 'C', 'H', 'C', 'H', 'O', 'C', 'C', 'H', 'C', 'O',
             'C', 'H', 'H', 'H', 'C', 'H', 'H', 'H', 'O', 'C', 'C', 'H', 'C', 'O', 'C', 'H', 'H',
             'H', 'C', 'H', 'H', 'H']
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            ['Ir', 'H', 'N', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C',
             'C', 'O', 'C', 'C', 'C', 'O', 'C', 'C', 'O', 'C', 'C', 'C', 'O', 'C', 'C']
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.IMPLICIT,
            ['Ir', 'H', 'N', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C',
             'C', 'O', 'C', 'C', 'C', 'O', 'C', 'C', 'O', 'C', 'C', 'C', 'O', 'C', 'C']
        ],

    ])
    def test_get_node_labels(self, file_path, hydrogen_mode, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default(hydrogen_mode=hydrogen_mode))

        # get result
        result = gg._get_node_labels(qm_data)

        print(result)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            HydrogenMode.EXPLICIT,
            [
                [-0.106076, -0.278587, -0.33231],
                [-0.170725, -0.845567, -2.701124],
                [-2.392952, -1.000996, -0.486426],
                [-3.291283, -0.056813, -0.23467],
                [-4.918379, -0.662092, -0.151817],
                [-4.328168, -2.249065, -0.479436],
                [-2.947436, -2.25308, -0.629106],
                [-2.088135, -3.443012, -0.907209],
                [-1.595504, 1.597966, -0.098041],
                [-2.917344, 1.351959, -0.042436],
                [-3.844646, 2.389592, 0.185798],
                [-3.354127, 3.689685, 0.351375],
                [-1.973161, 3.927918, 0.292157],
                [-1.106739, 2.839449, 0.066697],
                [1.050535, 1.83432, -0.277272],
                [2.395382, 1.802082, -0.291358],
                [3.154882, 2.962981, -0.031715],
                [2.474689, 4.150985, 0.253731],
                [1.071925, 4.161548, 0.284024],
                [0.38245, 2.963161, 0.014971],
                [2.250483, -0.580998, -0.859162],
                [2.986054, 0.487084, -0.573372],
                [4.690796, 0.155642, -0.527752],
                [4.366931, -1.490301, -0.917992],
                [3.003666, -1.716978, -1.051681],
                [2.351112, -3.029328, -1.339872],
                [0.813861, -1.659551, 2.163461],
                [0.179509, -2.287688, 0.868737],
                [0.526151, -0.149611, 2.014347],
                [2.276932, -1.899656, 2.145771],
                [0.140413, -2.20862, 3.350508],
                [0.621615, -0.550018, -3.189474],
                [-1.402499, -3.616254, -0.052374],
                [-0.930381, -0.628783, -3.274442],
                [4.254082, 2.931636, -0.048303],
                [5.184163, -2.215146, -1.011931],
                [3.037285, 5.071991, 0.464391],
                [-1.584812, 4.946415, 0.420801],
                [3.097829, -3.802562, -1.593459],
                [1.777393, -3.348908, -0.446273],
                [0.534129, 5.086243, 0.529844],
                [-4.049496, 4.522808, 0.529161],
                [-4.923648, 2.18184, 0.232511],
                [1.630822, -2.9331, -2.176881],
                [-5.016404, -3.100675, -0.539305],
                [-1.456789, -3.260287, -1.800301],
                [-2.698445, -4.347582, -1.077877]
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.OMIT,
            [
                [-0.106076, -0.278587, -0.33231],
                [-0.170725, -0.845567, -2.701124],
                [-2.392952, -1.000996, -0.486426],
                [-3.291283, -0.056813, -0.23467],
                [-4.918379, -0.662092, -0.151817],
                [-4.328168, -2.249065, -0.479436],
                [-2.947436, -2.25308, -0.629106],
                [-2.088135, -3.443012, -0.907209],
                [-1.595504, 1.597966, -0.098041],
                [-2.917344, 1.351959, -0.042436],
                [-3.844646, 2.389592, 0.185798],
                [-3.354127, 3.689685, 0.351375],
                [-1.973161, 3.927918, 0.292157],
                [-1.106739, 2.839449, 0.066697],
                [1.050535, 1.83432, -0.277272],
                [2.395382, 1.802082, -0.291358],
                [3.154882, 2.962981, -0.031715],
                [2.474689, 4.150985, 0.253731],
                [1.071925, 4.161548, 0.284024],
                [0.38245, 2.963161, 0.014971],
                [2.250483, -0.580998, -0.859162],
                [2.986054, 0.487084, -0.573372],
                [4.690796, 0.155642, -0.527752],
                [4.366931, -1.490301, -0.917992],
                [3.003666, -1.716978, -1.051681],
                [2.351112, -3.029328, -1.339872],
                [0.813861, -1.659551, 2.163461],
                [0.179509, -2.287688, 0.868737],
                [0.526151, -0.149611, 2.014347],
                [2.276932, -1.899656, 2.145771],
                [0.140413, -2.20862, 3.350508]
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.IMPLICIT,
            [
                [-0.106076, -0.278587, -0.33231],
                [-0.170725, -0.845567, -2.701124],
                [-2.392952, -1.000996, -0.486426],
                [-3.291283, -0.056813, -0.23467],
                [-4.918379, -0.662092, -0.151817],
                [-4.328168, -2.249065, -0.479436],
                [-2.947436, -2.25308, -0.629106],
                [-2.088135, -3.443012, -0.907209],
                [-1.595504, 1.597966, -0.098041],
                [-2.917344, 1.351959, -0.042436],
                [-3.844646, 2.389592, 0.185798],
                [-3.354127, 3.689685, 0.351375],
                [-1.973161, 3.927918, 0.292157],
                [-1.106739, 2.839449, 0.066697],
                [1.050535, 1.83432, -0.277272],
                [2.395382, 1.802082, -0.291358],
                [3.154882, 2.962981, -0.031715],
                [2.474689, 4.150985, 0.253731],
                [1.071925, 4.161548, 0.284024],
                [0.38245, 2.963161, 0.014971],
                [2.250483, -0.580998, -0.859162],
                [2.986054, 0.487084, -0.573372],
                [4.690796, 0.155642, -0.527752],
                [4.366931, -1.490301, -0.917992],
                [3.003666, -1.716978, -1.051681],
                [2.351112, -3.029328, -1.339872],
                [0.813861, -1.659551, 2.163461],
                [0.179509, -2.287688, 0.868737],
                [0.526151, -0.149611, 2.014347],
                [2.276932, -1.899656, 2.145771],
                [0.140413, -2.20862, 3.350508]
            ]
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.EXPLICIT,
            [
                [-1.339211, 0.079206, -0.361021],
                [-1.744384, 0.823097, -1.698982],
                [0.559518, 0.732394, -0.460712],
                [1.516895, -0.164342, -0.168083],
                [1.154659, -1.157481, 0.119291],
                [2.90283, 0.157426, -0.185692],
                [3.320158, 1.391493, -0.469124],
                [2.376961, 2.324297, -0.765855],
                [2.799199, 3.650707, -1.074667],
                [3.880389, 3.848117, -1.05108],
                [1.872429, 4.630681, -1.394268],
                [2.208925, 5.650806, -1.633517],
                [0.487955, 4.320418, -1.421837],
                [-0.241117, 5.1014, -1.684944],
                [0.036339, 3.039421, -1.12572],
                [-1.031931, 2.792453, -1.137741],
                [0.96603, 2.02406, -0.787066],
                [3.923759, -0.874277, 0.134255],
                [5.268974, -0.477148, 0.305625],
                [5.507142, 0.589631, 0.18947],
                [6.257812, -1.418227, 0.612165],
                [7.30034, -1.091163, 0.745735],
                [5.923774, -2.776275, 0.750256],
                [6.701448, -3.516888, 0.991332],
                [4.592027, -3.18401, 0.5748],
                [4.322548, -4.246559, 0.672439],
                [3.599212, -2.243241, 0.269404],
                [2.566489, -2.589355, 0.119258],
                [-0.720067, -1.536135, -1.415916],
                [-1.473484, -2.553912, -1.656886],
                [-2.829074, -2.692128, -1.288637],
                [-3.319993, -3.629708, -1.58175],
                [-3.624401, -1.759626, -0.582655],
                [-3.244489, -0.60747, -0.156795],
                [-0.778991, -3.659982, -2.415452],
                [-1.420678, -4.549804, -2.546439],
                [0.148179, -3.952308, -1.881655],
                [-0.468589, -3.287793, -3.413616],
                [-5.065466, -2.087428, -0.270177],
                [-5.22679, -2.028835, 0.825541],
                [-5.361494, -3.089165, -0.630204],
                [-5.725831, -1.324056, -0.730066],
                [-1.942958, 1.696523, 0.714257],
                [-1.881186, 1.769407, 2.002064],
                [-1.406143, 0.789375, 2.899225],
                [-1.434891, 1.067887, 3.961398],
                [-0.909096, -0.509849, 2.609263],
                [-0.801438, -1.030139, 1.448251],
                [-2.384951, 3.088818, 2.541952],
                [-2.341762, 3.142196, 3.64467],
                [-3.430143, 3.24845, 2.207404],
                [-1.78235, 3.915503, 2.112289],
                [-0.448627, -1.387902, 3.755284],
                [-1.00878, -2.344797, 3.730789],
                [-0.576437, -0.914149, 4.745726],
                [0.621489, -1.643369, 3.60997]
            ]
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            [
                [-1.339211, 0.079206, -0.361021],
                [-1.744384, 0.823097, -1.698982],
                [0.559518, 0.732394, -0.460712],
                [1.516895, -0.164342, -0.168083],
                [2.90283, 0.157426, -0.185692],
                [3.320158, 1.391493, -0.469124],
                [2.376961, 2.324297, -0.765855],
                [2.799199, 3.650707, -1.074667],
                [1.872429, 4.630681, -1.394268],
                [0.487955, 4.320418, -1.421837],
                [0.036339, 3.039421, -1.12572],
                [0.96603, 2.02406, -0.787066],
                [3.923759, -0.874277, 0.134255],
                [5.268974, -0.477148, 0.305625],
                [6.257812, -1.418227, 0.612165],
                [5.923774, -2.776275, 0.750256],
                [4.592027, -3.18401, 0.5748],
                [3.599212, -2.243241, 0.269404],
                [-0.720067, -1.536135, -1.415916],
                [-1.473484, -2.553912, -1.656886],
                [-2.829074, -2.692128, -1.288637],
                [-3.624401, -1.759626, -0.582655],
                [-3.244489, -0.60747, -0.156795],
                [-0.778991, -3.659982, -2.415452],
                [-5.065466, -2.087428, -0.270177],
                [-1.942958, 1.696523, 0.714257],
                [-1.881186, 1.769407, 2.002064],
                [-1.406143, 0.789375, 2.899225],
                [-0.909096, -0.509849, 2.609263],
                [-0.801438, -1.030139, 1.448251],
                [-2.384951, 3.088818, 2.541952],
                [-0.448627, -1.387902, 3.755284]
            ]
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.IMPLICIT,
            [
                [-1.339211, 0.079206, -0.361021],
                [-1.744384, 0.823097, -1.698982],
                [0.559518, 0.732394, -0.460712],
                [1.516895, -0.164342, -0.168083],
                [2.90283, 0.157426, -0.185692],
                [3.320158, 1.391493, -0.469124],
                [2.376961, 2.324297, -0.765855],
                [2.799199, 3.650707, -1.074667],
                [1.872429, 4.630681, -1.394268],
                [0.487955, 4.320418, -1.421837],
                [0.036339, 3.039421, -1.12572],
                [0.96603, 2.02406, -0.787066],
                [3.923759, -0.874277, 0.134255],
                [5.268974, -0.477148, 0.305625],
                [6.257812, -1.418227, 0.612165],
                [5.923774, -2.776275, 0.750256],
                [4.592027, -3.18401, 0.5748],
                [3.599212, -2.243241, 0.269404],
                [-0.720067, -1.536135, -1.415916],
                [-1.473484, -2.553912, -1.656886],
                [-2.829074, -2.692128, -1.288637],
                [-3.624401, -1.759626, -0.582655],
                [-3.244489, -0.60747, -0.156795],
                [-0.778991, -3.659982, -2.415452],
                [-5.065466, -2.087428, -0.270177],
                [-1.942958, 1.696523, 0.714257],
                [-1.881186, 1.769407, 2.002064],
                [-1.406143, 0.789375, 2.899225],
                [-0.909096, -0.509849, 2.609263],
                [-0.801438, -1.030139, 1.448251],
                [-2.384951, 3.088818, 2.541952],
                [-0.448627, -1.387902, 3.755284]
            ]
        ],

    ])
    def test_get_node_positions(self, file_path, hydrogen_mode, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default(hydrogen_mode=hydrogen_mode))

        # get result
        result = gg._get_node_positions(qm_data)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            0,
            False
        ],

        [
            TEST_FILE_LALMER,
            4,
            False
        ],

        [
            TEST_FILE_LALMER,
            20,
            False
        ],

        [
            TEST_FILE_LALMER,
            38,
            True
        ],

    ])
    def test_is_hydrogen(self, file_path, atom_index, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default())

        # get result
        result = gg._is_hydrogen(qm_data, atom_index)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            0,
            True
        ],

        [
            TEST_FILE_LALMER,
            4,
            False
        ],

        [
            TEST_FILE_LALMER,
            20,
            False
        ],

        [
            TEST_FILE_LALMER,
            38,
            False
        ],

        [
            TEST_FILE_OREDIA,
            0,
            True
        ],

    ])
    def test_is_metal(self, file_path, atom_index, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default())

        # get result
        result = gg._is_metal(qm_data, atom_index)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            [0, 29],
            False
        ],

        [
            TEST_FILE_LALMER,
            [25, 31],
            True
        ],

        [
            TEST_FILE_LALMER,
            [38, 39],
            True
        ],
    ])
    def test_is_hydrogen_bond(self, file_path, atom_indices, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default())

        # get result
        result = gg._is_hydrogen_bond(qm_data, atom_indices)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            [0, 12, 29],
            ValueError
        ]
    ])
    def test_is_hydrogen_bond_with_invalid_input(self, file_path, atom_indices, expected_error):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default())

        # get result
        self.assertRaises(expected_error, gg._is_hydrogen_bond, qm_data, atom_indices)

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            [0, 1],
            True
        ],

        [
            TEST_FILE_LALMER,
            [21, 22],
            False
        ],
    ])
    def test_is_metal_bond(self, file_path, atom_indices, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default())

        # get result
        result = gg._is_metal_bond(qm_data, atom_indices)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            [1, 9, 34],
            ValueError
        ]
    ])
    def test_is_metal_bond_with_invalid_input(self, file_path, atom_indices, expected_error):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default())

        # get result
        self.assertRaises(expected_error, gg._is_metal_bond, qm_data, atom_indices)

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            [1, 14, 23, 24],
            False
        ],

        [
            TEST_FILE_LALMER,
            [21, 22, 35, 42],
            True
        ],
    ])
    def test_contains_hydrogen(self, file_path, atom_indices, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default())

        # get result
        result = gg._contains_hydrogen(qm_data, atom_indices)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            [0, 14, 23, 24],
            True
        ],

        [
            TEST_FILE_LALMER,
            [21, 22, 35, 42],
            False
        ],
    ])
    def test_contains_metal(self, file_path, atom_indices, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default())

        # get result
        result = gg._contains_metal(qm_data, atom_indices)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            50,
            [0]
        ],

        [
            TEST_FILE_LALMER,
            54,
            [2]
        ],

        [
            TEST_FILE_LALMER,
            83,
            [5, 6]
        ],
    ])
    def test_get_atom_indices_from_nbo_id(self, file_path, nbo_id, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default())

        # get result
        result = gg._get_atom_indices_from_nbo_id(qm_data, nbo_id)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            50,
            0.5,
            [0]
        ],

        [
            TEST_FILE_LALMER,
            87,
            0.1,
            [7, 45]
        ],

        [
            TEST_FILE_LALMER,
            87,
            0.5,
            [7]
        ],

        [
            TEST_FILE_LALMER,
            87,
            0.8,
            []
        ],
    ])
    def test_select_atom_indices_from_nbo_id(self, file_path, nbo_id, sopa_contribution_threshold, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default(sopa_contribution_threshold=sopa_contribution_threshold))

        # get result
        result = gg._select_atom_indices_from_nbo_id(qm_data, nbo_id)

        self.assertEqual(result, expected)

    @parameterized.expand([

        # [
        #     TEST_FILE_LALMER,
        #     1,
        #     'CR'
        # ],

        [
            TEST_FILE_LALMER,
            57,
            'LP'
        ],

        [
            TEST_FILE_LALMER,
            76,
            'BD'
        ],

        [
            TEST_FILE_LALMER,
            131,
            'LV'
        ],

        [
            TEST_FILE_LALMER,
            135,
            'BD*'
        ],
    ])
    def test_get_nbo_type_from_nbo_id(self, file_path, nbo_id, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default())

        # get result
        result = gg._get_nbo_type_from_nbo_id(qm_data, nbo_id)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [
            [[1.1], [1.5, 1.2, 1.9], [1.2, 1.2], [1.5, 2.3]],
            SopaResolutionMode.FULL,
            [[1.1], [1.5, 1.2, 1.9], [1.2, 1.2], [1.5, 2.3]]
        ],

        [
            [[1.1], [1.5, 1.2, 1.9], [1.2, 1.2], [1.5, 2.3]],
            SopaResolutionMode.AVERAGE,
            [[1.1], [1.53333333], [1.2], [1.9]]
        ],

        [
            [[1.1], [1.5, 1.2, 1.9], [1.2, 1.2], [1.5, 2.3]],
            SopaResolutionMode.MIN_MAX,
            [[1.1], [1.2, 1.9], [1.2, 1.2], [1.5, 2.3]]
        ],

        [
            [[1.1], [1.5, 1.2, 1.9], [1.2, 1.2], [1.5, 2.3]],
            SopaResolutionMode.MAX,
            [[1.1], [1.9], [1.2], [2.3]]
        ],

    ])
    def test_resolve_stabilisation_energies(self, stabilisation_energies, sopa_resolution_mode, expected):

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default(sopa_resolution_mode=sopa_resolution_mode))

        # get result
        result = gg._resolve_stabilisation_energies(stabilisation_energies, sopa_resolution_mode)

        Utils.assert_are_almost_equal(result, expected, places=5)

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            1,
            (
                [[1, 0], [2, 0], [8, 0], [14, 0], [20, 0], [27, 0], [28, 0], [29, 0], [30, 0]],
                [[0.58, 15.10], [25.68], [22.74], [21.99], [23.34], [7.2, 0.28, 16.63], [6.79, 0.19, 12.43], [0.33], [0.2]],
                [['LP', 'LV'], ['LP', 'LV'], ['LP', 'LV'], ['LP', 'LV'], ['LP', 'LV'], ['LP', 'LV'], ['LP', 'LV'], ['LP', 'LV'], ['LP', 'LV']]
            )
        ],

        [
            TEST_FILE_LALMER,
            0.7,
            (
                [[0, 33], [1, 0], [1, 0], [2, 0], [8, 0], [14, 0], [20, 0], [27, 0], [28, 0], [29, 0], [30, 0]],
                [[0.12], [0.58, 15.10], [1.58, 1.32], [25.68], [22.74], [21.99], [23.34], [7.2, 0.28, 16.63], [6.79, 0.19, 12.43], [0.33], [0.2]],
                [['LP', 'BD*'], ['LP', 'LV'], ['BD', 'LV'], ['LP', 'LV'], ['LP', 'LV'], ['LP', 'LV'], ['LP', 'LV'], ['LP', 'LV'], ['LP', 'LV'], ['LP', 'LV'], ['LP', 'LV']]
            )
        ],

    ])
    def test_get_sopa_adjacency_list(self, file_path, sopa_contribution_threshold, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default(sopa_contribution_threshold=sopa_contribution_threshold))

        # get result
        result = gg._get_sopa_adjacency_list(qm_data)

        Utils.assert_are_almost_equal(result, expected, places=5)

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            10,
            [],
            [SopaEdgeFeature.STABILISATION_ENERGY_MAX, SopaEdgeFeature.DONOR_NBO_TYPE, SopaEdgeFeature.ACCEPTOR_NBO_TYPE],
            [
                Edge([1, 0], [15.10, 'LP', 'LV'], is_directed=True),
                Edge([2, 0], [25.68, 'LP', 'LV'], is_directed=True),
                Edge([8, 0], [22.74, 'LP', 'LV'], is_directed=True),
                Edge([14, 0], [21.99, 'LP', 'LV'], is_directed=True),
                Edge([20, 0], [23.34, 'LP', 'LV'], is_directed=True),
                Edge([27, 0], [16.63, 'LP', 'LV'], is_directed=True),
                Edge([28, 0], [12.43, 'LP', 'LV'], is_directed=True)
            ]
        ],

        [
            TEST_FILE_LALMER,
            20,
            [EdgeFeature.WIBERG_BOND_ORDER],
            [SopaEdgeFeature.STABILISATION_ENERGY_MAX, SopaEdgeFeature.DONOR_NBO_TYPE, SopaEdgeFeature.ACCEPTOR_NBO_TYPE],
            [
                Edge([2, 0], [25.68, 'LP', 'LV', 0.0936], is_directed=True),
                Edge([8, 0], [22.74, 'LP', 'LV', 0.0752], is_directed=True),
                Edge([14, 0], [21.99, 'LP', 'LV', 0.0723], is_directed=True),
                Edge([20, 0], [23.34, 'LP', 'LV', 0.0864], is_directed=True),
            ]
        ],

        [
            TEST_FILE_LALMER,
            10,
            [],
            [SopaEdgeFeature.STABILISATION_ENERGY_AVERAGE],
            [
                Edge([1, 0], [7.84], is_directed=True),
                Edge([2, 0], [25.68], is_directed=True),
                Edge([8, 0], [22.74], is_directed=True),
                Edge([14, 0], [21.99], is_directed=True),
                Edge([20, 0], [23.34], is_directed=True),
                Edge([27, 0], [8.036666], is_directed=True),
                Edge([28, 0], [6.47], is_directed=True)
            ]
        ],

    ])
    def test_get_sopa_edges(self, file_path, sopa_interaction_threshold, edge_features, sopa_edge_features, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default(edge_features=edge_features,
                                                           sopa_edge_features=sopa_edge_features,
                                                           sopa_contribution_threshold=1,
                                                           sopa_resolution_mode=SopaResolutionMode.MAX,
                                                           sopa_interaction_threshold=sopa_interaction_threshold))

        # get result
        result = gg._get_sopa_edges(qm_data)
        print(result)

        Utils.assert_are_almost_equal(result, expected, places=5)

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            [0.3458798245614035, 0.6517228070175439, 0.0020701754385964913, 0.0003280701754385965],
        ],

        [
            TEST_FILE_OREDIA,
            [0.3929666666666667, 0.59919318181818184, 0.007556818181818182, 0.00029015151515151515],
        ],

    ])
    def test_get_average_orbital_occupations(self, file_path, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default())

        result = gg._get_average_orbital_occupations(qm_data.bond_pair_data)

        Utils.assert_are_almost_equal(result, expected)

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            [NodeFeature.LONE_PAIR_S, NodeFeature.LONE_PAIR_P],
            [],
            OrbitalOccupationType.LONE_PAIR,
            [0.0, 0.0],
        ],

        [
            TEST_FILE_LALMER,
            [NodeFeature.LONE_VACANCY_P, NodeFeature.LONE_VACANCY_F],
            [],
            OrbitalOccupationType.LONE_VACANCY,
            [0.0, 0.0],
        ],

        [
            TEST_FILE_LALMER,
            [],
            [EdgeFeature.BOND_ORBITAL_DATA_S, EdgeFeature.BOND_ORBITAL_DATA_P, EdgeFeature.BOND_ORBITAL_DATA_D],
            OrbitalOccupationType.BOND_ORBITAL,
            [0.3458798245614035, 0.6517228070175439, 0.0020701754385964913],
        ],

        [
            TEST_FILE_LALMER,
            [],
            [EdgeFeature.ANTIBOND_ORBITAL_DATA_S, EdgeFeature.ANTIBOND_ORBITAL_DATA_F],
            OrbitalOccupationType.ANTIBOND_ORBITAL,
            [0.3458798245614035, 0.0003280701754385965],
        ],

    ])
    def test_get_default_orbital_occupations(self, file_path, node_features, edge_features, orbital_occupation_type, expected):

        # load data
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(file_path))

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default(node_features, edge_features))

        result = gg._get_default_orbital_occupations(qm_data, orbital_occupation_type)

        Utils.assert_are_almost_equal(result, expected)
