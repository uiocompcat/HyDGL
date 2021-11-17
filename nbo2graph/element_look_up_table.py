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
                                       39, 40, 41, 42, 43, 44, 45, 46, 47, 48,                          # second block
                                       57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71,      # lanthanides
                                       72, 73, 74, 75, 76, 77, 78, 79, 80,                              # third block
                                       89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103,  # actinides
                                       104, 105, 106, 107, 108, 109, 110, 111, 112]                     # fourth block

    atom_format_dict = {
        'H': {'colour': 'white', 'size': 12},
        'He': {'colour': 'cyan', 'size': 18},
        'Li': {'colour': 'violet', 'size': 18},
        'Be': {'colour': 'green', 'size': 18},
        'B': {'colour': 'gray', 'size': 30},
        'C': {'colour': 'black', 'size': 18},
        'N': {'colour': 'blue', 'size': 18},
        'O': {'colour': 'red', 'size': 18},
        'F': {'colour': 'lime', 'size': 18},
        'Ne': {'colour': 'cyan', 'size': 18},
        'Na': {'colour': 'violet', 'size': 18},
        'Mg': {'colour': 'green', 'size': 18},
        'Al': {'colour': 'gray', 'size': 30},
        'Si': {'colour': 'gray', 'size': 30},
        'P': {'colour': 'orange', 'size': 18},
        'S': {'colour': 'yellow', 'size': 18},
        'Cl': {'colour': 'lime', 'size': 18},
        'Ar': {'colour': 'gray', 'size': 30},
        'K': {'colour': 'violet', 'size': 18},
        'Ca': {'colour': 'green', 'size': 18},
        'Sc': {'colour': 'gray', 'size': 30},
        'Ti': {'colour': 'gray', 'size': 30},
        'V': {'colour': 'gray', 'size': 30},
        'Cr': {'colour': 'gray', 'size': 30},
        'Mn': {'colour': 'gray', 'size': 30},
        'Fe': {'colour': 'gray', 'size': 30},
        'Co': {'colour': 'gray', 'size': 30},
        'Ni': {'colour': 'gray', 'size': 30},
        'Cu': {'colour': 'gray', 'size': 30},
        'Zn': {'colour': 'gray', 'size': 30},
        'Ga': {'colour': 'gray', 'size': 30},
        'Ge': {'colour': 'gray', 'size': 30},
        'As': {'colour': 'gray', 'size': 30},
        'Se': {'colour': 'gray', 'size': 30},
        'Br': {'colour': 'gray', 'size': 30},
        'Kr': {'colour': 'gray', 'size': 30},
        'Rb': {'colour': 'violet', 'size': 18},
        'Sr': {'colour': 'green', 'size': 18},
        'Y': {'colour': 'gray', 'size': 30},
        'Zr': {'colour': 'gray', 'size': 30},
        'Nb': {'colour': 'gray', 'size': 30},
        'Mo': {'colour': 'gray', 'size': 30},
        'Tc': {'colour': 'gray', 'size': 30},
        'Ru': {'colour': 'gray', 'size': 30},
        'Rh': {'colour': 'gray', 'size': 30},
        'Pd': {'colour': 'gray', 'size': 30},
        'Ag': {'colour': 'gray', 'size': 30},
        'Cd': {'colour': 'gray', 'size': 30},
        'In': {'colour': 'gray', 'size': 30},
        'Sn': {'colour': 'gray', 'size': 30},
        'Sb': {'colour': 'gray', 'size': 30},
        'Te': {'colour': 'gray', 'size': 30},
        'I': {'colour': 'darkviolet', 'size': 18},
        'Xe': {'colour': 'gray', 'size': 30},
        'Cs': {'colour': 'violet', 'size': 18},
        'Ba': {'colour': 'green', 'size': 18},
        'La': {'colour': 'gray', 'size': 30},
        'Ce': {'colour': 'gray', 'size': 30},
        'Pr': {'colour': 'gray', 'size': 30},
        'Nd': {'colour': 'gray', 'size': 30},
        'Pm': {'colour': 'gray', 'size': 30},
        'Sm': {'colour': 'gray', 'size': 30},
        'Eu': {'colour': 'gray', 'size': 30},
        'Gd': {'colour': 'gray', 'size': 30},
        'Tb': {'colour': 'gray', 'size': 30},
        'Dy': {'colour': 'gray', 'size': 30},
        'Ho': {'colour': 'gray', 'size': 30},
        'Er': {'colour': 'gray', 'size': 30},
        'Tm': {'colour': 'gray', 'size': 30},
        'Yb': {'colour': 'gray', 'size': 30},
        'Lu': {'colour': 'gray', 'size': 30},
        'Hf': {'colour': 'gray', 'size': 30},
        'Ta': {'colour': 'gray', 'size': 30},
        'W': {'colour': 'gray', 'size': 30},
        'Re': {'colour': 'gray', 'size': 30},
        'Os': {'colour': 'gray', 'size': 30},
        'Ir': {'colour': 'gray', 'size': 30},
        'Pt': {'colour': 'gray', 'size': 30},
        'Au': {'colour': 'gray', 'size': 30},
        'Hg': {'colour': 'gray', 'size': 30},
        'Tl': {'colour': 'gray', 'size': 30},
        'Pb': {'colour': 'gray', 'size': 30},
        'Bi': {'colour': 'gray', 'size': 30},
        'Po': {'colour': 'gray', 'size': 30},
        'At': {'colour': 'gray', 'size': 30},
        'Rn': {'colour': 'gray', 'size': 30},
        'Fr': {'colour': 'violet', 'size': 18},
        'Ra': {'colour': 'green', 'size': 18},
        'Ac': {'colour': 'gray', 'size': 30},
        'Th': {'colour': 'gray', 'size': 30},
        'Pa': {'colour': 'gray', 'size': 30},
        'U': {'colour': 'gray', 'size': 30},
        'Np': {'colour': 'gray', 'size': 30},
        'Pu': {'colour': 'gray', 'size': 30},
        'Am': {'colour': 'gray', 'size': 30},
        'Cm': {'colour': 'gray', 'size': 30},
        'Bk': {'colour': 'gray', 'size': 30},
        'Cf': {'colour': 'gray', 'size': 30},
        'Es': {'colour': 'gray', 'size': 30},
        'Fm': {'colour': 'gray', 'size': 30},
        'Md': {'colour': 'gray', 'size': 30},
        'No': {'colour': 'gray', 'size': 30},
        'Lr': {'colour': 'gray', 'size': 30},
        'Rf': {'colour': 'gray', 'size': 30},
        'Db': {'colour': 'gray', 'size': 30},
        'Sg': {'colour': 'gray', 'size': 30},
        'Bh': {'colour': 'gray', 'size': 30},
        'Hs': {'colour': 'gray', 'size': 30},
        'Mt': {'colour': 'gray', 'size': 30},
        'Ds': {'colour': 'gray', 'size': 30},
        'Rg': {'colour': 'gray', 'size': 30},
        'Uub': {'colour': 'gray', 'size': 30},
        'Uuq': {'colour': 'gray', 'size': 30}
    }

    @staticmethod
    def get_element_format_colour(element_identifier):

        """Returns the appropriate formatting colour of a given element identifier.

        Args:
            element_identifier (string): The query element identifier.

        Raises:
            ValueError: If the element identifier does not exist.

        Returns:
            string: Discrete name for the colour.
        """

        if element_identifier in ElementLookUpTable.atom_format_dict.keys():
            return ElementLookUpTable.atom_format_dict[element_identifier]['colour']
        else:
            raise ValueError('Requested element identifier does not exist.')

    @staticmethod
    def get_element_format_size(element_identifier):

        """Returns the appropriate formatting size of a given element identifier.

        Args:
            element_identifier (string): The query element identifier.

        Raises:
            ValueError: If the element identifier does not exist.

        Returns:
            string: Formatting size of the element.
        """
        if element_identifier in ElementLookUpTable.atom_format_dict.keys():
            return ElementLookUpTable.atom_format_dict[element_identifier]['size']
        else:
            raise ValueError('Requested element identifier does not exist.')

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
