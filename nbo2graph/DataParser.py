import re
from operator import add

from FileHandler import FileHandler
from QmData import QmData



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

            if 'Bond orbital / Coefficients / Hybrids' in self.lines[i]:
                qmData.lonePairData, qmData.loneVacancyData, qmData.bondPairData = self.extractNboData(i + 2)
        
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

        # setup nAtoms x nAtoms matrix for Wiberg indices
        wibergIndexMatrix = [[0 for x in range(self.nAtoms)] for y in range(self.nAtoms)] 

        # counter for keeping track how many columns have been taken care of
        # this is necessary because the Gaussian output file prints the Wiberg
        # index matrix in blocks of columns
        nColumnsProcessed = 0

        # run until all columns have been processed
        while nColumnsProcessed < self.nAtoms:

            nColumns = None
            for i in range(startIndex, startIndex + self.nAtoms, 1):
                # split line at any white space
                lineSplit = ' '.join(self.lines[i].split()).split(' ')
                # drop first two columns so that only Wiberg indices remain
                lineSplit = lineSplit[2:]
            
                # check that the number of columns is the same
                if nColumns == None:
                    nColumns = len(lineSplit)
                else:
                    assert nColumns == len(lineSplit)

                # read out data (index number based on Gaussian output format)
                for j in range(len(lineSplit)):
                    # write matrix element
                    wibergIndexMatrix[i-startIndex][j + nColumnsProcessed] = float(lineSplit[j])

            nColumnsProcessed += nColumns

            # set startIndex to the next block
            startIndex += self.nAtoms + 3

        return wibergIndexMatrix

    def extractNboData(self, startIndex):
        
        # output variable for lone pairs
        lonePairAtomPositions = []
        lonePairCounts = []
        lonePairOccupations = []
        # final output variable
        lonePairData = [] #[[0, [0,0,0,0]] for x in range(self.nAtoms)]

        # variables for bond pairs
        bondPairAtomPositions = []
        bondPairOccupations = []
        # final output variable
        bondPairData = []

        # variables for lone vacancy
        loneVacancyAtomPositions = []
        loneVacancyCounts = []
        loneVacancyOccupations = []
        # final output variable
        loneVacancyData = []

        i = startIndex

        while not self.lines[i] == '':

            # split line at any white space
            lineSplit = ' '.join(self.lines[i].split()).split(' ')
            
            if len(lineSplit) > 3:

                # lone pairs
                if lineSplit[2] == 'LP':
                    atomPosition, occupations = self.extractLonePairData(i)

                    # check if lone pair atom already exists
                    # if so add together
                    # otherwise make new entry (with count 1)
                    if atomPosition in lonePairAtomPositions:
                        lonePairIndex = lonePairAtomPositions.index(atomPosition)
                        lonePairCounts[lonePairIndex] += 1
                        lonePairOccupations[lonePairIndex] = list(map(add, lonePairOccupations[lonePairIndex], occupations))
                    else:
                        lonePairAtomPositions.append(atomPosition)
                        lonePairCounts.append(1)
                        lonePairOccupations.append(occupations)

                # bonds
                if lineSplit[2] == 'BD':
                    atomPositions, occupations = self.extractBondingData(i)
                    
                    # sort to ensure correct compare behaviour
                    atomPositions.sort()

                    # check if bond pair already exists
                    # if so, add together
                    # otherwise make new entry
                    if atomPositions in bondPairAtomPositions:
                        bondPairIndex = bondPairAtomPositions.index(atomPositions)
                        bondPairOccupations[bondPairIndex] = list(map(add, bondPairOccupations[bondPairIndex], occupations))
                    else:
                        bondPairAtomPositions.append(atomPositions)
                        bondPairOccupations.append(occupations)

                # lone vacancy
                # TODO
                if lineSplit[2] == 'LV':
                    atomPosition, occupations = self.extractLonePairData(i)

                    # check if lone vacancy atom already exists
                    # if so add together
                    # otherwise make new entry (with count 1)
                    if atomPosition in loneVacancyAtomPositions:
                        loneVacancyIndex = loneVacancyAtomPositions.index(atomPosition)
                        loneVacancyCounts[loneVacancyIndex] += 1
                        loneVacancyOccupations[loneVacancyIndex] = list(map(add, loneVacancyOccupations[loneVacancyIndex], occupations))
                    else:
                        loneVacancyAtomPositions.append(atomPosition)
                        loneVacancyCounts.append(1)
                        loneVacancyOccupations.append(occupations)


            i += 1

        # normalise lone pair occupations to sum to 1
        for i in range(len(lonePairOccupations)):
            # only normalise when there is a significant difference that is not due to rounding errors
            if sum(lonePairOccupations[i]) > 1.1:
                lonePairOccupations[i] = [float(x)/sum(lonePairOccupations[i]) for x in lonePairOccupations[i]]

        # build lone pair data
        # check that atom position list, lone pair count list and occupation list have the same length
        if not len(lonePairAtomPositions) == len(lonePairCounts) or \
           not len(lonePairAtomPositions) == len(lonePairOccupations):
            raise Exception('Length of extracted data arrays is not equal.')
        else:
            for i in range(len(lonePairAtomPositions)):
                lonePairData.append([lonePairAtomPositions[i], lonePairCounts[i], lonePairOccupations[i]])

        # normalise bond pair occupations to sum to 1
        for i in range(len(bondPairOccupations)):
            # only normalise when there is a significant difference that is not due to rounding errors
            if sum(bondPairOccupations[i]) > 1.1:
                bondPairOccupations[i] = [float(x)/sum(bondPairOccupations[i]) for x in bondPairOccupations[i]]

        # build bond pair data
        # check that atom position list and occupation list have the same length
        if not len(bondPairAtomPositions) == len(bondPairOccupations):
            raise Exception('Length of extracted data arrays is not equal.')
        else:
            for i in range(len(bondPairAtomPositions)):
                bondPairData.append([bondPairAtomPositions[i], bondPairOccupations[i]])

        # normalise lone vacancy occupations to sum to 1
        for i in range(len(loneVacancyOccupations)):
            # only normalise when there is a significant difference that is not due to rounding errors
            if sum(loneVacancyOccupations[i]) > 1.1:
                loneVacancyOccupations[i] = [float(x)/sum(loneVacancyOccupations[i]) for x in loneVacancyOccupations[i]]

        # build lone vacancy data
        # check that atom position list, lone vacancy count list and occupation list have the same length
        if not len(loneVacancyAtomPositions) == len(loneVacancyCounts) or \
           not len(loneVacancyAtomPositions) == len(loneVacancyOccupations):
            raise Exception('Length of extracted data arrays is not equal.')
        else:
            for i in range(len(loneVacancyAtomPositions)):
                lonePairData.append([loneVacancyAtomPositions[i], loneVacancyCounts[i], loneVacancyOccupations[i]])

        return lonePairData, loneVacancyData, bondPairData

    def extractLonePairData(self, startIndex):

        # obtain atom position
        lineSplit = list(filter(None, re.split(r'\(|\)| ', self.lines[startIndex])))[5:]
        atomPosition = int(lineSplit[0]) - 1

        # get occupation from both lines using regex (values in brackets)
        mergedLines = (self.lines[startIndex] + self.lines[startIndex + 1]).replace(' ', '')
        result = re.findall('\((.{3,5})%\)', mergedLines)
        occupations = list(map(float, result))

        # return atom position for assignment in list
        # divide occupations by 100 (get rid of %)
        return atomPosition, [x / 100 for x in occupations]

    def extractBondingData(self, startIndex):

        # obtain atom positions
        lineSplit = list(filter(None, re.split(r'\(|\)|-| ', self.lines[startIndex])))[4:]
        atomPositions = [int(lineSplit[-3]) - 1, int(lineSplit[-1]) - 1]

        # get occupation from both lines using regex (values in brackets)
        mergedLines = (self.lines[startIndex + 1] + self.lines[startIndex + 2]).replace(' ', '')
        result = re.findall('\((.{3,5})%\)', mergedLines)
        occupations1 = list(map(float, result))[1:]
        # append zeros to account for atoms that do not have higher orbital types
        while len(occupations1) < 4:
            occupations1.append(0)

        # find line with second data
        i = startIndex + 3
        while not '(' in self.lines[i]:
            i += 1

        # get occupation from both lines using regex (values in brackets)
        mergedLines = (self.lines[i] + self.lines[i + 1]).replace(' ', '')
        result = re.findall('\((.{3,5})%\)', mergedLines)
        occupations2 = list(map(float, result))[1:]
        # append zeros to account for atoms that do not have higher orbital types
        while len(occupations2) < 4:
            occupations2.append(0)

        # add contributions from both parts
        occupations = list(map(add, occupations1, occupations2))

        # return atom position for assignment in list
        # divide occupations by 200 (average and get rid of %)
        return atomPositions, [x / 200 for x in occupations]


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