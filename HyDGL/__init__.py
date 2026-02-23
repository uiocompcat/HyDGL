__all__ = [
    "QmData",
    "Graph",
    "GraphGenerator",
    "GraphGeneratorSettings",
    "ElementLookUpTable",
    "FileHandler",
]

def __getattr__(name):
    if name == "GraphGeneratorSettings":
        from .graph_generator_settings import GraphGeneratorSettings
        return GraphGeneratorSettings
    if name == "Graph":
        from .graph import Graph
        return Graph
    if name == "GraphGenerator":
        from .graph_generator import GraphGenerator
        return GraphGenerator
    if name == "QmData":
        from .qm_data import QmData
        return QmData
    if name == "ElementLookUpTable":
        from .element_look_up_table import ElementLookUpTable
        return ElementLookUpTable
    if name == "FileHandler":
        from .file_handler import FileHandler
        return FileHandler
    raise AttributeError(f"module {__name__} has no attribute {name}")

__version__ = '0.1'
