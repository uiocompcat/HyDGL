class ElementLookUpTable():

    '''Class for looking up atomic numbers and element identifiers.'''

    elementIdentifiers = ['H','He','Li','Be','B','C','N','O','F','Ne',
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
    def getElementIdentifier(atomicNumber):
        if atomicNumber <= len(ElementLookUpTable.elementIdentifiers) and atomicNumber > 0:
            return ElementLookUpTable.elementIdentifiers[atomicNumber - 1]
        else:
            raise ValueError('Invalid atomic number, must be in range 1-118')
    
    @staticmethod
    def getAtomicNumber(elementIdentifier):
        if elementIdentifier.lower() in [x.lower() for x in ElementLookUpTable.elementIdentifiers]:
            elementIndex = [x.lower() for x in ElementLookUpTable.elementIdentifiers].index(elementIdentifier.lower())
            return elementIndex + 1
        else:
            raise ValueError('Requested element identifier does not exist')