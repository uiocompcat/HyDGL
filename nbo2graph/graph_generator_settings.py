from nbo2graph.file_handler import FileHandler
from nbo2graph.qm_atrribute import QmAttribute
from nbo2graph.node_feature import NodeFeature
from nbo2graph.edge_feature import EdgeFeature
from nbo2graph.graph_feature import GraphFeature
from nbo2graph.hydrogen_mode import HydrogenMode
from nbo2graph.bond_determination_mode import BondDeterminationMode
from nbo2graph.orbital_occupation_types import OrbitalOccupationTypes

# constants
DEFAULT_BOND_DETERMINATION_MODE = BondDeterminationMode.WIBERG
DEFAULT_HYDROGEN_MODE = HydrogenMode.EXPLICIT
DEFAULT_BOND_THRESHOLD = 0.3
DEFAULT_HYDROGEN_COUNT_THRESHOLD = 0.5


class GraphGeneratorSettings:

    """Class for storing graph generator settings."""

    def __init__(self,
                 node_features: list[NodeFeature] = [],
                 edge_features: list[EdgeFeature] = [],
                 graph_features: list[GraphFeature] = [],
                 attributes: list[QmAttribute] = [],
                 bond_determination_mode: BondDeterminationMode = DEFAULT_BOND_DETERMINATION_MODE,
                 bond_threshold=DEFAULT_BOND_THRESHOLD,
                 hydrogen_mode=DEFAULT_HYDROGEN_MODE,
                 hydrogen_count_threshold=DEFAULT_HYDROGEN_COUNT_THRESHOLD):

        """Constructor

        Args:
            node_features (list[NodeFeature]): List of node features to extract.
            edge_features (list[EdgeFeature]): List of edge features to extract.
            bond_determination_mode (BondDeterminationMode): Specifies the way bonds are determined when building the graph.
            attributes_to_extract (list[QmAttribute]): List of attributes defining which QM properties should be extracted as attributes.
            bond_threshold (float): Threshold value defining the lower bound for considering bonds.
            hydrogen_count_threshold(float): Threshold value defining the lower bound for considering hydrogens as bound for implicit mode.
            hydrogen_mode (HydrogenMode): Operation mode defining the way to handle hydrogens.
        """

        # features
        self.node_features = node_features
        self.edge_features = edge_features
        self.graph_features = graph_features

        # attributes
        self.attributes = attributes

        # bond mode
        self.bond_determination_mode = bond_determination_mode
        self.bond_threshold = bond_threshold

        # hydrogen mode
        self.hydrogen_mode = hydrogen_mode
        self.hydrogen_count_threshold = hydrogen_count_threshold

        # get orbital lists specifying which orbitals to consider
        # 0 -> s, 1 -> p, 2 -> d, 3 -> f
        self.lone_pair_orbital_indices = self._get_orbtials_to_extract_indices(OrbitalOccupationTypes.LONE_PAIR)
        self.lone_vacancy_orbital_indices = self._get_orbtials_to_extract_indices(OrbitalOccupationTypes.LONE_VACANCY)
        self.natural_orbital_configuration_indices = self._get_orbtials_to_extract_indices(OrbitalOccupationTypes.NATURAL_ELECTRON_CONFIGURATION)
        self.bond_orbital_indices = self._get_orbtials_to_extract_indices(OrbitalOccupationTypes.BOND_ORBITAL)
        self.antibond_orbital_indices = self._get_orbtials_to_extract_indices(OrbitalOccupationTypes.ANTIBOND_ORBITAL)

    @classmethod
    def default(cls):
        return cls()

    @classmethod
    def from_file(cls, file_path: str):

        "Initialize MyData from a file"

        data = FileHandler.read_file(file_path)
        lines = data.split('\n')

        # set up a dictionary for all sepified settings
        settings_dict = {}
        for i in range(len(lines)):

            # skip empty lines
            if lines[i].replace(' ', '') == '':
                continue
            # skip comment lines
            elif lines[i][0] == '#':
                continue
            # skip headers
            elif lines[i][0] == '[':
                continue

            line_split = lines[i].split(':')

            if len(line_split) == 2:

                # check for orbital settings
                if line_split[0].strip().upper() == 'LONE_PAIRS' or \
                   line_split[0].strip().upper() == 'LONE_VACANCIES' or \
                   line_split[0].strip().upper() == 'BOND_ORBITAL_DATA' or \
                   line_split[0].strip().upper() == 'ANTIBOND_ORBITAL_DATA' or \
                   line_split[0].strip().upper() == 'NATURAL_ELECTRON_CONFIGURATION':

                    # read requested orbitals
                    orbitals = line_split[1].strip().lower().split(' ')

                    # orbital types to consider
                    orbital_types = ['s', 'p', 'd', 'f']

                    # convert to bool representations
                    for orbital_type in orbital_types:

                        if orbital_type in orbitals:
                            settings_dict[line_split[0].strip().upper() + '_' + orbital_type.upper()] = 'true'
                        else:
                            settings_dict[line_split[0].strip().upper() + '_' + orbital_type.upper()] = 'false'

                # if regular entry simply add
                else:
                    settings_dict[line_split[0].strip().upper()] = line_split[1].strip().lower()
            else:
                print('The line "' + lines[i] + '" cannot be parsed. Skipping this line.')

        # settings to extract
        node_features = []
        edge_features = []
        graph_features = []
        attributes = []

        bond_determination_mode = None
        bond_threshold = None

        hydrogen_mode = None
        hydrogen_count_threshold = None

        for key in settings_dict.keys():

            # # skip if set value to false
            # if settings_dict[key].lower() == 'false':
            #     continue

            if settings_dict[key].lower() != 'true' and not GraphGeneratorSettings._is_float(settings_dict[key].lower()):
                # if it is not a recognised key that takes non boolean arguments
                if not key == 'BOND_DETERMINATION_MODE' and \
                   not key == 'HYDROGEN_MODE' and \
                   not key == 'BOND_THRESHOLD' and \
                   not key == 'HYDROGEN_COUNT_THRESHOLD':
                    # skip if set value to false
                    if settings_dict[key].lower() == 'false':
                        continue
                    # if not recognised, warn user before skipping
                    else:
                        print('The value "' + settings_dict[key] + '" could not be parsed to a bool value. Defaulting to False.')
                        continue

            # look for bond determination mode
            if key == 'BOND_DETERMINATION_MODE':
                if bond_determination_mode is None:

                    # warn user if hydrogen mode not recognised
                    if settings_dict[key].upper() not in [x.name for x in BondDeterminationMode]:
                        print('BOND_DETERMINATION_MODE "' + settings_dict[key] + '" not found.')
                    else:
                        # get the appropraite mode
                        for mode in BondDeterminationMode:
                            if settings_dict[key].upper() == mode.name:
                                bond_determination_mode = mode

            # look for hydrogen mode
            if key == 'HYDROGEN_MODE':
                if hydrogen_mode is None:

                    # warn user if hydrogen mode not recognised
                    if settings_dict[key].upper() not in [x.name for x in HydrogenMode]:
                        print('HYDROGEN_MODE "' + settings_dict[key] + '" not found.')
                    else:
                        # get the appropraite mode
                        for mode in HydrogenMode:
                            if settings_dict[key].upper() == mode.name:
                                hydrogen_mode = mode

            # bond threshold
            if key == 'BOND_THRESHOLD':
                if GraphGeneratorSettings._is_float(settings_dict[key]):
                    bond_threshold = float(settings_dict[key])
                else:
                    print('Cannot parse value for bond threshold to float.')

            # hydrogen count threshold
            if key == 'HYDROGEN_COUNT_THRESHOLD':
                if GraphGeneratorSettings._is_float(settings_dict[key]):
                    hydrogen_count_threshold = float(settings_dict[key])
                else:
                    print('Cannot parse value for hydrogen count threshold to float.')

            # look for node features
            for node_feature in NodeFeature:
                if key == node_feature.name:
                    node_features.append(node_feature)

            # look for edge features
            for edge_feature in EdgeFeature:
                if key == edge_feature.name:
                    edge_features.append(edge_feature)

            # look for graph features
            for graph_feature in GraphFeature:
                if key == graph_feature.name:
                    graph_features.append(graph_feature)

            # look for qm attribute
            for qm_attribute in QmAttribute:
                if key == qm_attribute.name:
                    attributes.append(qm_attribute)

            # print('The key:\n\n\t' + key + '\n\nCould not be found. Skipping this key.')

        # check if values are set, otherwise use default values and warn user.
        if bond_threshold is None:
            print('No setting for BOND_THRESHOLD found. Defaulting to ' + str(DEFAULT_BOND_THRESHOLD))
            bond_threshold = DEFAULT_BOND_THRESHOLD

        if hydrogen_count_threshold is None:
            print('No setting for HYDROGEN_COUNT_THRESHOLD found. Defaulting to ' + str(DEFAULT_HYDROGEN_COUNT_THRESHOLD))
            hydrogen_count_threshold = DEFAULT_HYDROGEN_COUNT_THRESHOLD

        if bond_determination_mode is None:
            print('No setting for BOND_DETERMINATION_MODE found. Defaulting to ' + str(DEFAULT_BOND_DETERMINATION_MODE))
            bond_determination_mode = DEFAULT_BOND_DETERMINATION_MODE

        if hydrogen_mode is None:
            print('No setting for HYDROGEN_MODE found. Defaulting to ' + str(DEFAULT_HYDROGEN_MODE))
            hydrogen_mode = DEFAULT_HYDROGEN_MODE

        # # print statements for debugging
        # print(node_features)
        # print(edge_features)
        # print(graph_features)
        # print(attributes)
        # print(bond_threshold)
        # print(hydrogen_count_threshold)
        # print(hydrogen_mode)
        # print(bond_determination_mode)

        return cls(node_features=node_features,
                   edge_features=edge_features,
                   graph_features=graph_features,
                   attributes=attributes,
                   bond_determination_mode=bond_determination_mode,
                   bond_threshold=bond_threshold,
                   hydrogen_mode=hydrogen_mode,
                   hydrogen_count_threshold=hydrogen_count_threshold
                   )

    def _get_orbtials_to_extract_indices(self, mode: OrbitalOccupationTypes):

        """Helper function to parse information about which orbitals occupancies to use as node/edge features.

        Returns:
            list[int]: List specifying which orbital occupancies to consider (0 -> s, 1 -> p, 2 -> d, 3 -> f).
        """

        orbital_indices = []

        if mode == OrbitalOccupationTypes.LONE_PAIR:
            if NodeFeature.LONE_PAIRS_S in self.node_features:
                orbital_indices.append(0)
            if NodeFeature.LONE_PAIRS_P in self.node_features:
                orbital_indices.append(1)
            if NodeFeature.LONE_PAIRS_D in self.node_features:
                orbital_indices.append(2)
            if NodeFeature.LONE_PAIRS_F in self.node_features:
                orbital_indices.append(3)
        elif mode == OrbitalOccupationTypes.LONE_VACANCY:
            if NodeFeature.LONE_VACANCIES_S in self.node_features:
                orbital_indices.append(0)
            if NodeFeature.LONE_VACANCIES_P in self.node_features:
                orbital_indices.append(1)
            if NodeFeature.LONE_VACANCIES_D in self.node_features:
                orbital_indices.append(2)
            if NodeFeature.LONE_VACANCIES_F in self.node_features:
                orbital_indices.append(3)
        elif mode == OrbitalOccupationTypes.NATURAL_ELECTRON_CONFIGURATION:
            if NodeFeature.NATURAL_ELECTRON_CONFIGURATION_S in self.node_features:
                orbital_indices.append(0)
            if NodeFeature.NATURAL_ELECTRON_CONFIGURATION_P in self.node_features:
                orbital_indices.append(1)
            if NodeFeature.NATURAL_ELECTRON_CONFIGURATION_D in self.node_features:
                orbital_indices.append(2)
            if NodeFeature.NATURAL_ELECTRON_CONFIGURATION_F in self.node_features:
                orbital_indices.append(3)
        elif mode == OrbitalOccupationTypes.BOND_ORBITAL:
            if EdgeFeature.BOND_ORBITAL_DATA_S in self.edge_features:
                orbital_indices.append(0)
            if EdgeFeature.BOND_ORBITAL_DATA_P in self.edge_features:
                orbital_indices.append(1)
            if EdgeFeature.BOND_ORBITAL_DATA_D in self.edge_features:
                orbital_indices.append(2)
            if EdgeFeature.BOND_ORBITAL_DATA_F in self.edge_features:
                orbital_indices.append(3)
        elif mode == OrbitalOccupationTypes.ANTIBOND_ORBITAL:
            if EdgeFeature.ANTIBOND_ORBITAL_DATA_S in self.edge_features:
                orbital_indices.append(0)
            if EdgeFeature.ANTIBOND_ORBITAL_DATA_P in self.edge_features:
                orbital_indices.append(1)
            if EdgeFeature.ANTIBOND_ORBITAL_DATA_D in self.edge_features:
                orbital_indices.append(2)
            if EdgeFeature.ANTIBOND_ORBITAL_DATA_F in self.edge_features:
                orbital_indices.append(3)

        return orbital_indices

    @staticmethod
    def _is_float(value):

        try:
            float(value)
            return True
        except ValueError:
            return False
