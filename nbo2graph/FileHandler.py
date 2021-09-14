class FileHandler:

    """Static class for handling all IO/file handling tasks."""

    @staticmethod
    def readFile(filePath):
        """Reads a specified file.

        Args:
            filePath (string): The path to the input file.

        Raises:
            FileNotFoundError: If file not found.
            IsADirectoryError: If path points to a directory.

        Returns:
            string: The file content.
        """
        try:
            f = open(filePath, 'r')
        except FileNotFoundError:
            raise FileNotFoundError('The specified file does not exist.')
        except IsADirectoryError:
            raise IsADirectoryError('Cannot open directory.')
        
        with f:
            data = f.read()
            f.close()

            return data

    @staticmethod
    def writeFile(filePath, data):
        """Writes the specified content into a file (overwrites).

        Args:
            filePath (string): The path to the output file.
            data (string): The file content to write.
        """
        f = open(filePath, 'w')
        f.write(data)
        f.close()