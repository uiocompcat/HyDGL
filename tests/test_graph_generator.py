import unittest
from parameterized import parameterized

from nbo2graph.data_parser import DataParser
from nbo2graph.enums.edge_feature import EdgeFeature
from nbo2graph.enums.node_feature import NodeFeature
from nbo2graph.enums.graph_feature import GraphFeature
from nbo2graph.enums.hydrogen_mode import HydrogenMode
from nbo2graph.enums.qm_target import QmTarget
from nbo2graph.graph_generator import GraphGenerator
from nbo2graph.enums.bond_determination_mode import BondDeterminationMode
from nbo2graph.graph_generator_settings import GraphGeneratorSettings
from tests.utils import Utils

# constants pointing to test files
TEST_FILE_LALMER = './tests/files/LALMER.out'
TEST_FILE_OREDIA = './tests/files/OREDIA.out'


class TestGraphGenerator(unittest.TestCase):

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            HydrogenMode.EXPLICIT,
            BondDeterminationMode.WIBERG,
            [NodeFeature.ATOMIC_NUMBERS],
            [
                [48], [8], [7], [6], [16], [6], [6], [6], [7], [6], [6], [6], [6], [6], [7], [6],
                [6], [6], [6], [6], [7], [6], [16], [6], [6], [6], [17], [8], [8], [8], [8], [1],
                [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1]
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.OMIT,
            BondDeterminationMode.WIBERG,
            [NodeFeature.ATOMIC_NUMBERS],
            [
                [48], [8], [7], [6], [16], [6], [6], [6], [7], [6], [6], [6], [6], [6], [7], [6],
                [6], [6], [6], [6], [7], [6], [16], [6], [6], [6], [17], [8], [8], [8], [8]
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.IMPLICIT,
            BondDeterminationMode.WIBERG,
            [NodeFeature.ATOMIC_NUMBERS],
            [
                [48, 0], [8, 2], [7, 0], [6, 0], [16, 0], [6, 1], [6, 0], [6, 3], [7, 0], [6, 0],
                [6, 1], [6, 1], [6, 1], [6, 0], [7, 0], [6, 0], [6, 1], [6, 1], [6, 1], [6, 0],
                [7, 0], [6, 0], [16, 0], [6, 1], [6, 0], [6, 3], [17, 0], [8, 0], [8, 0], [8, 0],
                [8, 0]
            ]
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            BondDeterminationMode.WIBERG,
            [NodeFeature.ATOMIC_NUMBERS],
            [
                [77], [1], [7], [6], [6], [7], [6], [6], [6], [6], [6], [6], [6], [6], [6], [6],
                [6], [6], [8], [6], [6], [6], [8], [6], [6], [8], [6], [6], [6], [8], [6], [6]
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.EXPLICIT,
            BondDeterminationMode.WIBERG,
            [NodeFeature.WIBERG_BOND_ORDER_TOTAL],
            [
                [0.5922], [1.5640], [3.1352], [4.0037], [2.7551], [3.9207], [3.9888], [3.8371],
                [3.1270], [3.9977], [3.9509], [3.9440], [3.9536], [3.9935], [3.1278], [3.9975],
                [3.9509], [3.9445], [3.9542], [3.9953], [3.1300], [4.0056], [2.7623], [3.9225],
                [3.9905], [3.8393], [4.5847], [1.4772], [1.5452], [1.7228], [1.7681], [0.7499],
                [0.9248], [0.7511], [0.9401], [0.9277], [0.9395], [0.9432], [0.9423], [0.9257],
                [0.9439], [0.9392], [0.9400], [0.9473], [0.9272], [0.9445], [0.9420]
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.EXPLICIT,
            BondDeterminationMode.NLMO,
            [NodeFeature.NLMO_BOND_ORDER_TOTAL],
            [
                [0.5744], [1.022], [2.2828], [3.3946], [1.9874], [3.3227], [3.5845], [3.1819],
                [2.2794], [3.5223], [3.5658], [3.7724], [3.5903], [3.7262], [2.2683], [3.532],
                [3.5804], [3.7722], [3.5926], [3.7325], [2.27], [3.3969], [1.993], [3.3239],
                [3.5949], [3.1929], [4.1104], [0.7012], [0.7221], [0.7784], [0.8416], [0.498],
                [0.7029], [0.4975], [0.755], [0.7378], [0.744], [0.7555], [0.7705], [0.7003],
                [0.7588], [0.7436], [0.7536], [0.7619], [0.735], [0.7559], [0.7702]
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.EXPLICIT,
            BondDeterminationMode.WIBERG,
            [NodeFeature.NATURAL_ATOMIC_CHARGES],
            [
                [1.68876], [-0.97287], [-0.5208], [-0.00055], [0.50384], [-0.42569], [0.16518],
                [-0.67147], [-0.49808], [0.15474], [-0.20643], [-0.14183], [-0.20915], [0.18],
                [-0.49346], [0.16092], [-0.20272], [-0.14315], [-0.20931], [0.17315], [-0.52989],
                [0.00237], [0.50834], [-0.42223], [0.1705], [-0.67088], [2.36189], [-0.9251],
                [-0.87318], [-0.75172], [-0.7181], [0.50206], [0.27661], [0.50076], [0.24647],
                [0.27044], [0.24758], [0.24012], [0.24114], [0.27532], [0.23865], [0.2482],
                [0.24659], [0.23192], [0.27127], [0.23798], [0.24182]
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.EXPLICIT,
            BondDeterminationMode.WIBERG,
            [NodeFeature.NATURAL_ELECTRON_CONFIGURATION_S, NodeFeature.NATURAL_ELECTRON_CONFIGURATION_P, NodeFeature.NATURAL_ELECTRON_CONFIGURATION_D, NodeFeature.NATURAL_ELECTRON_CONFIGURATION_F],
            [
                [0.31, 0.01, 9.98, 0], [1.75, 5.21, 0.01, 0], [1.37, 4.13, 0.01, 0], [0.97, 3.01, 0.01, 0],
                [1.65, 3.82, 0.03, 0], [1.10, 3.32, 0.01, 0], [0.91, 2.92, 0, 0], [1.13, 3.53, 0.01, 0],
                [1.34, 4.14, 0.01, 0], [0.89, 2.94, 0, 0], [1.00, 3.2, 0, 0], [1.00, 3.13, 0, 0],
                [1.00, 3.2, 0, 0], [0.89, 2.91, 0, 0], [1.34, 4.13, 0.01, 0], [0.89, 2.94, 0, 0],
                [1.00, 3.2, 0, 0], [1.00, 3.13, 0, 0], [1.00, 3.2, 0, 0], [0.89, 2.92, 0, 0],
                [1.37, 4.14, 0.02, 0], [0.96, 3.01, 0.01, 0], [1.65, 3.82, 0.03, 0], [1.10, 3.31, 0.01, 0],
                [0.91, 2.91, 0, 0], [1.13, 3.53, 0.01, 0], [1.25, 3.08, 0.3, 0.01], [1.89, 5.01, 0.02, 0],
                [1.89, 4.96, 0.02, 0], [1.87, 4.85, 0.02, 0], [1.87, 4.82, 0.02, 0], [0.5, 0, 0, 0],
                [0.72, 0, 0, 0], [0.5, 0, 0, 0], [0.75, 0, 0, 0], [0.73, 0, 0, 0], [0.75, 0, 0, 0], [0.76, 0, 0, 0],
                [0.76, 0, 0, 0], [0.72, 0, 0, 0], [0.76, 0, 0, 0], [0.75, 0, 0, 0], [0.75, 0, 0, 0], [0.77, 0, 0, 0],
                [0.73, 0, 0, 0], [0.76, 0, 0, 0], [0.76, 0, 0, 0]
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.OMIT,
            BondDeterminationMode.WIBERG,
            [NodeFeature.LONE_PAIR_MAX, NodeFeature.LONE_PAIRS_S, NodeFeature.LONE_PAIRS_P, NodeFeature.LONE_PAIRS_D, NodeFeature.LONE_PAIRS_F],
            [
                [5, -0.62573, 1.99593, 0.0001, 0.0, 0.9998, 0.0],
                [2, -0.56001, 1.99619, 0.1619, 0.8369, 0.0011, 0.0],
                [1, -0.50043, 1.86184, 0.3127, 0.6867, 0.0005, 0.0],
                [0, 0, 0, 0, 0, 0, 0],
                [2, -0.37741, 1.55738, 0.0, 0.9979, 0.002, 0.0001],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [1, -0.48921, 1.87884, 0.2791, 0.7203, 0.0005, 0.0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [1, -0.48483, 1.87975, 0.2796, 0.7198, 0.0006, 0.0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [1, -0.49310, 1.86490, 0.3133, 0.6860, 0.0006, 0.0],
                [0, 0, 0, 0, 0, 0, 0],
                [2, -0.36939, 1.55195, 0.0001, 0.9978, 0.002, 0.0001],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [3, -0.41714, 1.88616, 0.0003, 0.9976, 0.002, 0.0001],
                [3, -0.4117, 1.86643, 0.0002, 0.9972, 0.0025, 0.0001],
                [3, -0.4003, 1.79398, 0.0, 0.9964, 0.0035, 0.0001],
                [3, -0.39761, 1.77785, 0.0, 0.9961, 0.0038, 0.0001]
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.OMIT,
            BondDeterminationMode.WIBERG,
            [NodeFeature.LONE_PAIR_AVERAGE, NodeFeature.LONE_PAIRS_S, NodeFeature.LONE_PAIRS_P, NodeFeature.LONE_PAIRS_D, NodeFeature.LONE_PAIRS_F],
            [
                [5, -0.627936, 1.996892, 0.00014, 0, 0.99984, 0],
                [2, -0.61476, 1.9834, 0.26065, 0.73855, 0.00075, 0],
                [1, -0.50043, 1.86184, 0.3127, 0.6867, 0.0005, 0.0],
                [0, 0, 0, 0, 0, 0, 0],
                [2, -0.51211, 1.76919, 0.32825, 0.6705, 0.0012, 0.00005],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [1, -0.48921, 1.87884, 0.2791, 0.7203, 0.0005, 0.0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [1, -0.48483, 1.87975, 0.2796, 0.7198, 0.0006, 0.0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [1, -0.49310, 1.86490, 0.3133, 0.6860, 0.0006, 0.0],
                [0, 0, 0, 0, 0, 0, 0],
                [2, -0.504135, 1.766285, 0.32715, 0.6716, 0.0012, 0.00005],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [3, -0.5798866, 1.91078, 0.2991, 0.6994333, 0.0014, 0.0000333],
                [3, -0.5712033, 1.89843666666667, 0.2962666, 0.7019, 0.0017666, 0.0000666],
                [3, -0.55052, 1.863, 0.2877333, 0.70986666, 0.002333, 0.00006666],
                [3, -0.5467866, 1.85364, 0.2865666, 0.7108333, 0.0025333, 0.0000666]
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.OMIT,
            BondDeterminationMode.WIBERG,
            [NodeFeature.LONE_VACANCY_MIN, NodeFeature.LONE_VACANCIES_S, NodeFeature.LONE_VACANCIES_P, NodeFeature.LONE_VACANCIES_D, NodeFeature.LONE_VACANCIES_F],
            [
                [1, -0.04626, 0.30391, 0.9988, 0.0002, 0.001, 0.0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]
            ]
        ],

        [
            TEST_FILE_LALMER,
            HydrogenMode.OMIT,
            BondDeterminationMode.WIBERG,
            [NodeFeature.LONE_VACANCY_AVERAGE, NodeFeature.LONE_VACANCIES_S, NodeFeature.LONE_VACANCIES_P, NodeFeature.LONE_VACANCIES_D, NodeFeature.LONE_VACANCIES_F],
            [
                [1, -0.04626, 0.30391, 0.9988, 0.0002, 0.001, 0.0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]
            ]
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            BondDeterminationMode.WIBERG,
            [NodeFeature.LONE_VACANCY_MIN, NodeFeature.LONE_VACANCIES_S, NodeFeature.LONE_VACANCIES_P, NodeFeature.LONE_VACANCIES_D, NodeFeature.LONE_VACANCIES_F],
            [
                [2, -0.16639, 0.76906, 0.0015, 0.0001, 0.9984, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [1, -0.12926, 0.9643, 0, 00.9995, 0, 0.0005],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]
            ]
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            BondDeterminationMode.WIBERG,
            [NodeFeature.LONE_VACANCY_AVERAGE, NodeFeature.LONE_VACANCIES_S, NodeFeature.LONE_VACANCIES_P, NodeFeature.LONE_VACANCIES_D, NodeFeature.LONE_VACANCIES_F],
            [
                [2, 0.4279, 0.570795, 0.43415, 0.0003, 0.5655, 0.00005],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [1, -0.12926, 0.9643, 0, 00.9995, 0, 0.0005],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]
            ]
        ],

    ])
    def test_get_nodes(self, file_path, hydrogen_mode, bond_determination_mode, node_features, expected):

        # load data
        qm_data = DataParser(file_path).parse()

        # set up graph generator settings
        ggs = GraphGeneratorSettings(node_features=node_features,
                                     edge_features=[],
                                     hydrogen_mode=hydrogen_mode,
                                     bond_determination_mode=bond_determination_mode)

        # set up graph generator with variable node feature list
        gg = GraphGenerator(ggs)

        # get nodes
        result = gg._get_nodes(qm_data)

        print(result)

        # test
        Utils.assert_are_almost_equal(result, expected, places=3)

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
            HydrogenMode.OMIT,
            BondDeterminationMode.NLMO,
            [NodeFeature.ATOMIC_NUMBERS, NodeFeature.NLMO_BOND_ORDER_TOTAL],
            4,
            [16, 1.9874]
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.IMPLICIT,
            BondDeterminationMode.NLMO,
            [],
            0,
            [0]
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            BondDeterminationMode.NLMO,
            [NodeFeature.NATURAL_ATOMIC_CHARGES],
            1,
            [-0.05261]
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            BondDeterminationMode.NLMO,
            [NodeFeature.LONE_PAIR_ENERGY_MIN_MAX_DIFFERENCE],
            0,
            [3, 0.00634]
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            BondDeterminationMode.NLMO,
            [NodeFeature.LONE_PAIR_ENERGY_MIN_MAX_DIFFERENCE],
            2,
            [1, 0]
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            BondDeterminationMode.NLMO,
            [NodeFeature.LONE_PAIR_ENERGY_MIN_MAX_DIFFERENCE],
            1,
            [0, 0]
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            BondDeterminationMode.NLMO,
            [NodeFeature.LONE_VACANCY_ENERGY_MIN_MAX_DIFFERENCE],
            0,
            [2, 1.18858]
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            BondDeterminationMode.NLMO,
            [NodeFeature.LONE_VACANCY_ENERGY_MIN_MAX_DIFFERENCE],
            7,
            [1, 0]
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            BondDeterminationMode.NLMO,
            [NodeFeature.LONE_VACANCY_ENERGY_MIN_MAX_DIFFERENCE],
            1,
            [0, 0]
        ],

        [
            TEST_FILE_OREDIA,
            HydrogenMode.OMIT,
            BondDeterminationMode.NLMO,
            [NodeFeature.LONE_PAIR_ENERGY_MIN_MAX_DIFFERENCE, NodeFeature.LONE_VACANCY_ENERGY_MIN_MAX_DIFFERENCE],
            0,
            [3, 0.00634, 2, 1.18858]
        ],

    ])
    def test_get_individual_node(self, file_path, hydrogen_mode, bond_determination_mode, node_features, atom_index, expected):

        # load data
        qm_data = DataParser(file_path).parse()

        # set up graph generator settings
        ggs = GraphGeneratorSettings(node_features=node_features,
                                     edge_features=[],
                                     hydrogen_mode=hydrogen_mode,
                                     bond_determination_mode=bond_determination_mode)

        # set up graph generator with variable node feature list
        gg = GraphGenerator(ggs)

        # get nodes
        result = gg._get_individual_node(qm_data, atom_index)

        Utils.assert_are_almost_equal(result, expected, places=3)

    @parameterized.expand([

        [
            HydrogenMode.EXPLICIT,
            BondDeterminationMode.WIBERG,
            [EdgeFeature.WIBERG_BOND_ORDER],
            1,
            [
                [[2, 3], [1.4785]], [[2, 6], [1.2435]], [[3, 4], [1.2259]], [[3, 9], [1.0752]],
                [[4, 5], [1.2267]], [[5, 6], [1.5581]], [[6, 7], [1.0438]], [[8, 9], [1.3553]],
                [[8, 13], [1.3698]], [[9, 10], [1.3595]], [[10, 11], [1.4483]], [[11, 12], [1.4358]],
                [[12, 13], [1.3751]], [[13, 19], [1.0384]], [[14, 15], [1.3568]], [[14, 19], [1.3691]],
                [[15, 16], [1.3538]], [[15, 21], [1.0775]], [[16, 17], [1.4541]], [[17, 18], [1.4305]],
                [[18, 19], [1.3784]], [[20, 21], [1.4728]], [[20, 24], [1.2457]], [[21, 22], [1.2279]],
                [[22, 23], [1.2305]], [[23, 24], [1.554]], [[24, 25], [1.0439]], [[26, 28], [1.0553]],
                [[26, 29], [1.2463]], [[26, 30], [1.2875]]
            ]
        ],

        [
            HydrogenMode.EXPLICIT,
            BondDeterminationMode.WIBERG,
            [EdgeFeature.BOND_DISTANCE],
            1,
            [
                [[2, 3], [1.327352]], [[2, 6], [1.376780]], [[3, 4], [1.738008]], [[3, 9], [1.470177]],
                [[4, 5], [1.724577]], [[5, 6], [1.388826]], [[6, 7], [1.493880]], [[8, 9], [1.345686]],
                [[8, 13], [1.344363]], [[9, 10], [1.410199]], [[10, 11], [1.399380]], [[11, 12], [1.402615]],
                [[12, 13], [1.409355]], [[13, 19], [1.495214]], [[14, 15], [1.345307]], [[14, 19], [1.343885]],
                [[15, 16], [1.411362]], [[15, 21], [1.468893]], [[16, 17], [1.398391]], [[17, 18], [1.403130]],
                [[18, 19], [1.408509]], [[20, 21], [1.327983]], [[20, 24], [1.376516]], [[21, 22], [1.737262]],
                [[22, 23], [1.722296]], [[23, 24], [1.388434]], [[24, 25], [1.493701]], [[26, 28], [1.544322]],
                [[26, 29], [1.482748]], [[26, 30], [1.471084]]
            ]
        ],

        [
            HydrogenMode.EXPLICIT,
            BondDeterminationMode.WIBERG,
            [EdgeFeature.BOND_ORBITAL_MAX, EdgeFeature.BOND_ORBITAL_DATA_D],
            1,
            [
                [[2, 3], [2, -0.47335, 1.86181, 0.00125]], [[2, 6], [1, -0.83628, 1.98204, 0.0024]], [[3, 4], [1, -0.71751, 1.97740, 0.0048]], [[3, 9], [1, -0.75230, 1.97911, 0.00075]],
                [[4, 5], [1, -0.70950, 1.97628, 0.0055]], [[5, 6], [2, -0.40546, 1.80326, 0.0011]], [[6, 7], [1, -0.68826, 1.98282, 0.0011]], [[8, 9], [2, -0.46423, 1.73906, 0.00115]],
                [[8, 13], [1, -0.87779, 1.98407, 0.0021]], [[9, 10], [1, -0.75976, 1.98302, 0.0011]], [[10, 11], [2, -0.39926, 1.61498, 0.00055]], [[11, 12], [1, -0.75330, 1.98387, 0.00135]],
                [[12, 13], [2, -0.40128, 1.58771, 0.0003]], [[13, 19], [1, -0.72173, 1.97437, 0.0007]], [[14, 15], [2, -0.45893, 1.73616, 0.00115]], [[14, 19], [1, -0.87405, 1.98390, 0.0021]],
                [[15, 16], [1, -0.75425, 1.98305, 0.00105]], [[15, 21], [1, -0.74646, 1.97899, 0.00075]], [[16, 17], [2, -0.39528, 1.61781, 0.00055]], [[17, 18], [1, -0.74945, 1.98371, 0.00135]],
                [[18, 19], [2, -0.39886, 1.59508, 0.0003]], [[20, 21], [2, -0.46620, 1.86014, 0.00085]], [[20, 24], [1, -0.82945, 1.98174, 0.0024]], [[21, 22], [1, -0.71051, 1.97741, 0.0048]],
                [[22, 23], [1, -0.70280, 1.97615, 0.00545]], [[23, 24], [2, -0.39736, 1.79809, 0.0011]], [[24, 25], [1, -0.68261, 1.98279, 0.00105]], [[26, 28], [1, -0.92396, 1.98066, 0.01155]],
                [[26, 29], [1, -0.97513, 1.98174, 0.0112]], [[26, 30], [1, -0.98492, 1.98216, 0.011]]
            ]
        ],
    ])
    def test_get_edges(self, hydrogen_mode, bond_determination_mode, edge_features, bond_threshold, expected):

        # load data
        qm_data = DataParser(TEST_FILE_LALMER).parse()

        # set up graph generator settings
        ggs = GraphGeneratorSettings(node_features=[],
                                     edge_features=edge_features,
                                     hydrogen_mode=hydrogen_mode,
                                     bond_determination_mode=bond_determination_mode,
                                     bond_threshold=bond_threshold)

        # set up graph generator with variable node feature list
        gg = GraphGenerator(ggs)

        # get edges
        result = gg._get_edges(qm_data)

        # compare to expected
        print(result)
        print()
        print(expected)
        Utils.assert_are_almost_equal(result, expected, places=3)

    @parameterized.expand([

        [0, 0.1, []],

        [11, 0.1, [10, 12, 41]],

    ])
    def test_get_bound_atom_indices(self, atom_index, threshold, expected):

        # load data
        qm_data = DataParser(TEST_FILE_LALMER).parse()

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
        qm_data = DataParser(TEST_FILE_LALMER).parse()

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
        qm_data = DataParser(TEST_FILE_LALMER).parse()

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
        qm_data = DataParser(TEST_FILE_LALMER).parse()

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
        qm_data = DataParser(TEST_FILE_LALMER).parse()

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
        qm_data = DataParser(TEST_FILE_LALMER).parse()

        # set up graph generator settings
        ggs = GraphGeneratorSettings(graph_features=graph_features)

        # set up graph generator (default values)
        gg = GraphGenerator(ggs)

        # get result
        result = gg._get_graph_features(qm_data)

        self.assertEqual(result, expected)

    @parameterized.expand([

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
        qm_data = DataParser(file_path).parse()

        # set up graph generator settings
        ggs = GraphGeneratorSettings(targets=targets)

        # set up graph generator (default values)
        gg = GraphGenerator(ggs)

        # get result
        result = gg._get_targets(qm_data)

        Utils.assert_are_almost_equal(result, expected, places=5)

    @parameterized.expand([

        [
            BondDeterminationMode.WIBERG,
            1,
            [
                [2, 3], [2, 6], [3, 4], [3, 9], [4, 5], [5, 6], [6, 7],
                [8, 9], [8, 13], [9, 10], [10, 11], [11, 12], [12, 13],
                [13, 19], [14, 15], [14, 19], [15, 16], [15, 21], [16, 17],
                [17, 18], [18, 19], [20, 21], [20, 24], [21, 22], [22, 23],
                [23, 24], [24, 25], [26, 28], [26, 29], [26, 30]
            ]
        ],

    ])
    def test_get_adjacency_list(self, bond_determination_mode, bond_threshold, expected):

        # load data
        qm_data = DataParser(TEST_FILE_LALMER).parse()

        # set up graph generator settings
        ggs = GraphGeneratorSettings(bond_determination_mode=bond_determination_mode, bond_threshold=bond_threshold)

        # set up graph generator (default values)
        gg = GraphGenerator(ggs)

        # get result
        result = gg._get_adjacency_list(qm_data)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [
            [15, 21],
            [EdgeFeature.BOND_ORBITAL_MAX, EdgeFeature.BOND_DISTANCE, EdgeFeature.BOND_ORBITAL_DATA_S],
            [[15, 21], [1.468893, 1, -0.74646, 1.97899, 0.34105]]
        ],

        [
            [15, 21],
            [EdgeFeature.BOND_ORBITAL_AVERAGE, EdgeFeature.BOND_DISTANCE, EdgeFeature.BOND_ORBITAL_DATA_S],
            [[15, 21], [1.468893, 1, -0.74646, 1.97899, 0.34105]]
        ],

        [
            [2, 3],
            [EdgeFeature.BOND_ORBITAL_MAX, EdgeFeature.BOND_ORBITAL_DATA_S, EdgeFeature.BOND_ORBITAL_DATA_P, EdgeFeature.BOND_ORBITAL_DATA_D, EdgeFeature.  BOND_ORBITAL_DATA_F],
            [[2, 3], [2, -0.47335, 1.86181, 0, 0.9983, 0.00125, 0.0004]]
        ],

        [
            [2, 3],
            [EdgeFeature.BOND_ORBITAL_AVERAGE, EdgeFeature.BOND_ORBITAL_DATA_S, EdgeFeature.BOND_ORBITAL_DATA_P, EdgeFeature.BOND_ORBITAL_DATA_D, EdgeFeature.  BOND_ORBITAL_DATA_F],
            [[2, 3], [2, -0.68039, 1.924115, 0.174625, 0.823025, 0.00195, 0.00035]]
        ],

        [
            [2, 3],
            [EdgeFeature.ANTIBOND_ORBITAL_MIN, EdgeFeature.ANTIBOND_ORBITAL_DATA_S, EdgeFeature.ANTIBOND_ORBITAL_DATA_P, EdgeFeature.ANTIBOND_ORBITAL_DATA_D, EdgeFeature.ANTIBOND_ORBITAL_DATA_F],
            [[2, 3], [2, -0.15285, 0.47234, 0, 0.9983, 0.00125, 0.0004]]
        ],

        [
            [2, 3],
            [EdgeFeature.ANTIBOND_ORBITAL_AVERAGE, EdgeFeature.ANTIBOND_ORBITAL_DATA_S, EdgeFeature.ANTIBOND_ORBITAL_DATA_P, EdgeFeature.ANTIBOND_ORBITAL_DATA_D, EdgeFeature.ANTIBOND_ORBITAL_DATA_F],
            [[2, 3], [2, 0.110375, 0.247345, 0.174625, 0.823025, 0.00195, 0.00035]]
        ],

        [
            [2, 3],
            [EdgeFeature.ANTIBOND_ORBITAL_MIN, EdgeFeature.ANTIBOND_ORBITAL_AVERAGE, EdgeFeature.ANTIBOND_ORBITAL_DATA_S, EdgeFeature.ANTIBOND_ORBITAL_DATA_P, EdgeFeature.ANTIBOND_ORBITAL_DATA_D, EdgeFeature.ANTIBOND_ORBITAL_DATA_F],
            [[2, 3], [2, -0.15285, 0.47234, 0, 0.9983, 0.00125, 0.0004, 0.110375, 0.247345, 0.174625, 0.823025, 0.00195, 0.00035]]
        ],

        [
            [0, 5],
            [EdgeFeature.ANTIBOND_ORBITAL_AVERAGE, EdgeFeature.ANTIBOND_ORBITAL_DATA_S, EdgeFeature.ANTIBOND_ORBITAL_DATA_P, EdgeFeature.ANTIBOND_ORBITAL_DATA_D, EdgeFeature.ANTIBOND_ORBITAL_DATA_F],
            [[0, 5], [0, 0, 0, 0, 0, 0, 0]]
        ],

        [
            [2, 3],
            [EdgeFeature.BOND_ENERGY_MIN_MAX_DIFFERENCE],
            [[2, 3], [2, 0.41408]]
        ],

        [
            [2, 3],
            [EdgeFeature.ANTIBOND_ENERGY_MIN_MAX_DIFFERENCE],
            [[2, 3], [2, 0.52645]]
        ],

        [
            [0, 5],
            [EdgeFeature.BOND_ENERGY_MIN_MAX_DIFFERENCE],
            [[0, 5], [0, 0]]
        ],

        [
            [0, 5],
            [EdgeFeature.ANTIBOND_ENERGY_MIN_MAX_DIFFERENCE],
            [[0, 5], [0, 0]]
        ],

        [
            [2, 3],
            [EdgeFeature.BOND_ENERGY_MIN_MAX_DIFFERENCE, EdgeFeature.ANTIBOND_ENERGY_MIN_MAX_DIFFERENCE],
            [[2, 3], [2, 0.41408, 0.52645]]
        ],

        [
            [2, 6],
            [EdgeFeature.BOND_ENERGY_MIN_MAX_DIFFERENCE],
            [[2, 6], [1, 0]]
        ],

    ])
    def test_get_featurised_edge(self, bond_indices, edge_features, expected):

        # load data
        qm_data = DataParser(TEST_FILE_LALMER).parse()

        # set up graph generator settings
        ggs = GraphGeneratorSettings(edge_features=edge_features)

        # set up graph generator (default values)
        gg = GraphGenerator(ggs)

        # get result
        result = gg._get_featurised_edge(bond_indices, qm_data)

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
        qm_data = DataParser(file_path).parse()

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
        qm_data = DataParser(file_path).parse()

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default())

        # get result
        result = gg._get_hydride_bond_indices(qm_data)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [
            [[1, 2, 3], [1, 2, 3], [1, 2]],
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
                [[1, 2, 3], [1]],
                [[2, 3], [1]],
                [[3, 4], [1]]
            ],
            5,
            AssertionError
        ],

        [
            [
                [[1, 2], [1]],
                [[2, 3], [1, 3]],
                [[3, 4], [1]]
            ],
            5,
            AssertionError
        ],

        [
            [
                [[1, 1], [1]],
                [[2, 3], [1]],
                [[3, 4], [1]]
            ],
            5,
            AssertionError
        ],

        [
            [
                [[1, 2], [1]],
                [[2, 3], [1]],
                [[3, 4], [1]]
            ],
            4,
            AssertionError
        ],

        [
            [
                [[1, 2], [1]],
                [[2, 3], [1]],
                [[4, 3], [1]]
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
        qm_data = DataParser(file_path).parse()

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings.default())

        # get result
        result = gg._determine_hydrogen_position_offset(atom_index, qm_data)

        self.assertEqual(result, expected)

    @parameterized.expand([

        [
            TEST_FILE_LALMER
        ],

    ])
    def test_get_index_matrix(self, file_path):

        # load data
        qm_data = DataParser(file_path).parse()

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings(bond_determination_mode=BondDeterminationMode.WIBERG))

        # get result
        result = gg._get_index_matrix(qm_data)

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
        qm_data = DataParser(file_path).parse()

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings(hydrogen_mode=hydrogen_mode))

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
        qm_data = DataParser(file_path).parse()

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings(hydrogen_mode=hydrogen_mode))

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
        qm_data = DataParser(file_path).parse()

        # set up graph generator (default values)
        gg = GraphGenerator(GraphGeneratorSettings(hydrogen_mode=hydrogen_mode))

        # get result
        result = gg._get_node_positions(qm_data)

        print(result)

        self.assertEqual(result, expected)
