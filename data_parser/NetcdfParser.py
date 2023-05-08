from .parser import FileDataParser,Mapper
from .swtree import SWTree,SWNode
import os 
from datetime import datetime
import math
import numpy as np
import json
import logging
from netCDF4 import Dataset
import yaml
class NetcdfParser(FileDataParser):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.keys = []

        
    def write(self,sw_tree):
        ...
    #解析NetCDF 并构建SWTree
    def read(self):
        _,file = os.path.split(self.file_path)
        nc_data = Dataset(self.file_path)
        data = {}
        if self.mapper_path != None:
            if os.path.exists(self.mapper_path):
                with open(self.mapper_path,'r') as f:
                    mapper_data = yaml.safe_load(f)
                    items = mapper_data['items']
                    for i in items:
                        data_path = i['data_path']
                        value = nc_data.variables[data_path][:]
                        value = value.tolist()
                        data[data_path] = value
                
        # curden = nc_data.variables["curden"][:]
        # data["curden"] = curden.tolist()
        # # print("curden: ",curden)
        
        # curden = nc_data.variables["curbeam"][:]
        # data["curbeam"] = curden.tolist()
        # # print("curbeam: ",curden)
        
        # curden = nc_data.variables["curboot"][:]
        # data["curboot"] = curden.tolist()
        # # print("curboot: ",curden)
        
        # curden = nc_data.variables["curohm"][:]
        # data["curohm"] = curden.tolist()
        # # print("curohm: ",curden)
        
        # curden = nc_data.variables["currf"][:]
        # data["currf"] = curden.tolist()
        # # print("currf: ",curden)
        
        # curden = nc_data.variables["press"][:]
        # data["press"] = curden.tolist()
        # # print("press: ",curden)
        
        # curden = nc_data.variables["q_value"][:]
        # data["q_value"] = curden.tolist()
        
        # curden = nc_data.variables["rhog_beam"][:]
        # data["rhog_beam"] = curden.tolist()
        
        # print("q_value: ",curden)
        tree = SWTree(name="NetCDF")
        tree.loadFromDict(data)
        return tree
        
    def set_mapper_path(self,mapper_path):
        self.mapper_path = mapper_path