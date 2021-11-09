class ElementLookUpTable():

    '''Class for looking up atomic numbers and element identifiers.'''

    element_identifiers = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
                           'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K',
                           'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni',
                           'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb',
                           'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd',
                           'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs',
                           'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd',
                           'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta',
                           'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb',
                           'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa',
                           'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm',
                           'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt',
                           'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']

    transition_metal_atomic_numbers = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30,                          # first block
                                       39, 49, 41, 42, 43, 44, 45, 46, 47, 48,                          # second block
                                       57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71,      # lanthanides
                                       72, 73, 74, 75, 76, 77, 78, 79, 80,                              # third block
                                       89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103,  # actinides
                                       104, 105, 106, 107, 108, 109, 110, 111, 112]                     # fourth block

    atom_format_dict = {
        'H': {'color': 'white', 'size': 12},
        'He': {'color': 'cyan', 'size': 18},
        'Li': {'color': 'violet', 'size': 18},
        'Be': {'color': 'green', 'size': 18},
        'B': {'color': 'gray', 'size': 30},
        'C': {'color': 'black', 'size': 18},
        'N': {'color': 'blue', 'size': 18},
        'O': {'color': 'red', 'size': 18},
        'F': {'color': 'lime', 'size': 18},
        'Ne': {'color': 'cyan', 'size': 18},
        'Na': {'color': 'violet', 'size': 18},
        'Mg': {'color': 'green', 'size': 18},
        'Al': {'color': 'gray', 'size': 30},
        'Si': {'color': 'gray', 'size': 30},
        'P': {'color': 'orange', 'size': 18},
        'S': {'color': 'yellow', 'size': 18},
        'Cl': {'color': 'lime', 'size': 18},
        'Ar': {'color': 'gray', 'size': 30},
        'K': {'color': 'violet', 'size': 18},
        'Ca': {'color': 'green', 'size': 18},
        'Sc': {'color': 'gray', 'size': 30},
        'Ti': {'color': 'gray', 'size': 30},
        'V': {'color': 'gray', 'size': 30},
        'Cr': {'color': 'gray', 'size': 30},
        'Mn': {'color': 'gray', 'size': 30},
        'Fe': {'color': 'gray', 'size': 30},
        'Co': {'color': 'gray', 'size': 30},
        'Ni': {'color': 'gray', 'size': 30},
        'Cu': {'color': 'gray', 'size': 30},
        'Zn': {'color': 'gray', 'size': 30},
        'Ga': {'color': 'gray', 'size': 30},
        'Ge': {'color': 'gray', 'size': 30},
        'As': {'color': 'gray', 'size': 30},
        'Se': {'color': 'gray', 'size': 30},
        'Br': {'color': 'gray', 'size': 30},
        'Kr': {'color': 'gray', 'size': 30},
        'Rb': {'color': 'violet', 'size': 18},
        'Sr': {'color': 'green', 'size': 18},
        'Y': {'color': 'gray', 'size': 30},
        'Zr': {'color': 'gray', 'size': 30},
        'Nb': {'color': 'gray', 'size': 30},
        'Mo': {'color': 'gray', 'size': 30},
        'Tc': {'color': 'gray', 'size': 30},
        'Ru': {'color': 'gray', 'size': 30},
        'Rh': {'color': 'gray', 'size': 30},
        'Pd': {'color': 'gray', 'size': 30},
        'Ag': {'color': 'gray', 'size': 30},
        'Cd': {'color': 'gray', 'size': 30},
        'In': {'color': 'gray', 'size': 30},
        'Sn': {'color': 'gray', 'size': 30},
        'Sb': {'color': 'gray', 'size': 30},
        'Te': {'color': 'gray', 'size': 30},
        'I': {'color': 'darkviolet', 'size': 18},
        'Xe': {'color': 'gray', 'size': 30},
        'Cs': {'color': 'violet', 'size': 18},
        'Ba': {'color': 'green', 'size': 18},
        'La': {'color': 'gray', 'size': 30},
        'Ce': {'color': 'gray', 'size': 30},
        'Pr': {'color': 'gray', 'size': 30},
        'Nd': {'color': 'gray', 'size': 30},
        'Pm': {'color': 'gray', 'size': 30},
        'Sm': {'color': 'gray', 'size': 30},
        'Eu': {'color': 'gray', 'size': 30},
        'Gd': {'color': 'gray', 'size': 30},
        'Tb': {'color': 'gray', 'size': 30},
        'Dy': {'color': 'gray', 'size': 30},
        'Ho': {'color': 'gray', 'size': 30},
        'Er': {'color': 'gray', 'size': 30},
        'Tm': {'color': 'gray', 'size': 30},
        'Yb': {'color': 'gray', 'size': 30},
        'Lu': {'color': 'gray', 'size': 30},
        'Hf': {'color': 'gray', 'size': 30},
        'Ta': {'color': 'gray', 'size': 30},
        'W': {'color': 'gray', 'size': 30},
        'Re': {'color': 'gray', 'size': 30},
        'Os': {'color': 'gray', 'size': 30},
        'Ir': {'color': 'gray', 'size': 30},
        'Pt': {'color': 'gray', 'size': 30},
        'Au': {'color': 'gray', 'size': 30},
        'Hg': {'color': 'gray', 'size': 30},
        'Tl': {'color': 'gray', 'size': 30},
        'Pb': {'color': 'gray', 'size': 30},
        'Bi': {'color': 'gray', 'size': 30},
        'Po': {'color': 'gray', 'size': 30},
        'At': {'color': 'gray', 'size': 30},
        'Rn': {'color': 'gray', 'size': 30},
        'Fr': {'color': 'violet', 'size': 18},
        'Ra': {'color': 'green', 'size': 18},
        'Ac': {'color': 'gray', 'size': 30},
        'Th': {'color': 'gray', 'size': 30},
        'Pa': {'color': 'gray', 'size': 30},
        'U': {'color': 'gray', 'size': 30},
        'Np': {'color': 'gray', 'size': 30},
        'Pu': {'color': 'gray', 'size': 30},
        'Am': {'color': 'gray', 'size': 30},
        'Cm': {'color': 'gray', 'size': 30},
        'Bk': {'color': 'gray', 'size': 30},
        'Cf': {'color': 'gray', 'size': 30},
        'Es': {'color': 'gray', 'size': 30},
        'Fm': {'color': 'gray', 'size': 30},
        'Md': {'color': 'gray', 'size': 30},
        'No': {'color': 'gray', 'size': 30},
        'Lr': {'color': 'gray', 'size': 30},
        'Rf': {'color': 'gray', 'size': 30},
        'Db': {'color': 'gray', 'size': 30},
        'Sg': {'color': 'gray', 'size': 30},
        'Bh': {'color': 'gray', 'size': 30},
        'Hs': {'color': 'gray', 'size': 30},
        'Mt': {'color': 'gray', 'size': 30},
        'Ds': {'color': 'gray', 'size': 30},
        'Rg': {'color': 'gray', 'size': 30},
        'Uub': {'color': 'gray', 'size': 30},
        'Uuq': {'color': 'gray', 'size': 30}
    }

    @staticmethod
    def get_element_identifier(atomic_number):

        """Returns the appropriate element identifier based on a given atomic number.

        Args:
            atomic_number (int): The query atomic number.

        Raises:
            ValueError: If the atomic number does not exist.

        Returns:
            string: The element identifier.
        """

        if atomic_number <= len(ElementLookUpTable.element_identifiers) and atomic_number > 0:
            return ElementLookUpTable.element_identifiers[atomic_number - 1]
        else:
            raise ValueError('Invalid atomic number, must be in range 1-118.')

    @staticmethod
    def get_atomic_number(element_identifier):

        """Returns the appropriate atomic number based on a given element identifier.

        Args:
            element_identifier (string): The query element identifier.

        Raises:
            ValueError: If the element identifier does not exist.

        Returns:
            int: The atomic number.
        """

        if element_identifier.lower() in [x.lower() for x in ElementLookUpTable.element_identifiers]:
            element_index = [x.lower() for x in ElementLookUpTable.element_identifiers].index(element_identifier.lower())
            return element_index + 1
        else:
            raise ValueError('Requested element identifier does not exist.')
