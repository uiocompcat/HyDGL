import unittest
from parameterized import parameterized

from nbo2graph.element_look_up_table import ElementLookUpTable


class TestElementLookUpTable(unittest.TestCase):

    @parameterized.expand([

        [
            15,
            'P'
        ],

        [
            99,
            'Es'
        ],

    ])
    def test_get_element_identifier(self, atomic_number, expected):

        self.assertEqual(ElementLookUpTable.get_element_identifier(atomic_number), expected)

    @parameterized.expand([

        [
            'P',
            15

        ],

        [
            'eS',
            99

        ],

        [
            'ba',
            56

        ],

    ])
    def test_get_atomic_number(self, element_identifier, expected):

        self.assertEqual(ElementLookUpTable.get_atomic_number(element_identifier), expected)

    @parameterized.expand([

        [
            0,
            ValueError
        ],

        [
            -5,
            ValueError
        ],

        [
            119,
            ValueError
        ],

    ])
    def test_get_element_identifier_with_invalid_input(self, atomic_number, expected_error):

        self.assertRaises(expected_error, ElementLookUpTable.get_element_identifier, atomic_number)

    @parameterized.expand([

        [
            '',
            ValueError
        ],

        [
            'by',
            ValueError
        ],

    ])
    def test_get_atomic_number_with_invalid_input(self, atomic_number, expected_error):

        self.assertRaises(expected_error, ElementLookUpTable.get_atomic_number, atomic_number)
