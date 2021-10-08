from dataclasses import dataclass

@dataclass
class QmData():

    """Class for storing relevant QM data."""

    # attributes
    csd_code: str = None
    stoichiometry: str = None

    # basic information
    n_atoms: float = None
    atomic_numbers: list[int] = None
    geometric_data: list[list[float]] = None
    bond_distance_matrix: list[list[float]] = None

    charge: int = None # e
    molecular_mass: float = None # amu
    polarisability: float = None # Bohr ^ 3

    # energies
    svp_dispersion_energy: float = None # Ha
    tzvp_dispersion_energy: float = None # Ha

    svp_electronic_energy: float = None # Ha
    tzvp_electronic_energy: float = None # Ha

    svp_dipole_moment: float = None # D
    tzvp_dipole_moment: float = None # D

    # orbital data
    svp_occupied_orbital_energies: list[float] = None
    tzvp_occupied_orbital_energies: list[float] = None
    svp_virtual_orbital_energies: list[float] = None
    tzvp_virtual_orbital_energies: list[float] = None

    svp_homo_energy: float = None # Ha
    svp_lumo_energy: float = None # Ha
    tzvp_homo_energy: float = None # Ha
    tzvp_lumo_energy: float = None # Ha

    svp_homo_lumo_gap: float = None # Ha
    tzvp_homo_lumo_gap: float = None # Ha

    # vibrational frequencies
    frequencies: list[float] = None # cm ^ -1
    lowest_vibrational_frequency: float = None # cm ^ -1
    highest_vibrational_frequency: float = None # cm ^ -1

    # thermo chemistry
    heat_capacity: float = None # Cal/Mol-Kelvin
    entropy: float = None # Cal/Mol-Kelvin

    zpe_correction: float = None # Ha
    enthalpy_energy: float = None # Ha
    gibbs_energy: float = None # Ha
    corrected_enthalpy_energy: float = None # Ha
    corrected_gibbs_energy: float = None # Ha

    # electronic data
    natural_atomic_charges: list[float] = None
    natural_electron_configuration: list[list[float]] = None

    # bond data
    wiberg_index_matrix: list[list[float]] = None
    wiberg_atom_totals: list[float] = None

    # lmo bond data
    lmo_bond_order_matrix: list[list[float]] = None

    # nbo bond data
    nbo_bond_order_matrix: list[list[float]] = None
    nbo_bond_order_totals: list[float] = None

    # nbo data
    lone_pair_data = None
    lone_vacancy_data = None
    bond_pair_data = None
    antibond_pair_data = None
    nbo_energies: list[list] = None

    lone_pair_data_full = None
    lone_vacancy_data_full = None
    bond_pair_data_full = None
    antibond_pair_data_full = None

    # deltas
    dispersion_energy_delta: float = None # Ha
    electronic_energy_delta: float = None # Ha
    dipole_moment_delta: float = None # D
    homo_lumo_gap_delta: float = None # Ha

    def calculate_properties(self):

        """Calculates composite properties such as HOMO-LUMO gap and delta values/corrections between SVP and TZVP."""

        # geometric properties

        # calculate distance matrix
        distance_matrix = [[0 for x in range(self.n_atoms)] for y in range(self.n_atoms)]
        for i in range(len(distance_matrix) - 1):
            for j in range(i + 1, len(distance_matrix), 1):
                distance = QmData._calculate_euclidean_distance(self.geometric_data[i], self.geometric_data[j])
                distance_matrix[i][j] = distance
                distance_matrix[j][i] = distance
        self.bond_distance_matrix = distance_matrix

        # physical properties

        # calculate homo lumo svp
        self.svp_homo_energy = self.svp_occupied_orbital_energies[-1]
        self.svp_lumo_energy = self.svp_virtual_orbital_energies[0]

        # calculate homo lumo tzvp
        self.tzvp_homo_energy = self.tzvp_occupied_orbital_energies[-1]
        self.tzvp_lumo_energy = self.tzvp_virtual_orbital_energies[0]

        # calculate homo lumo gaps
        self.svp_homo_lumo_gap = self.svp_lumo_energy - self.svp_homo_energy
        self.tzvp_homo_lumo_gap = self.tzvp_lumo_energy - self.tzvp_homo_energy

        # get lowest and highest vibrational frequencies
        self.lowest_vibrational_frequency = self.frequencies[0]
        self.highest_vibrational_frequency = self.frequencies[-1]

        # calculate ZPE, thermal, and internal energy corrections
        self.corrected_enthalpy_energy = self.enthalpy_energy - self.svp_electronic_energy

        # calculate ZPE, thermal, internal, and entropy energy corrections
        self.corrected_gibbs_energy =  self.gibbs_energy - self.svp_electronic_energy

        # SVP - TZVP deltas

        # calculate svp - tzvp dispersion energy delta
        self.dispersion_energy_delta = self.svp_dispersion_energy - self.tzvp_dispersion_energy
        
        # calculate svp - tzvp electronic energy delta
        self.electronic_energy_delta = self.svp_electronic_energy - self.tzvp_electronic_energy
       
        # calculate svp - tzvp dipole moment delta
        self.dipole_moment_delta = self.svp_dipole_moment - self.tzvp_dipole_moment

        # calculate svp - tzvp homo lumo gap delta
        self.homo_lumo_gap_delta = self.svp_homo_lumo_gap - self.tzvp_homo_lumo_gap

        # calculate Wiberg atom-wise totals
        self.wiberg_atom_totals = []
        for i in range(len(self.wiberg_index_matrix)):
            self.wiberg_atom_totals.append(sum(self.wiberg_index_matrix[i]))

        # calculate nbo bond order atom-wise totals
        self.nbo_bond_order_totals = []
        for i in range(len(self.nbo_bond_order_matrix)):
            self.nbo_bond_order_totals.append(sum(self.nbo_bond_order_matrix[i]))

        # merge nbo data with corresponding energies        
        self.lone_pair_data_full = self._merge_nbo_data(self.lone_pair_data)
        self.lone_vacancy_data_full = self._merge_nbo_data(self.lone_vacancy_data)
        self.bond_pair_data_full = self._merge_nbo_data(self.bond_pair_data)
        self.antibond_pair_data_full = self._merge_nbo_data(self.antibond_pair_data)

    def _merge_nbo_data(self, nbo_data):

        merged_data = []
        # readout IDs of energies to match energies to corresponding nbo entries
        energy_ids = [x[0] for x in self.nbo_energies]

        for i in range(len(nbo_data)):

            # get the index of the ID of the current nbo data point
            nbo_energy_index = energy_ids.index(nbo_data[i][0])

            # merge together and drop ID
            # [ atom_position, energy, occupation value, [occupations] ]
            data_point = [nbo_data[i][1]]
            data_point.append(self.nbo_energies[nbo_energy_index][1])
            data_point.append(nbo_data[i][2])
            data_point.append(nbo_data[i][3])
            
            # append to output list
            merged_data.append(data_point)
        
        return merged_data
    
    @staticmethod
    def _calculate_euclidean_distance(x, y):
        
        # make sure both lists have the same length
        assert len(x) == len(y)

        # get dimension wise squared distances
        squares = [(a - b) ** 2 for a, b in zip(x, y)]

        # return sum of square root
        return sum(squares) ** 0.5