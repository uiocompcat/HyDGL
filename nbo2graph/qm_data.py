from nbo2graph.nbo_data_point import NboDataPoint
from nbo2graph.tools import Tools
from nbo2graph.enums.nbo_type import NboType


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
                 nbo_data: list[list],
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

        self.bond_distance_matrix = Tools.calculate_distance_matrix(geometric_data)

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
        self.enthalpy_energy_correction = self.enthalpy_energy - self.svp_electronic_energy
        # calculate ZPE, thermal, internal, and entropy energy corrections
        self.gibbs_energy_correction = self.gibbs_energy - self.svp_electronic_energy

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

        # NBO data
        self.nbo_data = [NboDataPoint.from_list(nbo_data_point) for nbo_data_point in nbo_data]
        # data for NBO SOPA
        self.sopa_data = sopa_data

        # get individual lists for LP, LV, BD, BD*
        self._set_nbo_individual_lists()

    @classmethod
    def from_dict(cls, qm_data_dict: dict):

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
                   sopa_data=qm_data_dict['sopa_data'])

    @property
    def lowest_vibrational_frequency(self):
        """Getter for the lowest vibrational frequeny."""
        return self.frequencies[0]

    @property
    def highest_vibrational_frequency(self):
        """Getter for the highest vibrational frequency."""
        return self.frequencies[-1]

    @property
    def svp_homo_energy(self):
        """Getter for the SVP HOMO energe."""
        return self.svp_occupied_orbital_energies[-1]

    @property
    def svp_lumo_energy(self):
        """Getter for the SVP LUMO energy."""
        return self.svp_virtual_orbital_energies[0]

    @property
    def tzvp_homo_energy(self):
        """Getter for the TZVP HOMO energy."""
        return self.tzvp_occupied_orbital_energies[-1]

    @property
    def tzvp_lumo_energy(self):
        """Getter for the TZVP LUMO energy."""
        return self.tzvp_virtual_orbital_energies[0]

    @property
    def svp_homo_lumo_gap(self):
        """Getter for the SVP HOMO-LUMO gap."""
        return self.svp_lumo_energy - self.svp_homo_energy

    @property
    def tzvp_homo_lumo_gap(self):
        """Getter for the TZVP HOMO-LUMO gap."""
        return self.tzvp_lumo_energy - self.tzvp_homo_energy

    @property
    def wiberg_bond_order_totals(self):
        """Getter for the Wiberg bond order totals."""
        return [sum(bond_orders) for bond_orders in self.wiberg_bond_order_matrix]

    @property
    def lmo_bond_order_totals(self):
        """Getter for the LMO bond order totals."""
        return [sum(bond_orders) for bond_orders in self.lmo_bond_order_matrix]

    @property
    def nlmo_bond_order_totals(self):
        """Getter for the NLMO bond order totals."""
        return [sum(bond_orders) for bond_orders in self.nlmo_bond_order_matrix]

    @property
    def dispersion_energy_delta(self):
        """Getter for the dispersion energy SVP-TZVP delta."""
        return abs(self.svp_dispersion_energy - self.tzvp_dispersion_energy)

    @property
    def electronic_energy_delta(self):
        """Getter for the electronic energy SVP-TZVP delta."""
        return abs(self.svp_electronic_energy - self.tzvp_electronic_energy)

    @property
    def dipole_moment_delta(self):
        """Getter for the dipole moment SVP-TZVP delta."""
        return abs(self.svp_dipole_moment - self.tzvp_dipole_moment)

    @property
    def homo_lumo_gap_delta(self):
        """Getter for the HOMO-LUMO SVP-TZVP delta."""
        return abs(self.svp_homo_lumo_gap - self.tzvp_homo_lumo_gap)

    def _set_nbo_individual_lists(self):

        """Generates individual lists for all the different NBO types and adds them as members."""

        lone_pair_data = []
        lone_vacancy_data = []
        bond_pair_data = []
        antibond_pair_data = []

        bond_3c_data = []
        antibond_3c_data = []
        nonbond_3c_data = []

        for i in range(len(self.nbo_data)):

            if self.nbo_data[i].nbo_type == 'LP':
                lone_pair_data.append(self.nbo_data[i])

            elif self.nbo_data[i].nbo_type == 'LV':
                lone_vacancy_data.append(self.nbo_data[i])

            elif self.nbo_data[i].nbo_type == 'BD':
                bond_pair_data.append(self.nbo_data[i])

            elif self.nbo_data[i].nbo_type == 'BD*':
                antibond_pair_data.append(self.nbo_data[i])

            elif self.nbo_data[i].nbo_type == '3C':
                bond_3c_data.append(self.nbo_data[i])

            elif self.nbo_data[i].nbo_type == '3C*':
                antibond_3c_data.append(self.nbo_data[i])

            elif self.nbo_data[i].nbo_type == '3Cn':
                nonbond_3c_data.append(self.nbo_data[i])

        self.lone_pair_data = lone_pair_data
        self.lone_vacancy_data = lone_vacancy_data
        self.bond_pair_data = bond_pair_data
        self.antibond_pair_data = antibond_pair_data
        self.bond_3c_data = bond_3c_data
        self.antibond_3c_data = antibond_3c_data
        self.nonbond_3c_data = nonbond_3c_data

    def get_nbo_data_by_type(self, nbo_type: NboType):

        if nbo_type == NboType.LONE_PAIR:
            return self.lone_pair_data
        elif nbo_type == NboType.LONE_VACANCY:
            return self.lone_vacancy_data
        elif nbo_type == NboType.BOND:
            return self.bond_pair_data
        elif nbo_type == NboType.ANTIBOND:
            return self.antibond_pair_data
        elif nbo_type == NboType.THREE_CENTER_BOND:
            return self.bond_3c_data
        elif nbo_type == NboType.THREE_CENTER_ANTIBOND:
            return self.antibond_3c_data
        elif nbo_type == NboType.THREE_CENTER_NONBOND:
            return self.nonbond_3c_data
        else:
            raise ValueError('NboType ' + str(nbo_type) + ' not recognized.')
