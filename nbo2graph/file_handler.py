import os
import pickle


class FileHandler:

    """Class for handling all IO/file handling tasks."""

    @staticmethod
    def read_file(file_path):
        """Reads a specified file.

        Args:
            file_path (string): The path to the input file.

        Raises:
            FileNotFoundError: If file not found.
            IsADirectoryError: If path points to a directory.

        Returns:
            string: The file content.
        """

        try:
            f = open(file_path, 'r')
        except FileNotFoundError:
            raise FileNotFoundError('The specified file does not exist.')
        except IsADirectoryError:
            raise IsADirectoryError('Cannot open directory.')

        with f:
            data = f.read()
            f.close()

            return data

    @staticmethod
    def write_file(file_path: str, data):
        """Writes the specified content into a file (overwrites).

        Args:
            file_path (string): The path to the output file.
            data (): The file content to write.
        """

        f = open(file_path, 'w')
        f.write(data)
        f.close()

    @staticmethod
    def read_binary_file(file_path):
        """Reads a specified binary file.

        Args:
            file_path (string): The path to the input file.

        Raises:
            FileNotFoundError: If file not found.
            IsADirectoryError: If path points to a directory.

        Returns:
            binary: The file content.
        """

        try:
            f = open(file_path, 'rb')
        except FileNotFoundError:
            raise FileNotFoundError('The specified file does not exist.')
        except IsADirectoryError:
            raise IsADirectoryError('Cannot open directory.')

        with f:
            data = pickle.load(f)
            f.close()

            return data

    @staticmethod
    def write_binary_file(file_path: str, data):
        """Writes the specified binary content into a file (overwrites).

        Args:
            file_path (string): The path to the output file.
            data (): The file content to write.
        """

        f = open(file_path, 'wb')
        pickle.dump(data, f)
        f.close()

    @staticmethod
    def clear_directory(directory: str, file_names: list[str]):

        """Clears a directory of specified files.

        Args:
            directory (string): The directory.
            file_names (list[string]): A list of file names to delete.
        """

        for file_name in file_names:
            if os.path.isfile(os.path.join(directory, file_name)):
                os.remove(os.path.join(directory, file_name))
