class ElementLookUpTable():

    '''Class for looking up atomic numbers and element identifiers.'''

    element_identifiers = ['H','He','Li','Be','B','C','N','O','F','Ne',
                          'Na','Mg','Al','Si','P','S','Cl','Ar','K',
                          'Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni',
                          'Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb',
                          'Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd',
                          'Ag','Cd','In','Sn','Sb','Te','I','Xe','Cs',
                          'Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd',
                          'Tb','Dy','Ho','Er','Tm','Yb','Lu','Hf','Ta',
                          'W','Re','Os','Ir','Pt','Au','Hg','Tl','Pb',
                          'Bi','Po','At','Rn','Fr','Ra','Ac','Th','Pa',
                          'U','Np','Pu','Am','Cm','Bk','Cf','Es','Fm',
                          'Md','No','Lr','Rf','Db','Sg','Bh','Hs','Mt',
                          'Ds','Rg','Cn','Nh','Fl','Mc','Lv','Ts','Og']

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