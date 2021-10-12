import unittest


class Utils():

    """Class for testing functions."""

    tc = unittest.TestCase()

    @staticmethod
    def assert_are_almost_equal(a, b, places=5):

        """Deep asserts almost equality between two objects."""

        # check if not list
        if type(a) != list:
            Utils.tc.assertAlmostEqual(a, b, places=places)
            # return a == b
        else:

            # check length
            Utils.tc.assertEqual(len(a), len(b))

            # recursively call
            for a_, b_ in zip(a, b):
                Utils.assert_are_almost_equal(a_, b_, places=places)
