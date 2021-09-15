from dataclasses import dataclass

@dataclass
class QmData():

    """Class for storing relevant QM data."""
    
    # basic information
    nAtoms: float = None
    atomicNumbers: list[int] = None
    naturalAtomicCharges: list[float] = None
    geometricData: list[list[float]] = None

    naturalElectronConfiguration: list[list[float]] = None

    # bond data
    wibergIndexMatrix: list[list[float]] = None
    
    # nbo data
    lonePairData = None
    loneVacancyData = None
    bondPairData = None
