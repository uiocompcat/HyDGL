Input
====

The input required for the generation of graphs is a dictionary containing the relevant QM data in a specific format. For each molecule there needs to be a dictionary holding all of the following data:

.. glossary::

   id: str
      The identifier of the molecule.
   stoichiometry: str
      The stoichiometric formula of the molecule.
   geometric_data: list[list[float]]
      A 2-dimensional list representing the xyz coordinates of the system.
   n_atoms: int
      The number of atoms.
   atomic_numbers: list[int]
      A list of integers corresponding to the atomic numbers of the atoms.
   charge: float
      The overall charge of the system.
   molecular_mass: float
      The molecular mass of the system.
   wiberg_bond_order_matrix: list[list[float]]
      A 2-dimensional list corresponding to the Wiberg bond order matrix.
   lmo_bond_order_matrix: list[list[float]]
      A 2-dimensional list corresponding to the LMO bond order matrix.
   nlmo_bond_order_matrix
      A 2-dimensional list corresponding to the NLMO bond order matrix.
   natural_atomic_charges: list[float]
      A list of the natural atomic charges.
   natural_electron_configuration: list[list[float]]
      A 2-dimensional list containing the natural electron configurations for each atom and orbitals s, p, d, and f.
   natural_electron_population: list[list[float]]
      A 2-dimensional list containing the Core, Valence and Rydberg contributions to the natural population of each atom.

   nbo_data: list[list]
      A nested list containing all information of the Natural Bond Order (NBO) analysis. For each NBO entry there is a list containing 7 elements. These are:
      
      1. nbo_id: int
      
         The ID of the NBO entry.
      2. nbo_typ: str
      
         The type of NBO (LP, LV, BD, BD*).
      3. atom_indices: list[int]
      
         A list containing the atom indices of the atoms involved in the NBO.
      4. energy: float
      
         The energy of the NBO.
      5. contributions: list[float]
      
         A list of contributions that indicate how much each of the atoms involve contributes to the NBO. Sums to 1.
      6. occupation: float
      
         The occupation of the NBO.
      7. orbital_occupations: list[float]
      
         A list of length 4 that holds the orbital occupations in terms of the s, p, d and f symmetries.

   sopa_data:
      A nested list containing all information of the Second Order Perturbation Analysis (SOPA). For each SOPA entry there is a list containing two elements. These are:
      
      1. nbo_ids: list[int]
      
         A list of length two that holds the ids of the interacting NBO entries. 
      2. energies: list[float]
         
         A list of length three that contains the stabilisation energy, E(NL)-E(L) and F(L,NL).

   polarisability: float
      The isotropic polarisability.
   svp_dipole_moment: float
      The magnitude of the SVP dipole moment.
   tzvp_dipole_moment: float
      The magnitude of the TZVP dipole moment.
   svp_dispersion_energy: float
      The SVP dispersion energy.
   tzvp_dispersion_energy: float
      The TZVP dispersion energy.
   svp_electronic_energy: float
      The SVP electronic energy.
   tzvp_electronic_energy: float
      The TZVP electronic energy.
   enthalpy_energy: float
      The enthalpy energy.
   gibbs_energy: float
      The Gibbs energy.
   entropy: float
      The entropy.
   heat_capacity: float
      The heat capacity.
   zpe_correction: float
      The ZPE correction.
   svp_occupied_orbital_energies
      A list of the SVP energies of the occupied orbitals.
   svp_virtual_orbital_energies
      A list of the SVP energies of the virtual orbitals.
   tzvp_occupied_orbital_energies: list[float]
      A list of the TZVP energies of the occupied orbitals.
   tzvp_virtual_orbital_energies: list[float]
      A list of the TZVP energies of the virtual orbitals.
   frequencies: list[float]
      A list of the vibrational frequencies.


For the tmQMg the dictionaries formatted as ``JSON`` files can be found `here <>`_. If you want to use your own data you have to setup the QM calculations and subsequent data extraction yourself.
