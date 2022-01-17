import unittest
from parameterized import parameterized

from tests.utils import Utils
from nbo2graph.data_parser import DataParser
from nbo2graph.enums.nbo_type import NboType

# constants pointing to test files
TEST_FILE_LALMER = './tests/files/LALMER.out'
TEST_FILE_OREDIA = './tests/files/OREDIA.out'


class TestQmData(unittest.TestCase):
    pass

    @parameterized.expand([

        [
            TEST_FILE_LALMER,
        ],

        [
            TEST_FILE_OREDIA,
        ]

    ])
    def test_get_nbo_data_by_type(self, file_path):

        qm_data = DataParser(file_path).parse_to_qm_data_object()

        Utils.assert_are_almost_equal(qm_data.get_nbo_data_by_type(NboType.LONE_PAIR), qm_data.lone_pair_data)
        Utils.assert_are_almost_equal(qm_data.get_nbo_data_by_type(NboType.LONE_VACANCY), qm_data.lone_vacancy_data)
        Utils.assert_are_almost_equal(qm_data.get_nbo_data_by_type(NboType.BOND), qm_data.bond_pair_data)
        Utils.assert_are_almost_equal(qm_data.get_nbo_data_by_type(NboType.ANTIBOND), qm_data.antibond_pair_data)
        Utils.assert_are_almost_equal(qm_data.get_nbo_data_by_type(NboType.THREE_CENTER_BOND), qm_data.bond_3c_data)
        Utils.assert_are_almost_equal(qm_data.get_nbo_data_by_type(NboType.THREE_CENTER_ANTIBOND), qm_data.antibond_3c_data)
        Utils.assert_are_almost_equal(qm_data.get_nbo_data_by_type(NboType.THREE_CENTER_NONBOND), qm_data.nonbond_3c_data)
