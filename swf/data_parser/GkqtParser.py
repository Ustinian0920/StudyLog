#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# GkqtParser.py
# GKQT物理代码特殊解析器

from .parser import FileDataParser,Mapper
from .swtree import SWTree,SWNode
import os 
from datetime import datetime
import math
import numpy as np
import json
import logging
import yaml
import re
class GkqtParser(FileDataParser):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.keys = []

        
    def write(self,sw_tree):
        ...
    def read(self):
        _,file = os.path.split(self.file_path)
        data = {}
        data_str = ""
        with open(self.file_path,'r') as f:
            data_str = f.read()
        m = re.match(r"(\w+)\s+.*\s+\=.*([\s\-]\d+\.\d+[Ee][\+\-]\d\d)",data_str,re.M|re.S)
        if m:
            key = m.group(1)
            value = m.group(2)
            value = eval(value)
            print("key: ",key," value: ",value)
            data[key] = value
        tree = SWTree(name="gkqt")
        tree.loadFromDict(data)
        return tree
        
    def set_mapper_path(self,mapper_path):
        self.mapper_path = mapper_path