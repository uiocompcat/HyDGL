from enum import Enum, auto

class QmAttribute(Enum):

    '''Enum class for the different QM attributes to be used.'''

    # dispersion energy
    SvpDispersionEnergy = auto()
    TzvpDispersionEnergy = auto()

    # electronic energy
    SvpElectronicEnergy = auto()
    TzvpElectronicEnergy = auto()

    # dipole moment
    SvpDipoleMoment = auto()
    TzvpDipoleMoment = auto()

    # orbitals
    SvpHomoEnergy = auto()
    SvpLumoEnergy = auto()
    TzvpHomoEnergy = auto()
    TzvpLumoEnergy = auto()

    SvpHomoLumoGap = auto()
    TzvpHomoLumoGap = auto()

    # frequencies
    LowestVibrationalFrequency = auto()
    HighestVibrationalFrequency = auto()

    # thermo chemistry
    HeatCapacity = auto()
    Entropy = auto()

    ZpeCorrection = auto()
    EnthalpyEnergy = auto()
    GibbsEnergy = auto()
    CorrectedEnthalpyEnergy = auto()
    CorrectedGibbsEnergy = auto()

    # delta values
    DispersionEnergyDelta = auto()
    ElectronicEnergyDelta = auto()
    DipoleMomentDelta = auto()
    HomoLumoGapDelta = auto()