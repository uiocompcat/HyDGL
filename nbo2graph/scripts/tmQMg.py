import os
import torch
from torch_geometric.data import Dataset
from tqdm import tqdm

from nbo2graph.graph_generator import GraphGenerator
from nbo2graph.graph_generator_settings import GraphGeneratorSettings
from nbo2graph.data_parser import DataParser
from nbo2graph.file_handler import FileHandler
from nbo2graph.tools import Tools


class tmQMg(Dataset):
    def __init__(self, root: str, settings: GraphGeneratorSettings, transform=None, pre_transform=None, pre_filter=None):

        self._graph_generator = GraphGenerator(settings)

        self._raw_file_extension = '.log'
        self._qm_data_file_extension = '.qmdata'
        self._graph_object_file_extension = '.graph'
        self._pytorch_graph_file_extension = '.pt'

        super().__init__(root, transform, pre_transform, pre_filter)

    @property
    def file_names(self):
        # random 500 file names
        return ['ICUMEY', 'VIRBEF', 'OGOBIV', 'RIVPUH', 'FIFCAB', 'DICTUE', 'LOGZIS', 'KUNBOK', 'VUSSUZ', 'TERJIK', 'UKASUU', 'LEZYOG', 'AGOHUZ', 'XIRFIP', 'AKUGIX', 'HINNEX', 'RACGUZ', 'TEXSUM', 'KELLUJ', 'FIVWIQ', 'SADXON', 'FERQOJ', 'VULFEN', 'VIGXOZ', 'VIHWEQ', 'QELDIU', 'WANNAB', 'EPIKIY', 'CAWLER', 'QARPUW', 'KELFEN', 'TIGXOY', 'HISJOI', 'GETWEI', 'KEQGIZ', 'KEJVEA', 'UFOYOE', 'MIDKUF', 'HESHAP', 'JEXZES', 'SUJPAO', 'FEFDUP', 'GEQXUW', 'TUDXIZ', 'DONCER', 'MAXNII', 'UNOPUJ', 'IPORUB', 'YATMAJ', 'SIXFAG', 'NANTUT', 'NIYBAY', 'HONDIZ', 'OZILEQ', 'CAXVED', 'SUFHOQ', 'MEHGIR', 'KILXEK', 'QIWKEN', 'FOBBUU', 'FAVSOM', 'DOQZIT', 'OREDIA', 'TITZEE', 'FEDJAA', 'QITXIC', 'JONNUY', 'MIVJEG', 'VEZGUD', 'YESXAW', 'XEFSOR', 'VUDYIC', 'SIZDOW', 'ENCYCO', 'MOQREQ', 'WABLAM', 'HORCIC', 'XAQFOK', 'FUYREY', 'EQURAL', 'PIBYOO', 'SOWMAV', 'TIHCAO', 'LOMWOB', 'TOCVAI', 'DMSCCR', 'AQAVIZ', 'NEVKII', 'QELVIM', 'UROPUN', 'CIRVOO', 'PIBQOJ', 'WIHLEE', 'UCEBOT', 'RIVZUU', 'HIKKIY', 'POTVOJ', 'ZUJHAP', 'LITWUJ', 'CIXGIA', 'ADOCII', 'BIGRAL', 'CIDZEX', 'OXEBUP', 'GIRCIW', 'JECBOJ', 'WAKGAT', 'REWMEO', 'FITLUQ', 'JOWBII', 'HUXSOK', 'MADWIZ', 'EMUQAG', 'QAHBAC', 'FAVTUR', 'BOYQAH', 'YIWTAC', 'QIWNIU', 'WADGUE', 'XIFBOG', 'LUZSUV', 'YEDGUM', 'VEGKIC', 'MAKGIO', 'VOWDAO', 'IVAPIG', 'SIYQOJ', 'QEZQER', 'RIDJEU', 'WEDBIQ', 'ZESHEN', 'FIJFEL', 'POYMAS', 'UHALEV', 'NEVNIO', 'ETESON', 'POJFEA', 'BINCOQ', 'RISCEE', 'BITHUH', 'BCNFEC', 'DAZTOO', 'LARYOS', 'EZURUN', 'SIKZOE', 'BOJHUF', 'CUQPIP', 'SEMXAL', 'QAYZAR', 'MACZEW', 'POTNEU', 'DOGJIT', 'FEFYUL', 'QACKIP', 'ZOJROI', 'GAKQIV', 'XEYNAS', 'QIRYEW', 'TUNKET', 'GATMAP', 'USUXOX', 'YAVLAL', 'GEHJOS', 'MODXEL', 'ATEPUL', 'WAPMEH', 'QEBPAR', 'UDOFAW', 'WUCXUP', 'COMSPW', 'GUPDOM', 'BENDOO', 'JUHPAF', 'CIMWED', 'VONVAX', 'RIDNEZ', 'ITUVEA', 'FIVCAP', 'KOBBEJ', 'QOFTIO', 'IXEZOB', 'GASNOF', 'WEJFUN', 'NOBBAJ', 'HEXFOH', 'AKILAJ', 'OYOPEY', 'EGIBEB', 'UXUQAG', 'SUMBIN', 'APICUY', 'COCSET', 'NEDKOZ', 'NIBHEO', 'SIRLEM', 'GAYRIJ', 'CETZIN', 'WUGVOJ', 'GIRVAH', 'MESDIA', 'TIBQUR', 'TADLOZ', 'SASGOL', 'HOKCEQ', 'MECKAH', 'YOGCIG', 'UMATOR', 'YOWWAK', 'DAZRUU', 'XUYCAV', 'ROLMUB', 'NIVPUG', 'NOSZIE', 'TBPCFE', 'DUMJIE', 'BAQROB', 'AFUXOP', 'WELJUS', 'FOTXOD', 'ZIFVUH', 'VEYTAX', 'OYIDIL', 'DITFUI', 'RAYHIK', 'ROGGUP', 'XEJSEK', 'CEMSEU', 'ATOPII', 'XOGCUU', 'OFAHOS', 'REBDEI', 'ZOCCAV', 'MALWAZ', 'ZUJHIX', 'ZOHQOE', 'SOTWAA', 'FOSHIG', 'WURFAS', 'FUNKOP', 'KEWROT', 'SIWFAG', 'HUPNAI', 'KEBGUU', 'EKEDIJ', 'MAQPIG', 'URUGUL', 'GEPKIW', 'SUPYIN', 'KIMLOH', 'BEZVOT', 'NECJUC', 'PIZGOV', 'IGATUF', 'QABYAV', 'FIPFEQ', 'KIBMAK', 'EHEBIE', 'SEPZOC', 'VUYXUJ', 'LEGXEA', 'OAMECO', 'KEJMES', 'KULGIH', 'UDARUP', 'INEQAU', 'KIJSUS', 'SANRUV', 'LOKPEH', 'COCXAU', 'ZEGVIQ', 'CMEEAM', 'WALZIU', 'MIFVIH', 'VOVRAZ', 'BOTZUI', 'QOZBOY', 'ROBYAJ', 'PUNFIN', 'HECCEX', 'LETTOW', 'OTEVOZ', 'MHPYCR', 'WILHOR', 'VIVKIV', 'VIJWAO', 'LEJPEW', 'FENVEA', 'AHASAF', 'NEFXOM', 'QOGBEU', 'LETXEQ', 'WEFLOI', 'MIRDUN', 'SEBTUO', 'WIRHOU', 'HIGQIX', 'FACGUN', 'LADVIY', 'ROLTES', 'GIWNEH', 'MIVBEZ', 'MIYWIA', 'PALZOS', 'LEYZAT', 'QEFSEB', 'FIPTED', 'UFIZAM', 'REFRAV', 'KUNWIB', 'SETPOX', 'HOSWAP', 'LIMZOY', 'JIPTIO', 'VIKZEW', 'ZEJVER', 'VASJOO', 'IGEBEB', 'OKEZOU', 'MUPFAE', 'SUYXAN', 'JIPJAU', 'SULYED', 'WEHLIH', 'YIDGAW', 'CAGBAQ', 'ZAVROG', 'GIYMAC', 'GEFWUM', 'LIPMAY', 'GORMOP', 'ROQRAT', 'TIVNUJ', 'HUDYAG', 'DODNAL', 'MARWEK', 'SAKHUJ', 'GAWYIM', 'HEVDOB', 'PIKBOB', 'UVOFUI', 'VUDKEM', 'YODMUB', 'UCUSIX', 'RISLIR', 'RERQUA', 'TATTEO', 'JIRBAN', 'REVPAL', 'QOXKOF', 'ZOQFOA', 'MAXQUX', 'DOSXAN', 'JOFTIK', 'KUCWUC', 'KAYBIV', 'SEQGIH', 'TAGHAK', 'QONHEG', 'OGATOI', 'XUQWOX', 'VOWXAG', 'BEKPUC', 'GOGPEA', 'GUVFAG', 'PUJWUM', 'VALKAV', 'SELSIL', 'UGOHOO', 'KASKAQ', 'NIBCIM', 'RITRIY', 'UTIXAY', 'XOTVAD', 'GOYVIB', 'KUNQOA', 'VEMWOA', 'JATBEL', 'LAMDUY', 'EMAZID', 'TULGUC', 'BULYEM', 'FIQCUF', 'AFICIC', 'VORCIR', 'HELGEK', 'VEZGEO', 'MEBXUN', 'UQAFUO', 'ZUYHEG', 'FUZFIQ', 'YOJNUG', 'FANLIP', 'PEQCUK', 'VEQLEI', 'VUWMAB', 'LAZQIP', 'PEZFUY', 'BABQUR', 'JUPPOZ', 'SIYLES', 'XOTLOJ', 'BOJMAQ', 'AQENIV', 'MAJBAC', 'LUYXAE', 'ROJLUX', 'LAXCOF', 'JOTJOR', 'QAYCEB', 'PALTAX', 'TUYPIM', 'UQAMEF', 'KICYAW', 'HUVSUN', 'YOSYEM', 'USONUN', 'EWISOS', 'REWHIK', 'OMEBEN', 'UDOVAM', 'EMULON', 'PUFQUC', 'UCEDOX', 'IFEGEH', 'TIKWAN', 'YEMVER', 'SIHTOT', 'COZFIH', 'MAMSAU', 'ETACEH', 'ZOCBEY', 'YEBXOV', 'YEBYAI', 'EZARAA', 'WUXCOI', 'ZIWPAW', 'YEKCOH', 'BAKBEV', 'GIQWEK', 'TIYNAT', 'IMAKOX', 'UJADAK', 'XUBKUB', 'TEXDOS', 'XAJWOX', 'QUJXEZ', 'TIFTUX', 'PUDPAF', 'ZIRJOZ', 'JAQPAS', 'QOPWIB', 'MASLEA', 'BUZQUK', 'CODYOK', 'AXIBAK', 'SUVYUF', 'JURGUY', 'LAQVEH', 'XOBFIF', 'OGEYAC', 'EPIMEW', 'JOKVOX', 'MUKHUX', 'CAFROQ', 'XIDGUO', 'SIMXIX', 'KAMSUM', 'TUMPEY', 'MECCEF', 'VIKRAJ', 'ALINEP', 'UYOVUA', 'QIJREI', 'ZITYOQ', 'VAWCEE', 'VOVDIV', 'SIJJUT', 'ZOLSOI', 'CEGKEH', 'GIDPAM', 'QAKBOT', 'FOCJIR', 'YEZBEK', 'BERQEV', 'ZAXXUR', 'BOVBOG', 'YILQAO', 'HETMUO', 'PEYGEI', 'ISITEL', 'XELDIE', 'BUKYUC', 'LOPDEC', 'JOCKAO', 'JOJZAK', 'QAQGEX', 'QUCBIB']
        # TODO: full tmQMg dataset

    @property
    def qm_data_dir(self):
        return self.root + '/qm_data'

    @property
    def graph_object_dir(self):
        return self.root + '/graph_objects'

    @property
    def raw_file_names(self):
        return [file_name + self._raw_file_extension for file_name in self.file_names]

    @property
    def processed_file_names(self):
        return 'not implemented'

    def download(self):

        """Function to download raw data."""

        print('Trying to download..')
        raise NotImplementedError('Download function is not implemented.')

    def len(self):

        """Getter for the number of processed pytorch graphs."""

        return len(self.file_names)

    def get(self, idx):

        """Accessor for processed pytorch graphs."""

        data = torch.load(self.processed_dir + '/' + self.file_names[idx] + '.pt')
        return data

    def process(self):

        print('')

        print('Extracting QmData..')
        self.extract_qm_data()

        print('Building graph objects..')
        self.build_graph_objects()

        print('Building pytorch graphs..')
        self.build_pytorch_graphs()

    def get_edge_class_feature_dict(self):

        """Gets a dict for one-hot enconding class-type features in edge features."""

        graph_object_files = [file for file in os.listdir(self.graph_object_dir)]

        pivot_graph_object = FileHandler.read_binary_file(self.graph_object_dir + '/' + graph_object_files[0])
        # get indicies in edge feature list that are non-numerical class values
        edge_class_feature_indices = Tools.get_class_feature_indices(pivot_graph_object.edges[0].features)

        # iterate through the edges of all graphs to obtain lists of class for each of the class indices
        edge_class_features = [[] for idx in edge_class_feature_indices]
        for file_name in graph_object_files:
            # read graph object
            graph_object = FileHandler.read_binary_file(self.graph_object_dir + '/' + file_name)

            for edge in graph_object.edges:
                for i in range(len(edge_class_feature_indices)):
                    if edge.features[edge_class_feature_indices[i]] not in edge_class_features[i]:
                        edge_class_features[i].append(edge.features[edge_class_feature_indices[i]])

        # build a dict that contains indices as keys and class features as values
        edge_class_feature_dict = {}
        for i in range(len(edge_class_feature_indices)):
            edge_class_feature_dict[edge_class_feature_indices[i]] = edge_class_features[i]

        return edge_class_feature_dict

    def extract_qm_data(self):

        """Extracts raw data into QmData objects."""

        # create qm_data directory if it does not exist
        if not os.path.isdir(self.qm_data_dir):
            os.mkdir(self.qm_data_dir)

        qm_data_files = [file for file in os.listdir(self.qm_data_dir)]
        for file_name in tqdm(self.file_names):

            # if file is not extracted yet
            if file_name + self._qm_data_file_extension not in qm_data_files:
                # extract QmData
                qm_data = DataParser(self.raw_dir + '/' + file_name + self._raw_file_extension).parse_to_qm_data_object()
                # write to file
                FileHandler.write_binary_file(self.qm_data_dir + '/' + file_name + self._qm_data_file_extension, qm_data)

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
                qm_data = FileHandler.read_binary_file(self.qm_data_dir + '/' + file_name + self._qm_data_file_extension)
                # build graph
                graph_object = self._graph_generator.generate_graph(qm_data)
                # write to file
                FileHandler.write_binary_file(self.graph_object_dir + '/' + file_name + self._graph_object_file_extension, graph_object)

    def build_pytorch_graphs(self):

        """Builds pytorch graphs from previously built grah objects."""

        # get dict for one-hot edge encoding of edges
        edge_class_feature_dict = self.get_edge_class_feature_dict()

        pytorch_graph_files = [file for file in os.listdir(self.processed_dir)]
        for file_name in tqdm(self.file_names):

            # if pytorch graph is not built yet
            if file_name + self._pytorch_graph_file_extension not in pytorch_graph_files:
                # read graph object
                graph_object = FileHandler.read_binary_file(self.graph_object_dir + '/' + file_name + self._graph_object_file_extension)
                # get pytorch graph
                graph = graph_object.get_pytorch_data_object(edge_class_feature_dict)
                # write to file
                torch.save(graph, self.processed_dir + '/' + file_name + self._pytorch_graph_file_extension)

    def clear_directories(self):

        """Deletes all files in the qm_data, graph_objects and processed directories."""

        self.clear_qm_data_dir()
        self.clear_graph_directories()

    def clear_graph_directories(self):

        """Deletes all graph files in the graph_objects and processed directories."""

        self.clear_graph_object_dir()
        self.clear_processed_dir()

    def clear_qm_data_dir(self):

        """Deletes all files in the qm_data directory."""

        FileHandler.clear_directory(self.qm_data_dir, [file_name + self._qm_data_file_extension for file_name in self.file_names])

    def clear_graph_object_dir(self):

        """Deletes all files in the graph_objects directory."""

        FileHandler.clear_directory(self.graph_object_dir, [file_name + self._graph_object_file_extension for file_name in self.file_names])

    def clear_processed_dir(self):

        """Deletes all files in the processed directory."""

        FileHandler.clear_directory(self.processed_dir, [file_name + self._pytorch_graph_file_extension for file_name in self.file_names])
