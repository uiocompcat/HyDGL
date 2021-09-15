from DataParser import DataParser
from GraphGenerator import GraphGenerator

dp = DataParser('/home/hkneiding/Desktop/full_Gaussian_file_AGOKEN.log')
qmData = dp.parse()

gg = GraphGenerator(qmData)
gg.generateGraph()