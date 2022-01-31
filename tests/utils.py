import unittest

# constants pointing to test files
TEST_FILE_LALMER = './tests/files/LALMER.json'
TEST_FILE_OREDIA = './tests/files/OREDIA.json'
TEST_FILE_ZUYHEG = './tests/files/ZUYHEG.json'
TEST_FILE_QM_DATA_OREDIA = './tests/files/OREDIA.qmdata'
TEST_FILE_JSON = './tests/files/test-file.json'


class Utils():

    """Class for testing functions."""

    tc = unittest.TestCase()

    @staticmethod
    def assert_are_almost_equal(a, b, places=5):

        """Deep asserts almost equality between two items (can be multidim lists, dicts or objects)."""

        Utils.tc.assertEqual(type(a), type(b))

        # check if not list
        if a is None or type(a) in [str, int, float, bool]:
            Utils.tc.assertAlmostEqual(a, b, places=places)
        elif type(a) == dict:
            Utils.dict_are_almost_equal(a, b, places=places)
        elif type(a) == list or type(a) == tuple:

            # check length
            Utils.tc.assertEqual(len(a), len(b))

            # recursively call
            for a_, b_ in zip(a, b):
                Utils.assert_are_almost_equal(a_, b_, places=places)
        else:
            Utils.object_are_almost_equal(a, b, places=places)

    @staticmethod
    def dict_are_almost_equal(a, b, places=5):

        """Equality operator for dicts."""

        keys_a = sorted(a.keys())
        keys_b = sorted(b.keys())

        Utils.tc.assertEqual(keys_a, keys_b)

        for key in keys_a:
            Utils.assert_are_almost_equal(a[key], b[key], places=places)

    @staticmethod
    def object_are_almost_equal(a, b, places=5):

        """Equality operator for class-type variables."""

        dict_a = vars(a)
        dict_b = vars(b)

        Utils.tc.assertEqual(list(dict_a.keys()), list(dict_b.keys()))

        for key in dict_a.keys():

            Utils.assert_are_almost_equal(dict_a[key], dict_b[key], places)
