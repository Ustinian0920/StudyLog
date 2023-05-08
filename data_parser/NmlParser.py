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
class NmlParser(FileDataParser):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.keys = []

        
    def write(self,sw_tree):
        ...
    def read(self):
        _,file = os.path.split(self.file_path)
        data = {}
        lines = []
        with open(self.file_path,'r') as f:
            lines = f.readlines()
    
        if self.mapper_path != None:
            if os.path.exists(self.mapper_path):
                with open(self.mapper_path,'r') as f:
                    mapper_data = yaml.safe_load(f)
                    items = mapper_data['items']
                    for i in items:
                        data_path = i['data_path']
                        re_str = f"\s*{data_path}\s*=\s*.*"
                        inx = 0
                        line_len = len(lines)
                        for line in lines:
                            m = re.match(re_str,line)
                            print(m)
                            if m:
                                re_str2 = f"\s*{data_path}\s*="
                                new_line = re.sub(re_str2,"",line)
                                new_line = new_line.strip()
                                
                                arr_re_str = r"(\d+\.*\d+)+"
                                m1 = re.match(arr_re_str,new_line)
                                if m1 :
                                    data_arr = []
                                    arr_line = "["+new_line+"]"
                                    data_arr += eval('[' + re.sub(r'(\d)([ \-]\d\.)', '\\1,\\2', new_line) + ']')
                                    pos = inx+1
                                    while pos < line_len:
                                        l = lines[pos]
                                        print(l)
                                        m2 = re.match(arr_re_str,l)
                                        print(m2)
                                        if m2 == None:
                                            break
                                        if l.find('=') >= 0:
                                            break
                                        data_arr += eval('[' + re.sub(r'(\d)([ \-]\d\.)', '\\1,\\2', new_line) + ']')
                                        pos = pos + 1

                                    print(data_arr) 
                                
                                    exit()
                            inx = inx + 1
       
        
        tree = SWTree(name="nml")
        tree.loadFromDict(data)
        return tree
        
    def set_mapper_path(self,mapper_path):
        self.mapper_path = mapper_path