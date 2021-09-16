from ElementLookUpTable import ElementLookUpTable

class FileHandler:

    """Class for handling all IO/file handling tasks."""

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

    @staticmethod
    def writeMolFile(filePath, graph):

        # data to write
        data = '\nMolecule\n\n'

        data += str(len(graph['nodes'])).rjust(3, ' ') + str(len(graph['edges'])).rjust(3, ' ') + '  0  0  0  0  0  0  0  0999 V2000\n'

        for i in range(len(graph['nodes'])):
            data += '    0.0000    0.0000    0.0000 ' + ElementLookUpTable.getElementIdentifier(graph['nodes'][i][0]).ljust(5, ' ') + '0  0  0  0  0  0  0  0  0  0  0  0\n'

        for i in range(len(graph['edges'])):
            
            data += str(graph['edges'][i][0][0] + 1).rjust(3, ' ') + str(graph['edges'][i][0][1] + 1).rjust(3, ' ') + '  1  0  0  0  0 \n'

        data += 'M  END'
        FileHandler.writeFile(filePath, data)