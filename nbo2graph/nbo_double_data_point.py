from nbo2graph.nbo_data_point import NboDataPoint


class NboDoubleDataPoint(NboDataPoint):

    """Class for storing double NBO data entries."""

    def __init__(self, nbo_id, nbo_type, atom_indeces, contributions, energy, occupation, orbital_occupations):

        """Constructor"""

        super().__init__(nbo_id, nbo_type, energy, occupation, orbital_occupations)

        self._atom_indeces = atom_indeces
        self._contributions = contributions

    @property
    def atom_indeces(self):
        """Getter for atom_indeces"""
        return self._atom_indeces

    @property
    def contributions(self):
        """Getter for contributions"""
        return self._contributions
