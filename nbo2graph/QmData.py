from dataclasses import dataclass

@dataclass
class QmData():

    """Class for storing relevant QM data."""
    
    nAtoms: float = None
    atomicNumbers: list[int] = None
    naturalAtomicCharges: list[float] = None
    wibergIndexMatrix: list[list[float]] = None
    geometricData: list[list[float]] = None
    naturalElectronConfiguration: list[list[float]] = None
