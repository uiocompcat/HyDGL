import unittest
from parameterized import parameterized

from nbo2graph.data_parser import DataParser
from nbo2graph.node_feature import NodeFeature
from nbo2graph.graph_generator import GraphGenerator

class TestGraphGenerator(unittest.TestCase):

    @parameterized.expand([

        # assumes explicit hydrogens
        [
         [NodeFeature.ATOMIC_NUMBERS],
         [
          [48], [8], [7], [6], [16], [6], [6], [6], [7], [6], [6], [6], [6], [6], [7], [6], 
          [6], [6], [6], [6], [7], [6], [16], [6], [6], [6], [17], [8], [8], [8], [8], [1], 
          [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1]
         ]
        ],

        # assumes explicit hydrogens
        # assumes Wiberg bond orders
        [
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

        # assumes explicit hydrogens
        [
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
    ])
    def test_get_nodes(self, node_features, expected):
        
        # load data
        qm_data = DataParser('./tests/test_file.log').parse()

        # set up graph generator with variable node feature list
        gg = GraphGenerator(node_features=node_features)

        # get nodes
        result = gg._get_nodes(qm_data)
        
        # assert
        # self.assertEqual(result, expected)
        # TODO very dirty work around for almost equaling lists ...
        for i in range(len(result)):
            for j in range(len(result[i])):
                self.assertAlmostEqual(result[i][j], expected[i][j], places=3)

