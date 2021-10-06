import re
from operator import add

from nbo2graph.qm_data import QmData
from nbo2graph.file_handler import FileHandler

class DataParser:
    
    """Class for reading relevant data from Gaussian output files."""

    def __init__(self, file_path):

        """Constructor

        Args:
            file_path (string): Path to the Gaussian output file.
        """

        self.file_path = file_path
        self.lines = FileHandler.read_file(file_path).split('\n')
        self.n_atoms = self._get_number_of_atoms()

    def _get_number_of_atoms(self):

        for i in range(len(self.lines)):
            # find line that contain atom number
            if 'NAtoms=' in self.lines[i]:

                # get position in line
                line_split = self.lines[i].split()
                n_atomsIndex = line_split.index('NAtoms=') + 1

                # return
                return int(line_split[n_atomsIndex])
        
        raise Exception('Could not find number of atoms in file.')

    def parse(self):

        # output variable
        qm_data = QmData()
        qm_data.n_atoms = self.n_atoms

        # get csd token from file name
        qm_data.csd_identifier = ''.join(self.file_path.split('/')[-1].split('.')[0:-1])

        # variable that shows if scan is currently in SVP or TZVP region of output file
        region_state = ''
        for i in range(len(self.lines)):

            if 'def2SVP' in self.lines[i]:
                region_state = 'svp'
            elif 'def2TZVP' in self.lines[i]:
                region_state = 'tzvp'

            # search for keywords and if found call appropriate functions with start index
            # the start index addition offset is based on the Gaussian output format
            if 'Standard orientation' in self.lines[i]:
                qm_data.atomic_numbers = self._extract_atomic_numbers(i + 5)
                qm_data.geometric_data = self._extract_geometric_data(i + 5)

            if 'Summary of Natural Population Analysis' in self.lines[i]:
                qm_data.natural_atomic_charges = self._extract_natural_atomic_charges(i + 6)

            if 'Natural Electron Configuration' in self.lines[i]:
                qm_data.natural_electron_configuration = self._extract_natural_electron_configuration(i + 2)

            if 'Wiberg bond index matrix' in self.lines[i]:
                qm_data.wiberg_index_matrix = self._extract_index_matrix(i + 4)

            if 'Atom-Atom Net Linear NLMO/NPA' in self.lines[i]:
                qm_data.nbo_bond_order_matrix = self._extract_index_matrix(i + 4)

            if 'Bond orbital / Coefficients / Hybrids' in self.lines[i]:
                qm_data.lone_pair_data, qm_data.lone_vacancy_data, qm_data.bond_pair_data, qm_data.antibond_pair_data = self._extract_nbo_data(i + 2)
        
            if 'NATURAL BOND ORBITALS' in self.lines[i]:
                qm_data.nbo_energies = self._extract_nbo_energies(i + 7)

            if 'Atom I' in self.lines[i]:
                qm_data.lmo_bond_order_matrix = self._extract_lmo_bond_data(i + 1)

            if 'Charge = ' in self.lines[i]:
                qm_data.charge = self._extract_charge(i)

            if 'Stoichiometry' in self.lines[i]:
                qm_data.stoichiometry = self._extract_stoichiometry(i)

            if 'Molecular mass' in self.lines[i]:
                qm_data.molecular_mass = self._extract_molecular_mass(i)

            if 'Grimme-D3(BJ) Dispersion energy=' in self.lines[i]:
                if region_state == 'svp':
                    qm_data.svp_dispersion_energy = self._extract_dispersion_energy(i)
                elif region_state == 'tzvp':
                    qm_data.tzvp_dispersion_energy = self._extract_dispersion_energy(i)

            if 'SCF Done' in self.lines[i]:
                if region_state == 'svp':
                    qm_data.svp_electronic_energy = self._extract_electronic_energy(i)
                elif region_state == 'tzvp':
                    qm_data.tzvp_electronic_energy = self._extract_electronic_energy(i)

            if 'Dipole moment (field-independent basis, Debye)' in self.lines[i]:
                if region_state == 'svp':
                    qm_data.svp_dipole_moment = self._extract_dipole_moment(i + 1)
                elif region_state == 'tzvp':
                    qm_data.tzvp_dipole_moment = self._extract_dipole_moment(i + 1)
            
            if 'Isotropic polarizability' in self.lines[i]:
                qm_data.polarisability = self._extract_polarisability(i)

            if 'Frequencies -- ' in self.lines[i]:
                if qm_data.frequencies == None:
                    qm_data.frequencies = self._extract_frequency(i)
                else:
                    qm_data.frequencies.extend(self._extract_frequency(i))

            if 'Zero-point correction=' in self.lines[i]:
                qm_data.zpe_correction = self._extract_zpe_correction(i)

            if 'Sum of electronic and thermal Enthalpies=' in self.lines[i]:
                qm_data.enthalpy_energy = self._extract_enthalpy_energy(i)

            if 'Sum of electronic and thermal Free Energies=' in self.lines[i]:
                qm_data.gibbs_energy = self._extract_gibbs_energy(i)
                qm_data.heat_capacity = self._extract_heat_capacity(i + 4)
                qm_data.entropy = self._extract_entropy(i + 4)

            if 'Alpha  occ. eigenvalues' in self.lines[i]:
                if region_state == 'svp':
                    if qm_data.svp_occupied_orbital_energies == None:
                        qm_data.svp_occupied_orbital_energies = self._extract_orbital_energies(i)
                    else:
                        qm_data.svp_occupied_orbital_energies.extend(self._extract_orbital_energies(i))
                elif region_state == 'tzvp':
                    if qm_data.tzvp_occupied_orbital_energies == None:
                        qm_data.tzvp_occupied_orbital_energies = self._extract_orbital_energies(i)
                    else:    
                        qm_data.tzvp_occupied_orbital_energies.extend(self._extract_orbital_energies(i))

            if 'Alpha virt. eigenvalues' in self.lines[i]:
                if region_state == 'svp':
                    if qm_data.svp_virtual_orbital_energies == None:
                        qm_data.svp_virtual_orbital_energies = self._extract_orbital_energies(i)
                    else:
                        qm_data.svp_virtual_orbital_energies.extend(self._extract_orbital_energies(i))
                elif region_state == 'tzvp':
                    if qm_data.tzvp_virtual_orbital_energies == None:
                        qm_data.tzvp_virtual_orbital_energies = self._extract_orbital_energies(i)
                    else:    
                        qm_data.tzvp_virtual_orbital_energies.extend(self._extract_orbital_energies(i))

        # calculate extra properties such as delta values, HOMO, LUMU, etc.
        qm_data.calculate_properties()

        return qm_data

    # - - - extraction functions - - - #

    # Some of the following extraction functions are redundant in the sense that for some properties
    # the extraction procedures are identical. The distinction between these functions is kept 
    # nonetheless to ensure maintainability (e.g. when the Gaussian output format changes).

    def _extract_charge(self, start_index):

        line_split = self.lines[start_index].split()
        return int(line_split[2])

    def _extract_stoichiometry(self, start_index):

        line_split = self.lines[start_index].split()
        return line_split[1]

    def _extract_molecular_mass(self, start_index):

        line_split = self.lines[start_index].split()
        return float(line_split[2])

    def _extract_dispersion_energy(self, start_index):

        line_split = self.lines[start_index].split()
        return float(line_split[4])

    def _extract_electronic_energy(self, start_index):

        line_split = self.lines[start_index].split()
        return float(line_split[4])

    def _extract_dipole_moment(self, start_index):

        line_split = self.lines[start_index].split()
        return float(line_split[7])

    def _extract_polarisability(self, start_index):

        line_split = self.lines[start_index].split()
        return float(line_split[5])

    def _extract_frequency(self, start_index):

        line_split = self.lines[start_index].split()
        return list(map(float, line_split[2:]))

    def _extract_orbital_energies(self, start_index):

        line_split = self.lines[start_index].split()

        # build output list
        orbital_energies = []
        for i in range(len(line_split[4:])):
            # check for entries that are not separated by white space
            match_result = re.search('([0-9]-[0-9])', line_split[4 + i])
            if match_result != None:
                first_item_end_index = match_result.span(0)[0]
                orbital_energies.append(line_split[4 + i][:first_item_end_index + 1])
                orbital_energies.append(line_split[4 + i][first_item_end_index + 1:])
            else:
                orbital_energies.append(line_split[4 + i])

        return list(map(float, orbital_energies))

    def _extract_enthalpy_energy(self, start_index):

        line_split = self.lines[start_index].split()
        return float(line_split[6])

    def _extract_gibbs_energy(self, start_index):

        line_split = self.lines[start_index].split()
        return float(line_split[7])

    def _extract_zpe_correction(self, start_index):

        line_split = self.lines[start_index].split()
        return float(line_split[2])

    def _extract_heat_capacity(self, start_index):

        line_split = self.lines[start_index].split()
        return float(line_split[2])

    def _extract_entropy(self, start_index):

        line_split = self.lines[start_index].split()
        return float(line_split[3])

    def _extract_atomic_numbers(self, start_index):

        atomic_numbers = []

        for i in range(start_index, start_index + self.n_atoms, 1):
            # split line at any white space
            line_split = self.lines[i].split()
            # read out data (index number based on Gaussian output format)
            atomic_numbers.append(int(line_split[1]))
        
        return atomic_numbers

    def _extract_geometric_data(self, start_index):

        geometric_data = []

        for i in range(start_index, start_index + self.n_atoms, 1):
            # split line at any white space
            line_split = self.lines[i].split()
            # read out data (index number based on Gaussian output format)
            xyz = [float(line_split[3]), float(line_split[4]), float(line_split[5])]
            geometric_data.append(xyz)

        return geometric_data

    def _extract_natural_atomic_charges(self, start_index):
        
        natural_atomic_charges = []

        for i in range(start_index, start_index + self.n_atoms, 1):
            # split line at any white space
            line_split = self.lines[i].split()
            # read out data (index number based on Gaussian output format)
            natural_atomic_charges.append(float(line_split[2]))
        
        return natural_atomic_charges

    def _extract_natural_electron_configuration(self, start_index):
        
        natural_electron_configuration = []

        for i in range(start_index, start_index + self.n_atoms, 1):
            
            # single atom electron configuration ([s, p, d, f])
            electron_configuration = [0.0, 0.0, 0.0, 0.0]

            # split line at any white space
            line_split = self.lines[i].split()
            # remove first two columns of data, rejoin and remove '[core]'
            line_cleaned = ''.join(line_split[2:]).replace('[core]', '')
            # split at '(' and ')' so that orbital type and config can be extracted
            line_cleanedSplit = re.split(r'\(|\)', line_cleaned)

            for j in range(0, len(line_cleanedSplit), 2):

                # add value to appropriate list element
                if 's' in line_cleanedSplit[j]:
                    electron_configuration[0] += float(line_cleanedSplit[j + 1])
                elif 'p' in line_cleanedSplit[j]:
                    electron_configuration[1] += float(line_cleanedSplit[j + 1])
                elif 'd' in line_cleanedSplit[j]:
                    electron_configuration[2] += float(line_cleanedSplit[j + 1])
                elif 'f' in line_cleanedSplit[j]:
                    electron_configuration[3] += float(line_cleanedSplit[j + 1])
                else:
                    continue

            # append to full list
            natural_electron_configuration.append(electron_configuration)

        return natural_electron_configuration

    def _extract_index_matrix(self, start_index):

        # setup n_atoms x n_atoms matrix for Wiberg indices
        wiberg_index_matrix = [[0 for x in range(self.n_atoms)] for y in range(self.n_atoms)] 

        # counter for keeping track how many columns have been taken care of
        # this is necessary because the Gaussian output file prints the Wiberg
        # index matrix in blocks of columns
        n_columns_processed = 0

        # run until all columns have been processed
        while n_columns_processed < self.n_atoms:

            n_columns = None
            for i in range(start_index, start_index + self.n_atoms, 1):
                # split line at any white space
                line_split = self.lines[i].split()
                # drop first two columns so that only Wiberg indices remain
                line_split = line_split[2:]
            
                # check that the number of columns is the same
                if n_columns == None:
                    n_columns = len(line_split)
                else:
                    assert n_columns == len(line_split)

                # read out data (index number based on Gaussian output format)
                for j in range(len(line_split)):
                    # write matrix element
                    wiberg_index_matrix[i-start_index][j + n_columns_processed] = float(line_split[j])

            n_columns_processed += n_columns

            # set start_index to the next block
            start_index += self.n_atoms + 3

        return wiberg_index_matrix

    def _extract_lmo_bond_data(self, start_index):

        # output matrix
        lmo_bond_data_matrix = [[0 for x in range(self.n_atoms)] for y in range(self.n_atoms)]

        # rename for brevity
        i = start_index

        while(self.lines[i] != ''):
            
            line_split = self.lines[i].split()

            # get atom indices and the corresponding LMO bond order
            index_a = int(line_split[0]) - 1
            index_b = int(line_split[1]) - 1
            lmo_bond_order = float(line_split[3])

            lmo_bond_data_matrix[index_a][index_b] += lmo_bond_order
            lmo_bond_data_matrix[index_b][index_a] += lmo_bond_order

            i += 1

        return lmo_bond_data_matrix

    def _extract_nbo_energies(self, start_index):

        data = []

        # rename index for brevity
        i = start_index

        while('NATURAL LOCALIZED MOLECULAR ORBITAL' not in self.lines[i]):

            line_split = list(filter(None, re.split(r'\(|\)|([0-9]+)-| ', self.lines[i])))

            if len(line_split) > 3:

                energy = 0

                if line_split[1] == 'LP' or line_split[1] == 'LV':
                    energy = float(line_split[6])
                elif line_split[1] == 'BD' or line_split[1] == 'BD*':
                    energy = float(line_split[8])
                else:
                    i += 1
                    continue

                id = int(line_split[0].replace('.', ''))
                data.append([id, energy])

            i += 1

        return data

    def _extract_nbo_data(self, start_index):
        
        # final output variables
        lone_pair_data = [] 
        antibond_pair_data = []
        bond_pair_data = []
        lone_vacancy_data = []

        # rename index for brevity
        i = start_index

        while not self.lines[i] == '':

            # split line at any white space
            line_split = self.lines[i].replace('(','').split()
            if len(line_split) > 3:

                # lone pairs
                if line_split[2] == 'LP':

                    lone_pair = self._extract_lone_pair_data(i)
                    lone_pair_data.append(lone_pair)

                # bonds
                if line_split[2] == 'BD':
                    
                    bond = self._extract_bonding_data(i)
                    bond_pair_data.append(bond)

                # anti bonds
                if line_split[2] == 'BD*':
                    
                    antibond = self._extract_bonding_data(i)
                    antibond_pair_data.append(antibond)

                # lone vacancy
                if line_split[2] == 'LV':

                    lone_vacancy = self._extract_lone_pair_data(i)
                    lone_vacancy_data.append(lone_vacancy)

            i += 1

        return lone_pair_data, lone_vacancy_data, bond_pair_data, antibond_pair_data

    def _extract_lone_pair_data(self, start_index):

        # get ID of entry
        id = int(self.lines[start_index].split('.')[0])

        # obtain atom position
        line_split = list(filter(None, re.split(r'\(|\)| ', self.lines[start_index])))[5:]
        atom_position = int(line_split[0]) - 1

        # obtain occupation
        line_split = list(filter(None, re.split(r'\(|\)| ', self.lines[start_index])))
        full_occupation = float(line_split[1])

        # get occupation from both lines using regex (values in brackets)
        merged_lines = (self.lines[start_index] + self.lines[start_index + 1]).replace(' ', '')
        result = re.findall(r'\((.{4,6})%\)', merged_lines)
        occupations = list(map(float, result))

        # check that length of occupation list is correct
        assert len(occupations) == 4

        # return id, atom position, occupation and percent occupations
        # divide occupations by 100 (get rid of %)
        return [id, atom_position, full_occupation, [x / 100 for x in occupations]]

    def _extract_bonding_data(self, start_index):

        # get ID of entry
        id = int(self.lines[start_index].split('.')[0])

        # obtain atom positions
        line_split = list(filter(None, re.split(r'\(|\)|-| ', self.lines[start_index])))[4:]
        atom_positions = [int(line_split[-3]) - 1, int(line_split[-1]) - 1]

        # obtain occupation
        line_split = list(filter(None, re.split(r'\(|\)| ', self.lines[start_index])))
        full_occupation = float(line_split[1])

        # get occupation from both lines using regex (values in brackets)
        merged_lines = (self.lines[start_index + 1] + self.lines[start_index + 2]).replace(' ', '')
        result = re.findall(r'\((.{3,5})%\)', merged_lines)
        occupations1 = list(map(float, result))[1:]
        # append zeros to account for atoms that do not have higher orbital types
        while len(occupations1) < 4:
            occupations1.append(0)

        # find line with second data
        i = start_index + 3
        while not '(' in self.lines[i]:
            i += 1

        # get occupation from both lines using regex (values in brackets)
        merged_lines = (self.lines[i] + self.lines[i + 1]).replace(' ', '')
        result = re.findall(r'\((.{3,5})%\)', merged_lines)
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
        return [id, atom_positions, full_occupation, [x / 200 for x in occupations]]
        # return atom_positions, [x / 200 for x in occupations]
