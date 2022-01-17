import unittest

# constants pointing to test files
TEST_FILE_LALMER = './tests/files/LALMER.out'
TEST_FILE_OREDIA = './tests/files/OREDIA.out'


class Utils():

    """Class for testing functions."""

    tc = unittest.TestCase()

    @staticmethod
    def assert_are_almost_equal(a, b, places=5):

        """Deep asserts almost equality between two items (can be multidim lists or objects)."""

        Utils.tc.assertEqual(type(a), type(b))

        # check if not list
        if a is None or type(a) in [str, int, float, bool]:
            Utils.tc.assertAlmostEqual(a, b, places=places)
            # return a == b
        elif type(a) == list or type(a) == tuple:

            # check length
            Utils.tc.assertEqual(len(a), len(b))

            # recursively call
            for a_, b_ in zip(a, b):
                Utils.assert_are_almost_equal(a_, b_, places=places)
        else:
            Utils.object_are_almost_equal(a, b, places=places)

    @staticmethod
    def object_are_almost_equal(a, b, places=5):

        """Equality operator for class-type variables."""

        dict_a = vars(a)
        dict_b = vars(b)

        Utils.tc.assertEqual(list(dict_a.keys()), list(dict_b.keys()))

        for key in dict_a.keys():

            Utils.assert_are_almost_equal(dict_a[key], dict_b[key], places)
