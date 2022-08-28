Input
===

 'id': str
    The identifier of the molecule.
 'stoichiometry': str
    The stoichiometric formula of the molecule.
 'geometric_data': list[list[float]]
    A 2-dimensional list representing the xyz coordinates of the system.
 'n_atoms': int
    The number of atoms.
 'atomic_numbers': list[int]
    A list of integers corresponding to the atomic numbers of the atoms.
 'charge': float
    The overall charge of the system.
 'molecular_mass': float
    The molecular mass of the system.
 'wiberg_bond_order_matrix': list[list[float]]
     A 2-dimensional list corresponding to the Wiberg bond order matrix.
 'lmo_bond_order_matrix': list[list[float]]
    A 2-dimensional list corresponding to the LMO bond order matrix.
 'nlmo_bond_order_matrix'
    A 2-dimensional list corresponding to the NLMO bond order matrix.
 'natural_atomic_charges': list[float]
    A list of the natural atomic charges.
 'natural_electron_configuration': list[list[float]]
    A 2-dimensional list containing the natural electron configurations for each atom and orbitals s, p, d, and f.
 'natural_electron_population': list[list[float]]
    A 2-dimensional list containing the Core, Valence and Rydberg contributions to the natural population of each atom.

 'nbo_data': list[list]
    A nested list containing all information of the Natural Bond Order (NBO) analysis.
 'sopa_data':
    A nested list containing all information of the Second Order Perturbation Analysis (SOPA). For each SOPA entry there is a list containing two elements. The first element is a list of length two that holds the ids of the interacting NBO entries. The second element is a list of length three that contains the stabilisation energy, E(NL)-E(L) and F(L,NL).





 'polarisability': float
    The isotropic polarisability.
 'svp_dipole_moment': float
    The magnitude of the SVP dipole moment.
 'tzvp_dipole_moment': float
    The magnitude of the TZVP dipole moment.
 'svp_dispersion_energy': float
    The SVP dispersion energy.
 'tzvp_dispersion_energy': float
    The TZVP dispersion energy.
 'svp_electronic_energy': float
    The SVP electronic energy.
 'tzvp_electronic_energy': float
    The TZVP electronic energy.
 'enthalpy_energy': float
    The enthalpy energy.
 'gibbs_energy': float
    The Gibbs energy.
 'entropy': float
    The entropy.
 'heat_capacity': float
    The heat capacity.
 'zpe_correction': float
    The ZPE correction.
 'svp_occupied_orbital_energies'
      A list of the SVP energies of the occupied orbitals.
 'svp_virtual_orbital_energies'
      A list of the SVP energies of the virtual orbitals.
 'tzvp_occupied_orbital_energies': list[float]
     A list of the TZVP energies of the occupied orbitals.
 'tzvp_virtual_orbital_energies': list[float]
    A list of the TZVP energies of the virtual orbitals.
 'frequencies': list[float]
    A list of the vibrational frequencies.