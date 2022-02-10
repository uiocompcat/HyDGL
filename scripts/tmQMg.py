import os
import torch
import numpy as np
from torch_geometric.data import Dataset
from tqdm import tqdm

from nbo2graph.graph_generator import GraphGenerator
from nbo2graph.graph_generator_settings import GraphGeneratorSettings
from nbo2graph.file_handler import FileHandler
from nbo2graph.qm_data import QmData
from nbo2graph.tools import Tools


class tmQMg(Dataset):
    def __init__(self, root: str, raw_dir: str, settings: GraphGeneratorSettings, transform=None, pre_transform=None, pre_filter=None):

        # if root path does not exist create folder
        if not os.path.isdir(root):
            os.makedirs(root, exist_ok=True)

        # set up graph generator
        self._graph_generator = GraphGenerator(settings)

        # directory to get raw dat from
        self._raw_dir = raw_dir

        self._raw_file_extension = '.json'
        self._graph_object_file_extension = '.graph'
        self._pytorch_graph_file_extension = '.pt'

        super().__init__(root, transform, pre_transform, pre_filter)

        self.process_()

    @property
    def file_names(self):
        # random 500 file names
        return ['LALMER', 'ICUMEY', 'VIRBEF', 'OGOBIV', 'RIVPUH', 'FIFCAB', 'DICTUE', 'LOGZIS', 'KUNBOK', 'VUSSUZ', 'TERJIK', 'UKASUU', 'LEZYOG', 'AGOHUZ', 'XIRFIP', 'AKUGIX', 'HINNEX', 'RACGUZ', 'TEXSUM', 'KELLUJ', 'FIVWIQ', 'SADXON', 'FERQOJ', 'VULFEN', 'VIGXOZ', 'VIHWEQ', 'QELDIU', 'WANNAB', 'EPIKIY', 'CAWLER', 'QARPUW', 'KELFEN', 'TIGXOY', 'HISJOI', 'GETWEI', 'KEQGIZ', 'KEJVEA', 'UFOYOE', 'MIDKUF', 'HESHAP', 'JEXZES', 'SUJPAO', 'FEFDUP', 'GEQXUW', 'TUDXIZ', 'DONCER', 'MAXNII', 'UNOPUJ', 'IPORUB', 'YATMAJ', 'SIXFAG', 'NANTUT', 'NIYBAY', 'HONDIZ', 'OZILEQ', 'CAXVED', 'SUFHOQ', 'MEHGIR', 'KILXEK', 'QIWKEN', 'FOBBUU', 'FAVSOM', 'DOQZIT', 'OREDIA', 'TITZEE', 'FEDJAA', 'QITXIC', 'JONNUY', 'MIVJEG', 'VEZGUD', 'YESXAW', 'XEFSOR', 'VUDYIC', 'SIZDOW', 'ENCYCO', 'MOQREQ', 'WABLAM', 'HORCIC', 'XAQFOK', 'FUYREY', 'EQURAL', 'PIBYOO', 'SOWMAV', 'TIHCAO', 'LOMWOB', 'TOCVAI', 'DMSCCR', 'AQAVIZ', 'NEVKII', 'QELVIM', 'UROPUN', 'CIRVOO', 'PIBQOJ', 'WIHLEE', 'UCEBOT', 'RIVZUU', 'HIKKIY', 'POTVOJ', 'ZUJHAP', 'LITWUJ', 'CIXGIA', 'ADOCII', 'BIGRAL', 'CIDZEX', 'OXEBUP', 'GIRCIW', 'JECBOJ', 'WAKGAT', 'REWMEO', 'FITLUQ', 'JOWBII', 'HUXSOK', 'MADWIZ', 'EMUQAG', 'QAHBAC', 'FAVTUR', 'BOYQAH', 'YIWTAC', 'QIWNIU', 'WADGUE', 'XIFBOG', 'LUZSUV', 'YEDGUM', 'VEGKIC', 'MAKGIO', 'VOWDAO', 'IVAPIG', 'SIYQOJ', 'QEZQER', 'RIDJEU', 'WEDBIQ', 'ZESHEN', 'FIJFEL', 'POYMAS', 'UHALEV', 'NEVNIO', 'ETESON', 'POJFEA', 'BINCOQ', 'RISCEE', 'BITHUH', 'BCNFEC', 'DAZTOO', 'LARYOS', 'EZURUN', 'SIKZOE', 'BOJHUF', 'CUQPIP', 'SEMXAL', 'QAYZAR', 'MACZEW', 'POTNEU', 'DOGJIT', 'FEFYUL', 'QACKIP', 'ZOJROI', 'GAKQIV', 'XEYNAS', 'QIRYEW', 'TUNKET', 'GATMAP', 'USUXOX', 'YAVLAL', 'GEHJOS', 'MODXEL', 'ATEPUL', 'WAPMEH', 'QEBPAR', 'UDOFAW', 'WUCXUP', 'COMSPW', 'GUPDOM', 'BENDOO', 'JUHPAF', 'CIMWED', 'VONVAX', 'RIDNEZ', 'ITUVEA', 'FIVCAP', 'KOBBEJ', 'QOFTIO', 'IXEZOB', 'GASNOF', 'WEJFUN', 'NOBBAJ', 'HEXFOH', 'AKILAJ', 'OYOPEY', 'EGIBEB', 'UXUQAG', 'SUMBIN', 'APICUY', 'COCSET', 'NEDKOZ', 'NIBHEO', 'SIRLEM', 'GAYRIJ', 'CETZIN', 'WUGVOJ', 'GIRVAH', 'MESDIA', 'TIBQUR', 'TADLOZ', 'SASGOL', 'HOKCEQ', 'MECKAH', 'YOGCIG', 'UMATOR', 'YOWWAK', 'DAZRUU', 'XUYCAV', 'ROLMUB', 'NIVPUG', 'NOSZIE', 'TBPCFE', 'DUMJIE', 'BAQROB', 'AFUXOP', 'WELJUS', 'FOTXOD', 'ZIFVUH', 'VEYTAX', 'OYIDIL', 'DITFUI', 'RAYHIK', 'ROGGUP', 'XEJSEK', 'CEMSEU', 'ATOPII', 'XOGCUU', 'OFAHOS', 'REBDEI', 'ZOCCAV', 'MALWAZ', 'ZUJHIX', 'ZOHQOE', 'SOTWAA', 'FOSHIG', 'WURFAS', 'FUNKOP', 'KEWROT', 'SIWFAG', 'HUPNAI', 'KEBGUU', 'EKEDIJ', 'MAQPIG', 'URUGUL', 'GEPKIW', 'SUPYIN', 'KIMLOH', 'BEZVOT', 'NECJUC', 'PIZGOV', 'IGATUF', 'QABYAV', 'FIPFEQ', 'KIBMAK', 'EHEBIE', 'SEPZOC', 'VUYXUJ', 'LEGXEA', 'OAMECO', 'KEJMES', 'KULGIH', 'UDARUP', 'INEQAU', 'KIJSUS', 'SANRUV', 'LOKPEH', 'COCXAU', 'ZEGVIQ', 'CMEEAM', 'WALZIU', 'MIFVIH', 'VOVRAZ', 'BOTZUI', 'QOZBOY', 'ROBYAJ', 'PUNFIN', 'HECCEX', 'LETTOW', 'OTEVOZ', 'MHPYCR', 'WILHOR', 'VIVKIV', 'VIJWAO', 'LEJPEW', 'FENVEA', 'AHASAF', 'NEFXOM', 'QOGBEU', 'LETXEQ', 'WEFLOI', 'MIRDUN', 'SEBTUO', 'WIRHOU', 'HIGQIX', 'FACGUN', 'LADVIY', 'ROLTES', 'GIWNEH', 'MIVBEZ', 'MIYWIA', 'PALZOS', 'LEYZAT', 'QEFSEB', 'FIPTED', 'UFIZAM', 'REFRAV', 'KUNWIB', 'SETPOX', 'HOSWAP', 'LIMZOY', 'JIPTIO', 'VIKZEW', 'ZEJVER', 'VASJOO', 'IGEBEB', 'OKEZOU', 'MUPFAE', 'SUYXAN', 'JIPJAU', 'SULYED', 'WEHLIH', 'YIDGAW', 'CAGBAQ', 'ZAVROG', 'GIYMAC', 'GEFWUM', 'LIPMAY', 'GORMOP', 'ROQRAT', 'TIVNUJ', 'HUDYAG', 'DODNAL', 'MARWEK', 'SAKHUJ', 'GAWYIM', 'HEVDOB', 'PIKBOB', 'UVOFUI', 'VUDKEM', 'YODMUB', 'UCUSIX', 'RISLIR', 'RERQUA', 'TATTEO', 'JIRBAN', 'REVPAL', 'QOXKOF', 'ZOQFOA', 'MAXQUX', 'DOSXAN', 'JOFTIK', 'KUCWUC', 'KAYBIV', 'SEQGIH', 'TAGHAK', 'QONHEG', 'OGATOI', 'XUQWOX', 'VOWXAG', 'BEKPUC', 'GOGPEA', 'GUVFAG', 'PUJWUM', 'VALKAV', 'SELSIL', 'UGOHOO', 'KASKAQ', 'NIBCIM', 'RITRIY', 'UTIXAY', 'XOTVAD', 'GOYVIB', 'KUNQOA', 'VEMWOA', 'JATBEL', 'LAMDUY', 'EMAZID', 'TULGUC', 'BULYEM', 'FIQCUF', 'AFICIC', 'VORCIR', 'HELGEK', 'VEZGEO', 'MEBXUN', 'UQAFUO', 'ZUYHEG', 'FUZFIQ', 'YOJNUG', 'FANLIP', 'PEQCUK', 'VEQLEI', 'VUWMAB', 'LAZQIP', 'PEZFUY', 'BABQUR', 'JUPPOZ', 'SIYLES', 'XOTLOJ', 'BOJMAQ', 'AQENIV', 'MAJBAC', 'LUYXAE', 'ROJLUX', 'LAXCOF', 'JOTJOR', 'QAYCEB', 'PALTAX', 'TUYPIM', 'UQAMEF', 'KICYAW', 'HUVSUN', 'YOSYEM', 'USONUN', 'EWISOS', 'REWHIK', 'OMEBEN', 'UDOVAM', 'EMULON', 'PUFQUC', 'UCEDOX', 'IFEGEH', 'TIKWAN', 'YEMVER', 'SIHTOT', 'COZFIH', 'MAMSAU', 'ETACEH', 'ZOCBEY', 'YEBXOV', 'YEBYAI', 'EZARAA', 'WUXCOI', 'ZIWPAW', 'YEKCOH', 'BAKBEV', 'GIQWEK', 'TIYNAT', 'IMAKOX', 'UJADAK', 'XUBKUB', 'TEXDOS', 'XAJWOX', 'QUJXEZ', 'TIFTUX', 'PUDPAF', 'ZIRJOZ', 'JAQPAS', 'QOPWIB', 'MASLEA', 'BUZQUK', 'CODYOK', 'AXIBAK', 'SUVYUF', 'JURGUY', 'LAQVEH', 'XOBFIF', 'OGEYAC', 'EPIMEW', 'JOKVOX', 'MUKHUX', 'CAFROQ', 'XIDGUO', 'SIMXIX', 'KAMSUM', 'TUMPEY', 'MECCEF', 'VIKRAJ', 'ALINEP', 'UYOVUA', 'QIJREI', 'ZITYOQ', 'VAWCEE', 'VOVDIV', 'SIJJUT', 'ZOLSOI', 'CEGKEH', 'GIDPAM', 'QAKBOT', 'FOCJIR', 'YEZBEK', 'BERQEV', 'ZAXXUR', 'BOVBOG', 'YILQAO', 'HETMUO', 'PEYGEI', 'ISITEL', 'XELDIE', 'BUKYUC', 'LOPDEC', 'JOCKAO', 'JOJZAK', 'QAQGEX', 'QUCBIB']
        # TODO: full tmQMg dataset

    @property
    def raw_dir(self):
        return self._raw_dir

    @property
    def scaled_pytorch_geometric_dir(self):
        return self.root + '/pyg_scaled'

    @property
    def pytorch_geometric_dir(self):
        return self.root + '/pyg'

    @property
    def graph_object_dir(self):
        return self.root + '/graph_objects'

    @property
    def raw_file_names(self):
        return [file_name + self._raw_file_extension for file_name in self.file_names]

    @property
    def processed_file_names(self):
        return 'data'

    def download(self):

        """Function to download raw data."""

        print('Trying to download..')
        raise NotImplementedError('Download function is not implemented.')

    def len(self):

        """Getter for the number of processed pytorch graphs."""

        return len(self.file_names)

    def get(self, idx):

        """Accessor for processed pytorch graphs."""

        return self.graphs[idx]

        data = torch.load(self.processed_dir + '/' + self.file_names[idx] + '.pt')
        return data

    def process_(self):

        print('')

        print('Building graph objects..')
        self.build_graph_objects()

        print('Building pytorch graphs..')
        self.build_pytorch_graphs()

        print('Scaling features')
        self.standard_scale_pytorch_graphs()

        # update in memory graphs
        # self.graphs = [torch.load(self.pytorch_geometric_dir + '/' + file_name + '.pt') for file_name in self.file_names]
        self.graphs = [torch.load(self.scaled_pytorch_geometric_dir + '/' + file_name + '.pt') for file_name in self.file_names]

    def get_full_feature_matrices(self, graphs: list):

        """Gets the node and edge features of all graphs in terms of two matrices."""

        node_feature_matrix = None
        edge_feature_matrix = None

        for graph in graphs:

            if node_feature_matrix is None:
                node_feature_matrix = graph['x'].detach().numpy()
            else:
                node_feature_matrix = np.concatenate((node_feature_matrix, graph['x'].detach().numpy()), axis=0)

            if edge_feature_matrix is None:
                edge_feature_matrix = graph['edge_attr'].detach().numpy()
            else:
                edge_feature_matrix = np.concatenate((edge_feature_matrix, graph['edge_attr'].detach().numpy()), axis=0)

        return node_feature_matrix, edge_feature_matrix

    def get_class_feature_dicts(self):

        """Gets dicts for one-hot enconding class-type features in node and edge features."""

        graph_object_files = [file for file in os.listdir(self.graph_object_dir)]

        pivot_graph_object = FileHandler.read_binary_file(self.graph_object_dir + '/' + graph_object_files[0])

        if len(pivot_graph_object.nodes) == 0:
            node_class_feature_keys = []
        else:
            # get indicies in node feature list that are non-numerical class values
            node_class_feature_keys = Tools.get_class_feature_keys(pivot_graph_object.nodes[0].features)

        if len(pivot_graph_object.edges) == 0:
            edge_class_feature_keys = []
        else:
            # get indicies in edge feature list that are non-numerical class values
            edge_class_feature_keys = Tools.get_class_feature_keys(pivot_graph_object.edges[0].features)

        # class features
        node_class_features = [[] for idx in node_class_feature_keys]
        edge_class_features = [[] for idx in edge_class_feature_keys]

        for file_name in graph_object_files:
            # read graph object
            graph_object = FileHandler.read_binary_file(self.graph_object_dir + '/' + file_name)

            # iterate through the nodes of all graphs to obtain lists of class for each of the class indices
            for node in graph_object.nodes:
                for i, key in enumerate(node_class_feature_keys):
                    if node.features[key] not in node_class_features[i]:
                        node_class_features[i].append(node.features[key])

            # iterate through the edges of all graphs to obtain lists of class for each of the class indices
            for edge in graph_object.edges:
                for i, key in enumerate(edge_class_feature_keys):
                    if edge.features[key] not in edge_class_features[i]:
                        edge_class_features[i].append(edge.features[key])

        # build dicts that contain feature keys as keys and lists of possible class features as values
        node_class_feature_dict = {}
        for i, key in enumerate(node_class_feature_keys):
            node_class_feature_dict[key] = edge_class_features[i]

        edge_class_feature_dict = {}
        for i, key in enumerate(edge_class_feature_keys):
            edge_class_feature_dict[key] = edge_class_features[i]

        return node_class_feature_dict, edge_class_feature_dict

    def build_graph_objects(self):

        """Builds graph objects from previously extracted QmData."""

        # create graph_object directory if it does not exist
        if not os.path.isdir(self.graph_object_dir):
            os.mkdir(self.graph_object_dir)

        graph_object_files = [file for file in os.listdir(self.graph_object_dir)]
        for file_name in tqdm(self.file_names):

            # if graph is not built yet
            if file_name + self._graph_object_file_extension not in graph_object_files:
                # read QmData file
                qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(self.raw_dir + '/' + file_name + self._raw_file_extension))
                # build graph
                graph_object = self._graph_generator.generate_graph(qm_data)
                # write to file
                FileHandler.write_binary_file(self.graph_object_dir + '/' + file_name + self._graph_object_file_extension, graph_object)

    def build_pytorch_graphs(self):

        """Builds pytorch graphs from previously built grah objects."""

        # create pytorch directory if it does not exist
        if not os.path.isdir(self.pytorch_geometric_dir):
            os.mkdir(self.pytorch_geometric_dir)

        # get dict for one-hot edge encoding of edges
        node_class_feature_dict, edge_class_feature_dict = self.get_class_feature_dicts()

        pytorch_graph_files = [file for file in os.listdir(self.pytorch_geometric_dir)]
        for file_name in tqdm(self.file_names):

            # if pytorch graph is not built yet
            if file_name + self._pytorch_graph_file_extension not in pytorch_graph_files:
                # read graph object
                graph_object = FileHandler.read_binary_file(self.graph_object_dir + '/' + file_name + self._graph_object_file_extension)
                # get pytorch graph
                graph = graph_object.get_pytorch_data_object(node_class_feature_dict=node_class_feature_dict, edge_class_feature_dict=edge_class_feature_dict)
                # write to file
                torch.save(graph, self.pytorch_geometric_dir + '/' + file_name + self._pytorch_graph_file_extension)

    def standard_scale_pytorch_graphs(self):

        """Scales pytorch graphs using the StandardScaler."""

        # create pytorch directory if it does not exist
        if not os.path.isdir(self.scaled_pytorch_geometric_dir):
            os.mkdir(self.scaled_pytorch_geometric_dir)

        # get graphs
        graphs = [torch.load(self.pytorch_geometric_dir + '/' + file_name + '.pt') for file_name in self.file_names]
        node_feature_matrix, edge_feature_matrix = self.get_full_feature_matrices(graphs)

        node_feature_stds = np.std(node_feature_matrix, axis=0)
        node_feature_means = np.mean(node_feature_matrix, axis=0)

        edge_feature_stds = np.std(edge_feature_matrix, axis=0)
        edge_feature_means = np.mean(edge_feature_matrix, axis=0)

        for i, graph in enumerate(tqdm(graphs)):
            # scale features
            graph['x'] = (graph['x'] - node_feature_means) / node_feature_stds
            graph['edge_attr'] = (graph['edge_attr'] - edge_feature_means) / edge_feature_stds
            # write to file
            torch.save(graph, self.scaled_pytorch_geometric_dir + '/' + self.file_names[i] + self._pytorch_graph_file_extension)

    def clear_directories(self):

        """Deletes all files in the raw, graph_objects and processed directories."""

        self.clear_raw_dir()
        self.clear_graph_directories()

    def clear_graph_directories(self):

        """Deletes all graph files in the graph_objects and processed directories."""

        self.clear_graph_object_dir()
        self.clear_processed_dir()

    def clear_raw_dir(self):

        """Deletes all files in the raw directory."""

        print('This will delete the files in the raw data directory.')
        reply = input('Do you really wish to continue? [Y/n]')
        while not (reply.strip().lower() == 'y' or reply.strip().lower() == 'n'):
            reply = input('Please anser with "y" or "n".')

        if reply.lower() == 'y':
            FileHandler.clear_directory(self.raw_dir, [file_name + self._raw_file_extension for file_name in self.file_names])
        elif reply.lower() == 'n':
            print('Aborting. If you only wish to clear the directories containing graph representations use the "clear_graph_directories()" function.')

    def clear_graph_object_dir(self):

        """Deletes all files in the graph_objects directory."""

        FileHandler.clear_directory(self.graph_object_dir, [file_name + self._graph_object_file_extension for file_name in self.file_names])

    def clear_processed_dir(self):

        """Deletes all files in the processed directory."""

        FileHandler.clear_directory(self.processed_dir, [file_name + self._pytorch_graph_file_extension for file_name in self.file_names])
