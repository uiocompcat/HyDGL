from FileHandler import FileHandler
from QmData import QmData

import re

class DataParser:
    
    """Class for reading relevant data from QM output files."""

    def __init__(self, filePath):
        """Constructor

        Args:
            filePath (string): Path to the QM Output file.
        """
        self.data = FileHandler.readFile(filePath)
        self.lines = self.data.split('\n')
        self.nAtoms = self.getNumberOfAtoms()

    def parse(self):

        qmData = QmData()
        qmData.nAtoms = self.nAtoms
        for i in range(len(self.lines)):

            # search for keywords and if found call appropriate functions with start index
            # the start index addition offset is based on the Gaussian output format
            if 'Standard orientation' in self.lines[i]:
                qmData.atomicNumbers = self.extractAtomicNumbers(i + 5)
                qmData.geometricData = self.extractGeometricData(i + 5)

            if 'Summary of Natural Population Analysis' in self.lines[i]:
                qmData.naturalAtomicCharges = self.extractNaturalAtomicCharges(i + 6)

            if 'Natural Electron Configuration' in self.lines[i]:
                qmData.naturalElectronConfiguration = self.extractNaturalElectronConfiguration(i + 2)

            if 'Wiberg bond index matrix' in self.lines[i]:
                qmData.wibergIndexMatrix = self.extractWibergIndexMatrix(i + 4)
        
        return qmData

    def extractAtomicNumbers(self, startIndex):

        atomicNumbers = []

        for i in range(startIndex, startIndex + self.nAtoms, 1):
            # split line at any white space
            lineSplit = ' '.join(self.lines[i].split()).split(' ')
            # read out data (index number based on Gaussian output format)
            atomicNumbers.append(int(lineSplit[1]))
        
        return atomicNumbers

    def extractGeometricData(self, startIndex):

        geometricData = []

        for i in range(startIndex, startIndex + self.nAtoms, 1):
            # split line at any white space
            lineSplit = ' '.join(self.lines[i].split()).split(' ')
            # read out data (index number based on Gaussian output format)
            xyz = [float(lineSplit[3]), float(lineSplit[4]), float(lineSplit[5])]
            geometricData.append(xyz)

        return geometricData

    def extractNaturalAtomicCharges(self, startIndex):
        
        naturalAtomicCharges = []

        for i in range(startIndex, startIndex + self.nAtoms, 1):
            # split line at any white space
            lineSplit = ' '.join(self.lines[i].split()).split(' ')
            # read out data (index number based on Gaussian output format)
            naturalAtomicCharges.append(float(lineSplit[2]))
        
        return naturalAtomicCharges

    def extractNaturalElectronConfiguration(self, startIndex):
        
        naturalElectronConfiguration = []

        for i in range(startIndex, startIndex + self.nAtoms, 1):
            
            # single atom electron configuration ([s, p, d, f])
            electronConfiguration = [0, 0, 0, 0]

            # split line at any white space
            lineSplit = ' '.join(self.lines[i].split()).split(' ')
            # remove first two columns of data, rejoin and remove '[core]'
            lineCleaned = ''.join(lineSplit[2:]).replace('[core]', '')
            # split at '(' and ')' so that orbital type and config can be extracted
            lineCleanedSplit = re.split(r'\(|\)', lineCleaned)

            for j in range(0, len(lineCleanedSplit), 2):

                # add value to appropriate list element
                if 's' in lineCleanedSplit[j]:
                    electronConfiguration[0] += float(lineCleanedSplit[j + 1])
                elif 'p' in lineCleanedSplit[j]:
                    electronConfiguration[1] += float(lineCleanedSplit[j + 1])
                elif 'd' in lineCleanedSplit[j]:
                    electronConfiguration[2] += float(lineCleanedSplit[j + 1])
                elif 'f' in lineCleanedSplit[j]:
                    electronConfiguration[3] += float(lineCleanedSplit[j + 1])
                else:
                    continue

            # append to full list
            naturalElectronConfiguration.append(electronConfiguration)

        return naturalElectronConfiguration

    def extractWibergIndexMatrix(self, startIndex):

        # setup nAtoms x nAtoms matrix for Wiberg indeces
        wibergIndexMatrix = [[0 for x in range(self.nAtoms)] for y in range(self.nAtoms)] 

        for i in range(startIndex, startIndex + self.nAtoms, 1):
            # split line at any white space
            lineSplit = ' '.join(self.lines[i].split()).split(' ')
            # drop first two columns so that only Wiberg indeces remain
            lineSplit = lineSplit[2:]
            # read out data (index number based on Gaussian output format)
            for j in range(len(lineSplit)):
                if not wibergIndexMatrix[i-startIndex][j] == 0:
                    print('Overwriting already set matrix element.')
                wibergIndexMatrix[i-startIndex][j] = float(lineSplit[j])

        print(wibergIndexMatrix)

    def getNumberOfAtoms(self):

        for i in range(len(self.lines)):
            # find line that contain atom number
            if 'NAtoms=' in self.lines[i]:

                # get position in line
                lineSplit = ' '.join(self.lines[i].split()).split(' ')
                nAtomsIndex = lineSplit.index('NAtoms=') + 1

                # return
                return int(lineSplit[nAtomsIndex])
        
        raise Exception('Could not find number of atoms in file.')