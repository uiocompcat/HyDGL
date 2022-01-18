class NboDataPoint:

    """Abstract class as template for NBO single and double data classes."""

    def __init__(self, nbo_id, nbo_type, atom_indices, energy, occupation, orbital_occupations, contributions):

        """Constructor"""

        # check for equal length of involved atoms and contributions
        assert len(atom_indices) == len(contributions)
        # check that orbital occupations for s, p, d, f are available
        assert len(orbital_occupations) == 4

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

    def contains_atom_indices(self, indices: list[int]) -> bool:

        """Helper function to determine whether given atom indices are contained in this NBO.

        Returns:
            bool: The result.
        """

        for i in range(len(self.atom_indices) - 1):
            if self.atom_indices[i:i + 2] == indices:
                return True
        return False
