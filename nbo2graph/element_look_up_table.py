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
                           'Bi', 'Po', 'At', 'Rn']

    transition_metal_atomic_numbers = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30,                          # first block
                                       39, 40, 41, 42, 43, 44, 45, 46, 47, 48,                          # second block
                                       57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71,      # lanthanides
                                       72, 73, 74, 75, 76, 77, 78, 79, 80,                              # third block
                                       89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103,  # actinides
                                       104, 105, 106, 107, 108, 109, 110, 111, 112]                     # fourth block

    # covalent radii taken from https://doi.org/10.1039%2Fb801115j
    # electronegativities (Pauling), taken from https://en.wikipedia.org/wiki/Electronegativity#Pauling_electronegativity
    atom_property_dict = {
        'H': {'covalent_radius': 0.31, 'electronegativity': 2.2},
        'He': {'covalent_radius': 0.28, 'electronegativity': '-'},
        'Li': {'covalent_radius': 1.28, 'electronegativity': 0.98},
        'Be': {'covalent_radius': 0.96, 'electronegativity': 1.57},
        'B': {'covalent_radius': 0.84, 'electronegativity': 2.04},
        'C': {'covalent_radius': 0.73, 'electronegativity': 2.55},
        'N': {'covalent_radius': 0.71, 'electronegativity': 3.04},
        'O': {'covalent_radius': 0.66, 'electronegativity': 3.44},
        'F': {'covalent_radius': 0.57, 'electronegativity': 3.98},
        'Ne': {'covalent_radius': 0.58, 'electronegativity': '-'},
        'Na': {'covalent_radius': 1.66, 'electronegativity': 0.93},
        'Mg': {'covalent_radius': 1.41, 'electronegativity': 1.31},
        'Al': {'covalent_radius': 1.21, 'electronegativity': 1.61},
        'Si': {'covalent_radius': 1.11, 'electronegativity': 1.9},
        'P': {'covalent_radius': 1.07, 'electronegativity': 2.19},
        'S': {'covalent_radius': 1.05, 'electronegativity': 2.58},
        'Cl': {'covalent_radius': 1.02, 'electronegativity': 3.16},
        'Ar': {'covalent_radius': 1.06, 'electronegativity': '-'},
        'K': {'covalent_radius': 2.03, 'electronegativity': 0.82},
        'Ca': {'covalent_radius': 1.76, 'electronegativity': 1},
        'Sc': {'covalent_radius': 1.7, 'electronegativity': 1.36},
        'Ti': {'covalent_radius': 1.6, 'electronegativity': 1.54},
        'V': {'covalent_radius': 1.53, 'electronegativity': 1.63},
        'Cr': {'covalent_radius': 1.39, 'electronegativity': 1.66},
        'Mn': {'covalent_radius': 1.5, 'electronegativity': 1.55},
        'Fe': {'covalent_radius': 1.42, 'electronegativity': 1.83},
        'Co': {'covalent_radius': 1.38, 'electronegativity': 1.88},
        'Ni': {'covalent_radius': 1.24, 'electronegativity': 1.91},
        'Cu': {'covalent_radius': 1.32, 'electronegativity': 1.9},
        'Zn': {'covalent_radius': 1.22, 'electronegativity': 1.65},
        'Ga': {'covalent_radius': 1.22, 'electronegativity': 1.81},
        'Ge': {'covalent_radius': 1.2, 'electronegativity': 2.01},
        'As': {'covalent_radius': 1.19, 'electronegativity': 2.18},
        'Se': {'covalent_radius': 1.2, 'electronegativity': 2.55},
        'Br': {'covalent_radius': 1.2, 'electronegativity': 2.96},
        'Kr': {'covalent_radius': 1.16, 'electronegativity': 3},
        'Rb': {'covalent_radius': 2.2, 'electronegativity': 0.82},
        'Sr': {'covalent_radius': 1.95, 'electronegativity': 0.95},
        'Y': {'covalent_radius': 1.9, 'electronegativity': 1.22},
        'Zr': {'covalent_radius': 1.75, 'electronegativity': 1.33},
        'Nb': {'covalent_radius': 1.64, 'electronegativity': 1.6},
        'Mo': {'covalent_radius': 1.54, 'electronegativity': 2.16},
        'Tc': {'covalent_radius': 1.47, 'electronegativity': 1.9},
        'Ru': {'covalent_radius': 1.46, 'electronegativity': 2.2},
        'Rh': {'covalent_radius': 1.42, 'electronegativity': 2.28},
        'Pd': {'covalent_radius': 1.39, 'electronegativity': 2.2},
        'Ag': {'covalent_radius': 1.45, 'electronegativity': 1.93},
        'Cd': {'covalent_radius': 1.44, 'electronegativity': 1.69},
        'In': {'covalent_radius': 1.42, 'electronegativity': 1.78},
        'Sn': {'covalent_radius': 1.39, 'electronegativity': 1.96},
        'Sb': {'covalent_radius': 1.39, 'electronegativity': 2.05},
        'Te': {'covalent_radius': 1.38, 'electronegativity': 2.1},
        'I': {'covalent_radius': 1.39, 'electronegativity': 2.66},
        'Xe': {'covalent_radius': 1.4, 'electronegativity': 2.6},
        'Cs': {'covalent_radius': 2.44, 'electronegativity': 0.79},
        'Ba': {'covalent_radius': 2.15, 'electronegativity': 0.89},
        'La': {'covalent_radius': 2.07, 'electronegativity': 1.1},
        'Ce': {'covalent_radius': 2.04, 'electronegativity': 1.12},
        'Pr': {'covalent_radius': 2.03, 'electronegativity': 1.13},
        'Nd': {'covalent_radius': 2.01, 'electronegativity': 1.14},
        'Pm': {'covalent_radius': 1.99, 'electronegativity': 1.13},
        'Sm': {'covalent_radius': 1.98, 'electronegativity': 1.17},
        'Eu': {'covalent_radius': 1.98, 'electronegativity': 1.2},
        'Gd': {'covalent_radius': 1.96, 'electronegativity': 1.2},
        'Tb': {'covalent_radius': 1.94, 'electronegativity': 1.22},
        'Dy': {'covalent_radius': 1.92, 'electronegativity': 1.23},
        'Ho': {'covalent_radius': 1.92, 'electronegativity': 1.24},
        'Er': {'covalent_radius': 1.89, 'electronegativity': 1.24},
        'Tm': {'covalent_radius': 1.9, 'electronegativity': 1.25},
        'Yb': {'covalent_radius': 1.87, 'electronegativity': 1.1},
        'Lu': {'covalent_radius': 1.87, 'electronegativity': 1.27},
        'Hf': {'covalent_radius': 1.75, 'electronegativity': 1.3},
        'Ta': {'covalent_radius': 1.7, 'electronegativity': 1.5},
        'W': {'covalent_radius': 1.62, 'electronegativity': 2.36},
        'Re': {'covalent_radius': 1.51, 'electronegativity': 1.9},
        'Os': {'covalent_radius': 1.44, 'electronegativity': 2.2},
        'Ir': {'covalent_radius': 1.41, 'electronegativity': 2.2},
        'Pt': {'covalent_radius': 1.36, 'electronegativity': 2.28},
        'Au': {'covalent_radius': 1.36, 'electronegativity': 2.54},
        'Hg': {'covalent_radius': 1.32, 'electronegativity': 2},
        'Tl': {'covalent_radius': 1.45, 'electronegativity': 1.62},
        'Pb': {'covalent_radius': 1.46, 'electronegativity': 2.33},
        'Bi': {'covalent_radius': 1.48, 'electronegativity': 2.02},
        'Po': {'covalent_radius': 1.4, 'electronegativity': 2},
        'At': {'covalent_radius': 1.5, 'electronegativity': 2.2},
        'Rn': {'covalent_radius': 1.5, 'electronegativity': '-'},
    }

    atom_format_dict = {
        'H': {'colour': 'white', 'size': 12, 'group': 1, 'period': 1},
        'He': {'colour': 'cyan', 'size': 18, 'group': 18, 'period': 1},
        'Li': {'colour': 'violet', 'size': 18, 'group': 1, 'period': 2},
        'Be': {'colour': 'green', 'size': 18, 'group': 2, 'period': 2},
        'B': {'colour': 'gray', 'size': 30, 'group': 13, 'period': 2},
        'C': {'colour': 'black', 'size': 18, 'group': 14, 'period': 2},
        'N': {'colour': 'blue', 'size': 18, 'group': 15, 'period': 2},
        'O': {'colour': 'red', 'size': 18, 'group': 16, 'period': 2},
        'F': {'colour': 'lime', 'size': 18, 'group': 17, 'period': 2},
        'Ne': {'colour': 'cyan', 'size': 18, 'group': 18, 'period': 2},
        'Na': {'colour': 'violet', 'size': 18, 'group': 1, 'period': 3},
        'Mg': {'colour': 'green', 'size': 18, 'group': 2, 'period': 3},
        'Al': {'colour': 'gray', 'size': 30, 'group': 13, 'period': 3},
        'Si': {'colour': 'gray', 'size': 30, 'group': 14, 'period': 3},
        'P': {'colour': 'orange', 'size': 18, 'group': 15, 'period': 3},
        'S': {'colour': 'yellow', 'size': 18, 'group': 16, 'period': 3},
        'Cl': {'colour': 'lime', 'size': 18, 'group': 17, 'period': 3},
        'Ar': {'colour': 'gray', 'size': 30, 'group': 18, 'period': 3},
        'K': {'colour': 'violet', 'size': 18, 'group': 1, 'period': 4},
        'Ca': {'colour': 'green', 'size': 18, 'group': 2, 'period': 4},
        'Sc': {'colour': 'gray', 'size': 30, 'group': 3, 'period': 4},
        'Ti': {'colour': 'gray', 'size': 30, 'group': 4, 'period': 4},
        'V': {'colour': 'gray', 'size': 30, 'group': 5, 'period': 4},
        'Cr': {'colour': 'gray', 'size': 30, 'group': 6, 'period': 4},
        'Mn': {'colour': 'gray', 'size': 30, 'group': 7, 'period': 4},
        'Fe': {'colour': 'gray', 'size': 30, 'group': 8, 'period': 4},
        'Co': {'colour': 'gray', 'size': 30, 'group': 9, 'period': 4},
        'Ni': {'colour': 'gray', 'size': 30, 'group': 10, 'period': 4},
        'Cu': {'colour': 'gray', 'size': 30, 'group': 11, 'period': 4},
        'Zn': {'colour': 'gray', 'size': 30, 'group': 12, 'period': 4},
        'Ga': {'colour': 'gray', 'size': 30, 'group': 13, 'period': 4},
        'Ge': {'colour': 'gray', 'size': 30, 'group': 14, 'period': 4},
        'As': {'colour': 'gray', 'size': 30, 'group': 15, 'period': 4},
        'Se': {'colour': 'gray', 'size': 30, 'group': 16, 'period': 4},
        'Br': {'colour': 'gray', 'size': 30, 'group': 17, 'period': 4},
        'Kr': {'colour': 'gray', 'size': 30, 'group': 18, 'period': 4},
        'Rb': {'colour': 'violet', 'size': 18, 'group': 1, 'period': 5},
        'Sr': {'colour': 'green', 'size': 18, 'group': 2, 'period': 5},
        'Y': {'colour': 'gray', 'size': 30, 'group': 3, 'period': 5},
        'Zr': {'colour': 'gray', 'size': 30, 'group': 4, 'period': 5},
        'Nb': {'colour': 'gray', 'size': 30, 'group': 5, 'period': 5},
        'Mo': {'colour': 'gray', 'size': 30, 'group': 6, 'period': 5},
        'Tc': {'colour': 'gray', 'size': 30, 'group': 7, 'period': 5},
        'Ru': {'colour': 'gray', 'size': 30, 'group': 8, 'period': 5},
        'Rh': {'colour': 'gray', 'size': 30, 'group': 9, 'period': 5},
        'Pd': {'colour': 'gray', 'size': 30, 'group': 10, 'period': 5},
        'Ag': {'colour': 'gray', 'size': 30, 'group': 11, 'period': 5},
        'Cd': {'colour': 'gray', 'size': 30, 'group': 12, 'period': 5},
        'In': {'colour': 'gray', 'size': 30, 'group': 13, 'period': 5},
        'Sn': {'colour': 'gray', 'size': 30, 'group': 14, 'period': 5},
        'Sb': {'colour': 'gray', 'size': 30, 'group': 15, 'period': 5},
        'Te': {'colour': 'gray', 'size': 30, 'group': 16, 'period': 5},
        'I': {'colour': 'darkviolet', 'size': 18, 'group': 17, 'period': 5},
        'Xe': {'colour': 'gray', 'size': 30, 'group': 18, 'period': 5},
        'Cs': {'colour': 'violet', 'size': 18, 'group': 1, 'period': 6},
        'Ba': {'colour': 'green', 'size': 18, 'group': 2, 'period': 6},
        'La': {'colour': 'gray', 'size': 30, 'group': 3, 'period': 6},
        'Ce': {'colour': 'gray', 'size': 30, 'group': None, 'period': 6},
        'Pr': {'colour': 'gray', 'size': 30, 'group': None, 'period': 6},
        'Nd': {'colour': 'gray', 'size': 30, 'group': None, 'period': 6},
        'Pm': {'colour': 'gray', 'size': 30, 'group': None, 'period': 6},
        'Sm': {'colour': 'gray', 'size': 30, 'group': None, 'period': 6},
        'Eu': {'colour': 'gray', 'size': 30, 'group': None, 'period': 6},
        'Gd': {'colour': 'gray', 'size': 30, 'group': None, 'period': 6},
        'Tb': {'colour': 'gray', 'size': 30, 'group': None, 'period': 6},
        'Dy': {'colour': 'gray', 'size': 30, 'group': None, 'period': 6},
        'Ho': {'colour': 'gray', 'size': 30, 'group': None, 'period': 6},
        'Er': {'colour': 'gray', 'size': 30, 'group': None, 'period': 6},
        'Tm': {'colour': 'gray', 'size': 30, 'group': None, 'period': 6},
        'Yb': {'colour': 'gray', 'size': 30, 'group': None, 'period': 6},
        'Lu': {'colour': 'gray', 'size': 30, 'group': 3, 'period': 6},
        'Hf': {'colour': 'gray', 'size': 30, 'group': 4, 'period': 6},
        'Ta': {'colour': 'gray', 'size': 30, 'group': 5, 'period': 6},
        'W': {'colour': 'gray', 'size': 30, 'group': 6, 'period': 6},
        'Re': {'colour': 'gray', 'size': 30, 'group': 7, 'period': 6},
        'Os': {'colour': 'gray', 'size': 30, 'group': 8, 'period': 6},
        'Ir': {'colour': 'gray', 'size': 30, 'group': 9, 'period': 6},
        'Pt': {'colour': 'gray', 'size': 30, 'group': 10, 'period': 6},
        'Au': {'colour': 'gray', 'size': 30, 'group': 11, 'period': 6},
        'Hg': {'colour': 'gray', 'size': 30, 'group': 12, 'period': 6},
        'Tl': {'colour': 'gray', 'size': 30, 'group': 13, 'period': 6},
        'Pb': {'colour': 'gray', 'size': 30, 'group': 14, 'period': 6},
        'Bi': {'colour': 'gray', 'size': 30, 'group': 15, 'period': 6},
        'Po': {'colour': 'gray', 'size': 30, 'group': 16, 'period': 6},
        'At': {'colour': 'gray', 'size': 30, 'group': 17, 'period': 6},
        'Rn': {'colour': 'gray', 'size': 30, 'group': 18, 'period': 6}
    }

    @staticmethod
    def get_element_format_colour(element_identifier: str) -> str:

        """Returns the appropriate formatting colour of a given element identifier.

        Args:
            element_identifier (string): The query element identifier.

        Raises:
            ValueError: If the element identifier does not exist.

        Returns:
            string: Discrete name for the colour.
        """

        if element_identifier.title() in ElementLookUpTable.atom_format_dict.keys():
            return ElementLookUpTable.atom_format_dict[element_identifier.title()]['colour']
        else:
            raise ValueError('Requested element identifier does not exist.')

    @staticmethod
    def get_element_format_size(element_identifier: str) -> int:

        """Returns the appropriate formatting size of a given element identifier.

        Args:
            element_identifier (string): The query element identifier.

        Raises:
            ValueError: If the element identifier does not exist.

        Returns:
            string: Formatting size of the element.
        """
        if element_identifier.title() in ElementLookUpTable.atom_format_dict.keys():
            return ElementLookUpTable.atom_format_dict[element_identifier.title()]['size']
        else:
            raise ValueError('Requested element identifier does not exist.')

    @staticmethod
    def get_element_identifier(atomic_number: int) -> str:

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
            raise ValueError('Invalid atomic number, must be in range 1-86.')

    @staticmethod
    def get_atomic_number(element_identifier: str) -> int:

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
