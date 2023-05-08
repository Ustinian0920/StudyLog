from .Hdf5Parser import Hdf5Parser
from .AfileParser import AfileParser
from .GfileParser import GfileParser
from .parser_factory import ParserFactory
from .swtree import *
parser_list = [
    "afile",
    "gfile",
    "hdf5",
    "netcdf",
    "text_file",
    "json",
    "xml"
]