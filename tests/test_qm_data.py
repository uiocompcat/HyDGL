import unittest
from parameterized import parameterized

from HyDGL.qm_data import QmData
from HyDGL.enums.nbo_type import NboType
from HyDGL.file_handler import FileHandler
from tests.utils import Utils, TEST_FILE_QM_DATA_OREDIA


class TestQmData(unittest.TestCase):

    @parameterized.expand([

        [
            TEST_FILE_QM_DATA_OREDIA,
        ],

    ])
    def test_get_nbo_data_by_type(self, file_path):

        qm_data: QmData = FileHandler.read_binary_file(file_path)

        Utils.assert_are_almost_equal(qm_data.get_nbo_data_by_type(NboType.LONE_PAIR), qm_data.lone_pair_data)
        Utils.assert_are_almost_equal(qm_data.get_nbo_data_by_type(NboType.LONE_VACANCY), qm_data.lone_vacancy_data)
        Utils.assert_are_almost_equal(qm_data.get_nbo_data_by_type(NboType.BOND), qm_data.bond_pair_data)
        Utils.assert_are_almost_equal(qm_data.get_nbo_data_by_type(NboType.ANTIBOND), qm_data.antibond_pair_data)
        Utils.assert_are_almost_equal(qm_data.get_nbo_data_by_type(NboType.THREE_CENTER_BOND), qm_data.bond_3c_data)
        Utils.assert_are_almost_equal(qm_data.get_nbo_data_by_type(NboType.THREE_CENTER_ANTIBOND), qm_data.antibond_3c_data)
        Utils.assert_are_almost_equal(qm_data.get_nbo_data_by_type(NboType.THREE_CENTER_NONBOND), qm_data.nonbond_3c_data)
