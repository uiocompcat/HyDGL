import unittest
from parameterized import parameterized

from nbo2graph.bond_determination_mode import BondDeterminationMode
from nbo2graph.hydrogen_mode import HydrogenMode

from nbo2graph.data_parser import DataParser
from nbo2graph.node_feature import NodeFeature
from nbo2graph.graph_generator import GraphGenerator

class TestGraphGenerator(unittest.TestCase):

    @parameterized.expand([

        [
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
         HydrogenMode.OMIT,
         BondDeterminationMode.WIBERG,
         [NodeFeature.ATOMIC_NUMBERS],
         [
          [48], [8], [7], [6], [16], [6], [6], [6], [7], [6], [6], [6], [6], [6], [7], [6], 
          [6], [6], [6], [6], [7], [6], [16], [6], [6], [6], [17], [8], [8], [8], [8]
         ]
        ],

        [
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
         HydrogenMode.EXPLICIT,
         BondDeterminationMode.WIBERG,
         [NodeFeature.BOND_ORDER_TOTAL],
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
         HydrogenMode.EXPLICIT,
         BondDeterminationMode.NLMO,
         [NodeFeature.BOND_ORDER_TOTAL],
         [
          [0.5744], [1.022], [2.2828], [3.3946], [1.9874], [3.3227], [3.5845], [3.1819], 
          [2.2794], [3.5223], [3.5658], [3.7724], [3.5903], [3.7262], [2.2683], [3.5313], 
          [3.5804], [3.7722], [3.5926], [3.7325], [2.27], [3.3969], [1.993], [3.3239], 
          [3.5949], [3.1929], [4.1104], [0.7012], [0.7221], [0.7784], [0.8416], [0.4988], 
          [0.7029], [0.4975], [0.755], [0.7378], [0.744], [0.7555], [0.7705], [0.7003], 
          [0.7588], [0.7436], [0.7536], [0.7619], [0.735], [0.7559], [0.7702]
         ]
        ],

        [
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
         HydrogenMode.EXPLICIT,
         BondDeterminationMode.WIBERG,
         [NodeFeature.NATURAL_ELECTRON_CONFIGURATION_S, NodeFeature.NATURAL_ELECTRON_CONFIGURATION_P, NodeFeature.NATURAL_ELECTRON_CONFIGURATION_D, NodeFeature.NATURAL_ELECTRON_CONFIGURATION_F],
         [
          [0.31,0.01,9.98,0], [1.75,5.21,0.01,0], [1.37,4.13,0.01,0], [0.97,3.01,0.01,0], 
          [1.65,3.82,0.03,0], [1.10,3.32,0.01,0], [0.91,2.92,0,0], [1.13,3.53,0.01,0], 
          [1.34,4.14,0.01,0], [0.89,2.94,0,0], [1.00,3.2,0,0], [1.00,3.13,0,0], 
          [1.00,3.2,0,0], [0.89,2.91,0,0], [1.34,4.13,0.01,0], [0.89,2.94,0,0], 
          [1.00,3.2,0,0], [1.00,3.13,0,0], [1.00,3.2,0,0], [0.89,2.92,0,0], 
          [1.37,4.14,0.02,0], [0.96,3.01,0.01,0], [1.65,3.82,0.03,0], [1.10,3.31,0.01,0],
          [0.91,2.91,0,0], [1.13,3.53,0.01,0], [1.25,3.08,0.3,0.01], [1.89,5.01,0.02,0], 
          [1.89,4.96,0.02,0], [1.87,4.85,0.02,0], [1.87,4.82,0.02,0], [0.5,0,0,0], 
          [0.72,0,0,0], [0.5,0,0,0], [0.75,0,0,0], [0.73,0,0,0], [0.75,0,0,0], [0.76,0,0,0], 
          [0.76,0,0,0], [0.72,0,0,0], [0.76,0,0,0], [0.75,0,0,0], [0.75,0,0,0], [0.77,0,0,0], 
          [0.73,0,0,0], [0.76,0,0,0], [0.76,0,0,0]
         ]
        ],

        [
         HydrogenMode.OMIT,
         BondDeterminationMode.WIBERG,
         [NodeFeature.LONE_PAIRS_S, NodeFeature.LONE_PAIRS_P, NodeFeature.LONE_PAIRS_D, NodeFeature.LONE_PAIRS_F],
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
         HydrogenMode.OMIT,
         BondDeterminationMode.WIBERG,
         [NodeFeature.LONE_VACANCIES_S, NodeFeature.LONE_VACANCIES_P, NodeFeature.LONE_VACANCIES_D, NodeFeature.LONE_VACANCIES_F,],
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
    ])
    def test_get_nodes(self, hydrogen_mode, bond_determination_mode, node_features, expected):
        
        # load data
        qm_data = DataParser('./tests/test_file.out').parse()

        # set up graph generator with variable node feature list
        gg = GraphGenerator(node_features=node_features, hydrogen_mode=hydrogen_mode, bond_determination_mode=bond_determination_mode)

        # get nodes
        result = gg._get_nodes(qm_data)
        
        # assert length
        self.assertEqual(len(result), len(expected))
        
        # TODO very dirty work around for almost equaling lists ...
        for i in range(len(result)):
            # assert length of sublists
            self.assertEqual(len(result[i]), len(expected[i]))
            for j in range(len(result[i])):
                # assert equality
                self.assertAlmostEqual(result[i][j], expected[i][j], places=3)

    @parameterized.expand([

        [
         0, 0.1, []
        ],

        [
         11, 0.1, [10, 12, 41]
        ],

    ])

    def test_get_bound_atom_indices(self, atom_index, threshold, expected):

        # load data
        qm_data = DataParser('./tests/test_file.out').parse()

        # set up graph generator (default values)
        gg = GraphGenerator()

        # get result
        result = gg._get_bound_atom_indices(atom_index, qm_data, threshold)

        self.assertEqual(result, expected)


    @parameterized.expand([

        [
         -1, 0.1
        ],

        [
         47, 0.1
        ],

    ])
    def test_get_bound_atom_indices_with_invalid_input(self, atom_index, threshold):

        # load data
        qm_data = DataParser('./tests/test_file.out').parse()

        # set up graph generator (default values)
        gg = GraphGenerator()

        # get result
        self.assertRaises(ValueError, gg._get_bound_atom_indices, atom_index, qm_data, threshold)


    @parameterized.expand([

        [
         2, 0.1, []
        ],

        [
         7, 0.1, [32, 45, 46]
        ],

    ])

    def test_get_bound_h_indices(self, atom_index, threshold, expected):

        # load data
        qm_data = DataParser('./tests/test_file.out').parse()

        # set up graph generator (default values)
        gg = GraphGenerator()

        # get result
        result = gg._get_bound_h_atom_indices(atom_index, qm_data, threshold)

        self.assertEqual(result, expected)


    @parameterized.expand([

        [
         -1, 0.1
        ],

        [
         47, 0.1
        ],

    ])
    def test_get_bound_h_indices_with_invalid_input(self, atom_index, threshold):

        # load data
        qm_data = DataParser('./tests/test_file.out').parse()

        # set up graph generator (default values)
        gg = GraphGenerator()

        # get result
        self.assertRaises(ValueError, gg._get_bound_h_atom_indices, atom_index, qm_data, threshold)


    @parameterized.expand([

        [
         15, 0
        ],

        [
         18, 1
        ],

    ])

    def test_determine_hydrogen_count(self, atom_index, expected):

        # load data
        qm_data = DataParser('./tests/test_file.out').parse()

        # set up graph generator (default values)
        gg = GraphGenerator()

        # get result
        result = gg._determine_hydrogen_count(atom_index, qm_data)

        self.assertEqual(result, expected)