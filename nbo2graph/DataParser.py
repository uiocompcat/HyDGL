import re
from operator import add

from FileHandler import FileHandler
from QmData import QmData

class DataParser:
    
    """Class for reading relevant data from Gaussian output files."""

    def __init__(self, filePath):

        """Constructor

        Args:
            filePath (string): Path to the Gaussian output file.
        """

        self.filePath = filePath
        self.lines = FileHandler.readFile(filePath).split('\n')
        self.nAtoms = self._getNumberOfAtoms()

    def _getNumberOfAtoms(self):

        for i in range(len(self.lines)):
            # find line that contain atom number
            if 'NAtoms=' in self.lines[i]:

                # get position in line
                lineSplit = self.lines[i].split()
                nAtomsIndex = lineSplit.index('NAtoms=') + 1

                # return
                return int(lineSplit[nAtomsIndex])
        
        raise Exception('Could not find number of atoms in file.')

    def parse(self):

        # output variable
        qmData = QmData()
        qmData.nAtoms = self.nAtoms

        # get csd token from file name
        qmData.csdIdentifier = ''.join(self.filePath.split('/')[-1].split('.')[0:-1])

        # variable that shows if scan is currently in SVP or TZVP region of output file
        regionState = ''
        for i in range(len(self.lines)):

            if 'def2SVP' in self.lines[i]:
                regionState = 'svp'
            elif 'def2TZVP' in self.lines[i]:
                regionState = 'tzvp'

            # search for keywords and if found call appropriate functions with start index
            # the start index addition offset is based on the Gaussian output format
            if 'Standard orientation' in self.lines[i]:
                qmData.atomicNumbers = self._extractAtomicNumbers(i + 5)
                qmData.geometricData = self._extractGeometricData(i + 5)

            if 'Summary of Natural Population Analysis' in self.lines[i]:
                qmData.naturalAtomicCharges = self._extractNaturalAtomicCharges(i + 6)

            if 'Natural Electron Configuration' in self.lines[i]:
                qmData.naturalElectronConfiguration = self._extractNaturalElectronConfiguration(i + 2)

            if 'Wiberg bond index matrix' in self.lines[i]:
                qmData.wibergIndexMatrix = self._extractIndexMatrix(i + 4)

            if 'Atom-Atom Net Linear NLMO/NPA' in self.lines[i]:
                qmData.nboBondOrderMatrix = self._extractIndexMatrix(i + 4)

            if 'Bond orbital / Coefficients / Hybrids' in self.lines[i]:
                qmData.lonePairData, qmData.loneVacancyData, qmData.bondPairData, qmData.antibondPairData = self._extractNboData(i + 2)
        
            if 'NATURAL BOND ORBITALS' in self.lines[i]:
                qmData.nboEnergies = self._extractNboEnergies(i + 7)

            if 'Atom I' in self.lines[i]:
                qmData.lmoBondOrderMatrix = self._extractLmoBondData(i + 1)

            if 'Charge = ' in self.lines[i]:
                qmData.charge = self._extractCharge(i)

            if 'Stoichiometry' in self.lines[i]:
                qmData.stoichiometry = self._extractStoichiometry(i)

            if 'Molecular mass' in self.lines[i]:
                qmData.molecularMass = self._extractMolecularMass(i)

            if 'Grimme-D3(BJ) Dispersion energy=' in self.lines[i]:
                if regionState == 'svp':
                    qmData.svpDispersionEnergy = self._extractDispersionEnergy(i)
                elif regionState == 'tzvp':
                    qmData.tzvpDispersionEnergy = self._extractDispersionEnergy(i)

            if 'SCF Done' in self.lines[i]:
                if regionState == 'svp':
                    qmData.svpElectronicEnergy = self._extractElectronicEnergy(i)
                elif regionState == 'tzvp':
                    qmData.tzvpElectronicEnergy = self._extractElectronicEnergy(i)

            if 'Dipole moment (field-independent basis, Debye)' in self.lines[i]:
                if regionState == 'svp':
                    qmData.svpDipoleMoment = self._extractDipoleMoment(i + 1)
                elif regionState == 'tzvp':
                    qmData.tzvpDipoleMoment = self._extractDipoleMoment(i + 1)
            
            if 'Isotropic polarizability' in self.lines[i]:
                qmData.polarisability = self._extractPolarisability(i)

            if 'Frequencies -- ' in self.lines[i]:
                if qmData.frequencies == None:
                    qmData.frequencies = self._extractFrequency(i)
                else:
                    qmData.frequencies.extend(self._extractFrequency(i))

            if 'Zero-point correction=' in self.lines[i]:
                qmData.zpeCorrection = self._extractZpeCorrection(i)

            if 'Sum of electronic and thermal Enthalpies=' in self.lines[i]:
                qmData.enthalpyEnergy = self._extractEnthalpyEnergy(i)

            if 'Sum of electronic and thermal Free Energies=' in self.lines[i]:
                qmData.gibbsEnergy = self._extractGibbsEnergy(i)
                qmData.heatCapacity = self._extractHeatCapacity(i + 4)
                qmData.entropy = self._extractEntropy(i + 4)

            if 'Alpha  occ. eigenvalues' in self.lines[i]:
                if regionState == 'svp':
                    if qmData.svpOccupiedOrbitalEnergies == None:
                        qmData.svpOccupiedOrbitalEnergies = self._extractOrbitalEnergies(i)
                    else:
                        qmData.svpOccupiedOrbitalEnergies.extend(self._extractOrbitalEnergies(i))
                elif regionState == 'tzvp':
                    if qmData.tzvpOccupiedOrbitalEnergies == None:
                        qmData.tzvpOccupiedOrbitalEnergies = self._extractOrbitalEnergies(i)
                    else:    
                        qmData.tzvpOccupiedOrbitalEnergies.extend(self._extractOrbitalEnergies(i))

            if 'Alpha virt. eigenvalues' in self.lines[i]:
                if regionState == 'svp':
                    if qmData.svpVirtualOrbitalEnergies == None:
                        qmData.svpVirtualOrbitalEnergies = self._extractOrbitalEnergies(i)
                    else:
                        qmData.svpVirtualOrbitalEnergies.extend(self._extractOrbitalEnergies(i))
                elif regionState == 'tzvp':
                    if qmData.tzvpVirtualOrbitalEnergies == None:
                        qmData.tzvpVirtualOrbitalEnergies = self._extractOrbitalEnergies(i)
                    else:    
                        qmData.tzvpVirtualOrbitalEnergies.extend(self._extractOrbitalEnergies(i))

        # calculate extra properties such as delta values, HOMO, LUMU, etc.
        qmData.calculateProperties()

        return qmData

    # - - - extraction functions - - - #

    # Some of the following extraction functions are redundant in the sense that for some properties
    # the extraction procedures are identical. The distinction between these functions is kept 
    # nonetheless to ensure maintainability (e.g. when the Gaussian output format changes).

    def _extractCharge(self, startIndex):

        lineSplit = self.lines[startIndex].split()
        return int(lineSplit[2])

    def _extractStoichiometry(self, startIndex):

        lineSplit = self.lines[startIndex].split()
        return lineSplit[1]

    def _extractMolecularMass(self, startIndex):

        lineSplit = self.lines[startIndex].split()
        return float(lineSplit[2])

    def _extractDispersionEnergy(self, startIndex):

        lineSplit = self.lines[startIndex].split()
        return float(lineSplit[4])

    def _extractElectronicEnergy(self, startIndex):

        lineSplit = self.lines[startIndex].split()
        return float(lineSplit[4])

    def _extractDipoleMoment(self, startIndex):

        lineSplit = self.lines[startIndex].split()
        return float(lineSplit[7])

    def _extractPolarisability(self, startIndex):

        lineSplit = self.lines[startIndex].split()
        return float(lineSplit[5])

    def _extractFrequency(self, startIndex):

        lineSplit = self.lines[startIndex].split()
        return list(map(float, lineSplit[2:]))

    def _extractOrbitalEnergies(self, startIndex):

        lineSplit = self.lines[startIndex].split()

        # build output list
        orbitalEnergies = []
        for i in range(len(lineSplit[4:])):
            # check for entries that are not separated by white space
            matchResult = re.search('([0-9]-[0-9])', lineSplit[4 + i])
            if matchResult != None:
                firstItemEndIndex = matchResult.span(0)[0]
                orbitalEnergies.append(lineSplit[4 + i][:firstItemEndIndex + 1])
                orbitalEnergies.append(lineSplit[4 + i][firstItemEndIndex + 1:])
            else:
                orbitalEnergies.append(lineSplit[4 + i])

        return list(map(float, orbitalEnergies))

    def _extractEnthalpyEnergy(self, startIndex):

        lineSplit = self.lines[startIndex].split()
        return float(lineSplit[6])

    def _extractGibbsEnergy(self, startIndex):

        lineSplit = self.lines[startIndex].split()
        return float(lineSplit[7])

    def _extractZpeCorrection(self, startIndex):

        lineSplit = self.lines[startIndex].split()
        return float(lineSplit[2])

    def _extractHeatCapacity(self, startIndex):

        lineSplit = self.lines[startIndex].split()
        return float(lineSplit[2])

    def _extractEntropy(self, startIndex):

        lineSplit = self.lines[startIndex].split()
        return float(lineSplit[3])

    def _extractAtomicNumbers(self, startIndex):

        atomicNumbers = []

        for i in range(startIndex, startIndex + self.nAtoms, 1):
            # split line at any white space
            lineSplit = self.lines[i].split()
            # read out data (index number based on Gaussian output format)
            atomicNumbers.append(int(lineSplit[1]))
        
        return atomicNumbers

    def _extractGeometricData(self, startIndex):

        geometricData = []

        for i in range(startIndex, startIndex + self.nAtoms, 1):
            # split line at any white space
            lineSplit = self.lines[i].split()
            # read out data (index number based on Gaussian output format)
            xyz = [float(lineSplit[3]), float(lineSplit[4]), float(lineSplit[5])]
            geometricData.append(xyz)

        return geometricData

    def _extractNaturalAtomicCharges(self, startIndex):
        
        naturalAtomicCharges = []

        for i in range(startIndex, startIndex + self.nAtoms, 1):
            # split line at any white space
            lineSplit = self.lines[i].split()
            # read out data (index number based on Gaussian output format)
            naturalAtomicCharges.append(float(lineSplit[2]))
        
        return naturalAtomicCharges

    def _extractNaturalElectronConfiguration(self, startIndex):
        
        naturalElectronConfiguration = []

        for i in range(startIndex, startIndex + self.nAtoms, 1):
            
            # single atom electron configuration ([s, p, d, f])
            electronConfiguration = [0.0, 0.0, 0.0, 0.0]

            # split line at any white space
            lineSplit = self.lines[i].split()
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

    def _extractIndexMatrix(self, startIndex):

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
                lineSplit = self.lines[i].split()
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

    def _extractLmoBondData(self, startIndex):

        # output matrix
        lmoBondDataMatrix = [[0 for x in range(self.nAtoms)] for y in range(self.nAtoms)]

        # rename for brevity
        i = startIndex

        while(self.lines[i] != ''):
            
            lineSplit = self.lines[i].split()

            # get atom indices and the corresponding LMO bond order
            indexA = int(lineSplit[0]) - 1
            indexB = int(lineSplit[1]) - 1
            lmoBondOrder = float(lineSplit[3])

            lmoBondDataMatrix[indexA][indexB] += lmoBondOrder
            lmoBondDataMatrix[indexB][indexA] += lmoBondOrder

            i += 1

        return lmoBondDataMatrix

    def _extractNboEnergies(self, startIndex):

        data = []

        # rename index for brevity
        i = startIndex

        while('NATURAL LOCALIZED MOLECULAR ORBITAL' not in self.lines[i]):

            lineSplit = list(filter(None, re.split(r'\(|\)|([0-9]+)-| ', self.lines[i])))

            if len(lineSplit) > 3:

                energy = 0

                if lineSplit[1] == 'LP' or lineSplit[1] == 'LV':
                    energy = float(lineSplit[6])
                elif lineSplit[1] == 'BD' or lineSplit[1] == 'BD*':
                    energy = float(lineSplit[8])
                else:
                    i += 1
                    continue

                id = int(lineSplit[0].replace('.', ''))
                data.append([id, energy])

            i += 1

        return data

    def _extractNboData(self, startIndex):
        
        # final output variables
        lonePairData = [] 
        antibondPairData = []
        bondPairData = []
        loneVacancyData = []

        # rename index for brevity
        i = startIndex

        while not self.lines[i] == '':

            # split line at any white space
            lineSplit = self.lines[i].replace('(','').split()
            if len(lineSplit) > 3:

                # lone pairs
                if lineSplit[2] == 'LP':

                    lonePair = self._extractLonePairData(i)
                    lonePairData.append(lonePair)

                # bonds
                if lineSplit[2] == 'BD':
                    
                    bond = self._extractBondingData(i)
                    bondPairData.append(bond)

                # anti bonds
                if lineSplit[2] == 'BD*':
                    
                    antibond = self._extractBondingData(i)
                    antibondPairData.append(antibond)

                # lone vacancy
                if lineSplit[2] == 'LV':

                    loneVacancy = self._extractLonePairData(i)
                    loneVacancyData.append(loneVacancy)

            i += 1

        return lonePairData, loneVacancyData, bondPairData, antibondPairData

    def _extractLonePairData(self, startIndex):

        # get ID of entry
        id = int(self.lines[startIndex].split('.')[0])

        # obtain atom position
        lineSplit = list(filter(None, re.split(r'\(|\)| ', self.lines[startIndex])))[5:]
        atomPosition = int(lineSplit[0]) - 1

        # obtain occupation
        lineSplit = list(filter(None, re.split(r'\(|\)| ', self.lines[startIndex])))
        fullOccupation = float(lineSplit[1])

        # get occupation from both lines using regex (values in brackets)
        mergedLines = (self.lines[startIndex] + self.lines[startIndex + 1]).replace(' ', '')
        result = re.findall('\((.{4,6})%\)', mergedLines)
        occupations = list(map(float, result))

        # check that length of occupation list is correct
        assert len(occupations) == 4

        # return id, atom position, occupation and percent occupations
        # divide occupations by 100 (get rid of %)
        return [id, atomPosition, fullOccupation, [x / 100 for x in occupations]]

    def _extractBondingData(self, startIndex):

        # get ID of entry
        id = int(self.lines[startIndex].split('.')[0])

        # obtain atom positions
        lineSplit = list(filter(None, re.split(r'\(|\)|-| ', self.lines[startIndex])))[4:]
        atomPositions = [int(lineSplit[-3]) - 1, int(lineSplit[-1]) - 1]

        # obtain occupation
        lineSplit = list(filter(None, re.split(r'\(|\)| ', self.lines[startIndex])))
        fullOccupation = float(lineSplit[1])

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

        # check that length of occupation list is correct
        assert len(occupations) == 4

        # return id, atom position, occupation and percent occupations
        # divide occupations by 100 (get rid of %)
        return [id, atomPositions, fullOccupation, [x / 200 for x in occupations]]
        # return atomPositions, [x / 200 for x in occupations]
