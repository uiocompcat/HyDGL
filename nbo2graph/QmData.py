from dataclasses import dataclass

@dataclass
class QmData():

    """Class for storing relevant QM data."""

    # attributes
    csdIdentifier: str = None
    stoichiometry: str = None

    # basic information
    nAtoms: float = None
    atomicNumbers: list[int] = None
    geometricData: list[list[float]] = None

    charge: int = None # e
    molecularMass: float = None # amu
    polarisability: float = None # Bohr ^ 3

    # energies
    svpDispersionEnergy: float = None # Ha
    tzvpDispersionEnergy: float = None # Ha

    svpElectronicEnergy: float = None # Ha
    tzvpElectronicEnergy: float = None # Ha

    svpDipoleMoment: float = None # D
    tzvpDipoleMoment: float = None # D

    # orbital data
    svpOccupiedOrbitalEnergies: list[float] = None
    tzvpOccupiedOrbitalEnergies: list[float] = None
    svpVirtualOrbitalEnergies: list[float] = None
    tzvpVirtualOrbitalEnergies: list[float] = None

    svpHomoEnergy: float = None # Ha
    svpLumoEnergy: float = None # Ha
    tzvpHomoEnergy: float = None # Ha
    tzvpLumoEnergy: float = None # Ha

    svpHomoLumoGap: float = None # Ha
    tzvpHomoLumoGap: float = None # Ha

    # vibrational frequencies
    frequencies: list[float] = None # cm ^ -1
    lowestVibrationalFrequency: float = None # cm ^ -1
    highestVibrationalFrequency: float = None # cm ^ -1

    # thermo chemistry
    heatCapacity: float = None # Cal/Mol-Kelvin
    entropy: float = None # Cal/Mol-Kelvin

    zpeCorrection: float = None # Ha
    enthalpyEnergy: float = None # Ha
    gibbsEnergy: float = None # Ha
    correctedEnthalpyEnergy: float = None # Ha
    correctedGibbsEnergy: float = None # Ha

    # electronic data
    naturalAtomicCharges: list[float] = None
    naturalElectronConfiguration: list[list[float]] = None

    # bond data
    wibergIndexMatrix: list[list[float]] = None
    
    # nbo data
    lonePairData = None
    loneVacancyData = None
    bondPairData = None

    # deltas
    dispersionEnergyDelta: float = None # Ha
    electronicEnergyDelta: float = None # Ha
    dipoleMomentDelta: float = None # D
    homoLumoGapDelta: float = None # Ha

    def calculateProperties(self):

        """Calculates composite properties such as HOMO-LUMO gap and delta values/corrections between SVP and TZVP."""

        # physical properties

        # calculate homo lumo svp
        self.svpHomoEnergy = self.svpOccupiedOrbitalEnergies[-1]
        self.svpLumoEnergy = self.svpVirtualOrbitalEnergies[0]

        # calculate homo lumo tzvp
        self.tzvpHomoEnergy = self.tzvpOccupiedOrbitalEnergies[-1]
        self.tzvpLumoEnergy = self.tzvpVirtualOrbitalEnergies[0]

        # calculate homo lumo gaps
        self.svpHomoLumoGap = self.svpLumoEnergy - self.svpHomoEnergy
        self.tzvpHomoLumoGap = self.tzvpLumoEnergy - self.tzvpHomoEnergy

        # get lowest and highest vibrational frequencies
        self.lowestVibrationalFrequency = self.frequencies[0]
        self.highestVibrationalFrequency = self.frequencies[-1]

        # calculate ZPE, thermal, and internal energy corrections
        self.correctedEnthalpyEnergy = self.enthalpyEnergy - self.svpElectronicEnergy

        # calculate ZPE, thermal, internal, and entropy energy corrections
        self.correctedGibbsEnergy =  self.gibbsEnergy - self.svpElectronicEnergy

        # SVP - TZVP deltas

        # calculate svp - tzvp dispersion energy delta
        self.dispersionEnergyDelta = self.svpDispersionEnergy - self.tzvpDispersionEnergy
        
        # calculate svp - tzvp electronic energy delta
        self.electronicEnergyDelta = self.svpElectronicEnergy - self.tzvpElectronicEnergy
       
        # calculate svp - tzvp dipole moment delta
        self.dipoleMomentDelta = self.svpDipoleMoment - self.tzvpDipoleMoment

        # calculate svp - tzvp homo lumo gap delta
        self.homoLumoGapDelta = self.svpHomoLumoGap - self.tzvpHomoLumoGap