import unittest

from nbo2graph import Graph

class TestGraph(unittest.TestCase):

    # build test graphs
    nodes = [[0], [0], [0], [0], [0]]
    edges = [[[0,1], [0]], [[0,2], [0]], [[0,3], [0]], [[3,2], [0]], [[2,4], [0]]]
    graph1 = Graph(nodes, edges)

    nodes = [[0], [0], [0], [0], [0]]
    edges = [[[0,1], [0]], [[0,2], [0]], [[0,3], [0]], [[3,2], [0]]]
    graph2 = Graph(nodes, edges)

    def isConnected(self):

        self.assertEqual(self.graph1.isConnected(), True)
        self.assertEqual(self.graph2.isConnected(), False)

    def getDisjointSubGraphs(self):

        self.assertEqual(self.graph1.getDisjointSubGraphs, [[0,1,2,3,4]])
        self.assertEqual(self.graph2.getDisjointSubGraphs, [[0,1,2,3], [4]])

    def getAdjacentNodes(self):

        self.assertEqual(self.graph1.getAdjacentNodes(0), [1,2,3])
        self.assertEqual(self.graph1.getAdjacentNodes(4), [2])
        self.assertEqual(self.graph1.getAdjacentNodes(4), [])

        self.assertRaises(ValueError, self.graph1.getAdjacentNodes(5))
        self.assertRaises(ValueError, self.graph1.getAdjacentNodes(-1))