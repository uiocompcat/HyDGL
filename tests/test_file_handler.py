import unittest
from parameterized import parameterized

from nbo2graph.file_handler import FileHandler


class TestFileHandler(unittest.TestCase):

    @parameterized.expand([

        [
            './tests/files/not-existing-file',
            FileNotFoundError
        ],

        [
            './tests/files/',
            IsADirectoryError
        ],

    ])
    def test_read_file_with_invalid_input(self, file_path, expected_error):

        self.assertRaises(expected_error, FileHandler.read_file, file_path)
