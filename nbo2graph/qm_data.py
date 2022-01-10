from nbo2graph.nbo_data_point import NboDataPoint
from nbo2graph.nbo_single_data_point import NboSingleDataPoint
from nbo2graph.nbo_double_data_point import NboDoubleDataPoint

# list of keys to be expected from the data parser dict
DICT_KEYS = ['n_atoms', 'id', 'charge', 'stoichiometry', 'atomic_numbers', 'geometric_data',
             'svp_dispersion_energy', 'svp_electronic_energy', 'polarisability', 'svp_occupied_orbital_energies',
             'svp_virtual_orbital_energies', 'svp_dipole_moment', 'frequencies', 'molecular_mass', 'zpe_correction',
             'enthalpy_energy', 'gibbs_energy', 'heat_capacity', 'entropy', 'tzvp_dispersion_energy', 'tzvp_electronic_energy',
             'tzvp_occupied_orbital_energies', 'tzvp_virtual_orbital_energies', 'tzvp_dipole_moment', 'natural_atomic_charges',
             'natural_electron_configuration', 'natural_electron_population', 'wiberg_bond_order_matrix', 'nbo_data', 'three_center_nbos',
             'sopa_data', 'nbo_energies', 'lmo_bond_order_matrix', 'nlmo_bond_order_matrix', 'three_center_nbos']


class QmData():

    """Class for storing relevant QM data."""

    def __init__(self,
                 id: str,
                 stoichiometry: str,
                 n_atoms: int,
                 atomic_numbers: list[int],
                 geometric_data: list[list[float]],
                 charge: int,
                 molecular_mass: float,
                 polarisability: float,
                 svp_dispersion_energy: float,
                 tzvp_dispersion_energy: float,
                 svp_electronic_energy: float,
                 tzvp_electronic_energy: float,
                 svp_dipole_moment: float,
                 tzvp_dipole_moment: float,
                 svp_occupied_orbital_energies: list[float],
                 tzvp_occupied_orbital_energies: list[float],
                 svp_virtual_orbital_energies: list[float],
                 tzvp_virtual_orbital_energies: list[float],
                 frequencies: list[float],
                 heat_capacity: float,
                 entropy: float,
                 zpe_correction: float,
                 enthalpy_energy: float,
                 gibbs_energy: float,
                 natural_atomic_charges: list[float],
                 natural_electron_configuration: list[list[float]],
                 natural_electron_population: list[list[float]],
                 wiberg_bond_order_matrix: list[list[float]],
                 lmo_bond_order_matrix: list[list[float]],
                 nlmo_bond_order_matrix: list[list[float]],
                 nbo_data: NboDataPoint,
                 nbo_energies: list[list],
                 sopa_data) -> None:

        # misc
        self.id = id
        self.stoichiometry = stoichiometry

        # basic information
        self.n_atoms = n_atoms
        self.atomic_numbers = atomic_numbers
        self.geometric_data = geometric_data

        self.charge = charge
        self.molecular_mass = molecular_mass
        self.polarisability = polarisability

        # energies
        self.svp_dispersion_energy = svp_dispersion_energy
        self.tzvp_dispersion_energy = tzvp_dispersion_energy

        self.svp_electronic_energy = svp_electronic_energy
        self.tzvp_electronic_energy = tzvp_electronic_energy

        self.svp_dipole_moment = svp_dipole_moment
        self.tzvp_dipole_moment = tzvp_dipole_moment

        # orbital data
        self.svp_occupied_orbital_energies = svp_occupied_orbital_energies
        self.tzvp_occupied_orbital_energies = tzvp_occupied_orbital_energies
        self.svp_virtual_orbital_energies = svp_virtual_orbital_energies
        self.tzvp_virtual_orbital_energies = tzvp_virtual_orbital_energies

        # vibrational frequencies
        self.frequencies = frequencies

        # thermo chemistry
        self.heat_capacity = heat_capacity
        self.entropy = entropy

        self.zpe_correction = zpe_correction
        self.enthalpy_energy = enthalpy_energy
        self.gibbs_energy = gibbs_energy
        # calculate ZPE, thermal, and internal energy corrections
        self.corrected_enthalpy_energy = self.enthalpy_energy - self.svp_electronic_energy
        # calculate ZPE, thermal, internal, and entropy energy corrections
        self.corrected_gibbs_energy = self.gibbs_energy - self.svp_electronic_energy

        # electronic data
        self.natural_atomic_charges = natural_atomic_charges
        self.natural_electron_configuration = natural_electron_configuration
        self.natural_electron_population = natural_electron_population

        # bond data
        self.wiberg_bond_order_matrix = wiberg_bond_order_matrix
        # lmo bond data
        self.lmo_bond_order_matrix = lmo_bond_order_matrix
        # nbo bond data
        self.nlmo_bond_order_matrix = nlmo_bond_order_matrix

        # merge nbo data with corresponding energies
        self.nbo_data = self._merge_nbo_data(nbo_data, nbo_energies)

        # data for NBO SOPA
        self.sopa_data = sopa_data

        # get individual lists for LP, LV, BD, BD*
        self._get_nbo_individual_lists()

        # calculate additional composite properties
        self._get_frequencies()
        self._calculate_atom_distance_matrix()
        self._calculate_bond_order_totals()
        self._calculate_homo_lumo_energies()
        self._calculate_delta_values()

    @classmethod
    def from_dict(cls, qm_data_dict: dict):

        # set values of missing keys to None
        for key in DICT_KEYS:
            if key not in qm_data_dict.keys():
                qm_data_dict[key] = None

        return cls(id=qm_data_dict['id'],
                   stoichiometry=qm_data_dict['stoichiometry'],
                   n_atoms=qm_data_dict['n_atoms'],
                   atomic_numbers=qm_data_dict['atomic_numbers'],
                   geometric_data=qm_data_dict['geometric_data'],
                   charge=qm_data_dict['charge'],
                   molecular_mass=qm_data_dict['molecular_mass'],
                   polarisability=qm_data_dict['polarisability'],
                   svp_dispersion_energy=qm_data_dict['svp_dispersion_energy'],
                   tzvp_dispersion_energy=qm_data_dict['tzvp_dispersion_energy'],
                   svp_electronic_energy=qm_data_dict['svp_electronic_energy'],
                   tzvp_electronic_energy=qm_data_dict['tzvp_electronic_energy'],
                   svp_dipole_moment=qm_data_dict['svp_dipole_moment'],
                   tzvp_dipole_moment=qm_data_dict['tzvp_dipole_moment'],
                   svp_occupied_orbital_energies=qm_data_dict['svp_occupied_orbital_energies'],
                   tzvp_occupied_orbital_energies=qm_data_dict['tzvp_occupied_orbital_energies'],
                   svp_virtual_orbital_energies=qm_data_dict['svp_virtual_orbital_energies'],
                   tzvp_virtual_orbital_energies=qm_data_dict['tzvp_virtual_orbital_energies'],
                   frequencies=qm_data_dict['frequencies'],
                   heat_capacity=qm_data_dict['heat_capacity'],
                   entropy=qm_data_dict['entropy'],
                   zpe_correction=qm_data_dict['zpe_correction'],
                   enthalpy_energy=qm_data_dict['enthalpy_energy'],
                   gibbs_energy=qm_data_dict['gibbs_energy'],
                   natural_atomic_charges=qm_data_dict['natural_atomic_charges'],
                   natural_electron_configuration=qm_data_dict['natural_electron_configuration'],
                   natural_electron_population=qm_data_dict['natural_electron_population'],
                   wiberg_bond_order_matrix=qm_data_dict['wiberg_bond_order_matrix'],
                   lmo_bond_order_matrix=qm_data_dict['lmo_bond_order_matrix'],
                   nlmo_bond_order_matrix=qm_data_dict['nlmo_bond_order_matrix'],
                   nbo_data=qm_data_dict['nbo_data'],
                   nbo_energies=qm_data_dict['nbo_energies'],
                   sopa_data=qm_data_dict['sopa_data'])

    def _get_frequencies(self):

        self.lowest_vibrational_frequency = self.frequencies[0]
        self.highest_vibrational_frequency = self.frequencies[-1]

    def _calculate_homo_lumo_energies(self):

        # calculate homo lumo svp
        self.svp_homo_energy = self.svp_occupied_orbital_energies[-1]
        self.svp_lumo_energy = self.svp_virtual_orbital_energies[0]
        # calculate homo lumo tzvp
        self.tzvp_homo_energy = self.tzvp_occupied_orbital_energies[-1]
        self.tzvp_lumo_energy = self.tzvp_virtual_orbital_energies[0]

        # calculate homo lumo gaps
        self.svp_homo_lumo_gap = self.svp_lumo_energy - self.svp_homo_energy
        self.tzvp_homo_lumo_gap = self.tzvp_lumo_energy - self.tzvp_homo_energy

    def _calculate_bond_order_totals(self):

        self.wiberg_bond_order_totals = [sum(bond_orders) for bond_orders in self.wiberg_bond_order_matrix]
        self.lmo_bond_order_totals = [sum(bond_orders) for bond_orders in self.lmo_bond_order_matrix]
        self.nlmo_bond_order_totals = [sum(bond_orders) for bond_orders in self.nlmo_bond_order_matrix]

    def _calculate_delta_values(self):

        # calculate svp - tzvp dispersion energy delta
        self.dispersion_energy_delta = abs(self.svp_dispersion_energy - self.tzvp_dispersion_energy)
        # calculate svp - tzvp electronic energy delta
        self.electronic_energy_delta = abs(self.svp_electronic_energy - self.tzvp_electronic_energy)
        # calculate svp - tzvp dipole moment delta
        self.dipole_moment_delta = abs(self.svp_dipole_moment - self.tzvp_dipole_moment)
        # calculate svp - tzvp homo lumo gap delta
        self.homo_lumo_gap_delta = abs(self.svp_homo_lumo_gap - self.tzvp_homo_lumo_gap)

    def _calculate_atom_distance_matrix(self):

        distance_matrix = [[0 for x in range(self.n_atoms)] for y in range(self.n_atoms)]
        for i in range(len(distance_matrix) - 1):
            for j in range(i + 1, len(distance_matrix), 1):
                distance = QmData._calculate_euclidean_distance(self.geometric_data[i], self.geometric_data[j])
                distance_matrix[i][j] = distance
                distance_matrix[j][i] = distance
        self.bond_distance_matrix = distance_matrix

    def _merge_nbo_data(self, nbo_data, nbo_energies):

        x = []

        # readout IDs of energies to match energies to corresponding nbo entries
        energy_ids = [x[0] for x in nbo_energies]
        for i in range(len(nbo_data)):

            # get the index of the ID of the current nbo data point
            nbo_energy_index = energy_ids.index(nbo_data[i][0])
            nbo_energy = nbo_energies[nbo_energy_index][1]

            if nbo_data[i][1] == 'LP' or nbo_data[i][1] == 'LV':

                nbo_data_point = NboSingleDataPoint(nbo_id=nbo_data[i][0],
                                                    nbo_type=nbo_data[i][1],
                                                    atom_index=nbo_data[i][2],
                                                    energy=nbo_energy,
                                                    occupation=nbo_data[i][3],
                                                    orbital_occupations=nbo_data[i][4])

            elif nbo_data[i][1] == 'BD' or nbo_data[i][1] == 'BD*':

                nbo_data_point = NboDoubleDataPoint(nbo_id=nbo_data[i][0],
                                                    nbo_type=nbo_data[i][1],
                                                    atom_indices=nbo_data[i][2],
                                                    contributions=nbo_data[i][3],
                                                    energy=nbo_energy,
                                                    occupation=nbo_data[i][4],
                                                    orbital_occupations=nbo_data[i][5])

            x.append(nbo_data_point)

        return x

    def _get_nbo_individual_lists(self):

        lone_pair_data = []
        lone_vacancy_data = []
        bond_pair_data = []
        antibond_pair_data = []

        for i in range(len(self.nbo_data)):

            if self.nbo_data[i].nbo_type == 'LP':
                lone_pair_data.append(self.nbo_data[i])

            if self.nbo_data[i].nbo_type == 'LV':
                lone_vacancy_data.append(self.nbo_data[i])

            if self.nbo_data[i].nbo_type == 'BD':
                bond_pair_data.append(self.nbo_data[i])

            if self.nbo_data[i].nbo_type == 'BD*':
                antibond_pair_data.append(self.nbo_data[i])

        self.lone_pair_data = lone_pair_data
        self.lone_vacancy_data = lone_vacancy_data
        self.bond_pair_data = bond_pair_data
        self.antibond_pair_data = antibond_pair_data

    @staticmethod
    def _calculate_euclidean_distance(x, y):

        # make sure both lists have the same length
        assert len(x) == len(y)

        # get dimension wise squared distances
        squares = [(a - b) ** 2 for a, b in zip(x, y)]

        # return sum of square root
        return sum(squares) ** 0.5
