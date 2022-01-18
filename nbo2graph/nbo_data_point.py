class NboDataPoint:

    """Abstract class as template for NBO single and double data classes."""

    def __init__(self, nbo_id, nbo_type, atom_indices, energy, occupation, orbital_occupations, contributions):

        """Constructor"""

        self._nbo_id = nbo_id
        self._nbo_type = nbo_type
        self._atom_indices = atom_indices
        self._energy = energy
        self._occupation = occupation
        self._orbital_occupations = orbital_occupations
        self._contributions = contributions

    @property
    def atom_indices(self):
        """Getter for atom_indices"""
        return self._atom_indices

    @property
    def contributions(self):
        """Getter for contributions"""
        return self._contributions

    @property
    def nbo_id(self):
        """Getter for nbo_id"""
        return self._nbo_id

    @property
    def nbo_type(self):
        """Getter for nbo_type"""
        return self._nbo_type

    @property
    def energy(self):
        """Getter for energy"""
        return self._energy

    @property
    def occupation(self):
        """Getter for occupation"""
        return self._occupation

    @property
    def orbital_occupations(self):
        """Getter for orbital_occupations"""
        return self._orbital_occupations
