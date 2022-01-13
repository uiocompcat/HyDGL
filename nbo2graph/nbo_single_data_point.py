from nbo2graph.nbo_data_point import NboDataPoint


class NboSingleDataPoint(NboDataPoint):

    """Class for storing single NBO data entries  (i.e. LP, LV)."""

    def __init__(self, nbo_id, nbo_type, atom_index, energy, occupation, orbital_occupations):

        """Constructor"""

        super().__init__(nbo_id, nbo_type, energy, occupation, orbital_occupations)

        self._atom_index = atom_index

    @property
    def atom_index(self):
        """Getter for atom_index"""
        return self._atom_index
