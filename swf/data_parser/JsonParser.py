#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# JsonParser.py
# JSON解析器

from .parser import FileDataParser,Mapper
from .swtree import SWTree,SWNode
import os 
from datetime import datetime
import math
import numpy as np
import json
class JsonParser(FileDataParser):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.keys = []

        
    def write(self,sw_tree):
        ...
    #解析NetCDF 并构建SWTree
    def read(self):
        _,file = os.path.split(self.file_path)
        data = {}
        if os.path.exists(self.file_path):
            with open(self.file_path,'r') as f:
                data = json.load(f)
        tree = SWTree(name="JSON")
        tree.loadFromDict(data)
        return tree
        
    def set_mapper_path(self,mapper_path):
        self.mapper_path = mapper_path