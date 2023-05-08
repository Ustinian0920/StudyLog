#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Hdf5Parser.py
# HDF5解析器

from .parser import FileDataParser,Mapper
from .swtree import SWTree,SWNode
import os 
from datetime import datetime
import math
import numpy as np
import json
import h5py
import logging

#hdf5 解析器         
class Hdf5Parser(FileDataParser):
    def __init__(self, file_path):
        super().__init__(file_path)
        
    def write(self,sw_tree):
        ...
    #解析hdf5 并构建SWTree
    def read(self):
        _,file = os.path.split(self.file_path)
        h5 = h5py.File(self.file_path,'r')
        tree = SWTree(name=file.split('.')[0])
        tree.create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        def vist(name,obj):
            name_arr = name.split('/')
            first_name = name_arr[0]
            cur_node = tree.getNode(first_name)
            cur_h5 = h5[first_name]
            if cur_node == None:
               cur_node = SWNode(name=first_name)
               tree.addNode(cur_node)
            for n_i in name_arr[1:]:
                node = cur_node.getNode(n_i)
                if node == None:
                    node = SWNode(name=n_i)
                    cur_node.addNode(node)
                cur_h5 = cur_h5[n_i]
                cur_node = node
            if isinstance(obj, h5py.Dataset):
                cur_node.setData(obj[()].tolist())
                # cur_node.setData([])
                    # node.setData([])
        h5.visititems(vist)
        return tree 

        

    