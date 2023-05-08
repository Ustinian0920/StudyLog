#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# AfileParser.py
# afile解析器


from .parser import FileDataParser,Mapper
import os 
from datetime import datetime
import re 
import math
import numpy as np
import json
from .swtree import SWTree,SWNode
import logging

#AFile解析器
class AfileParser(FileDataParser):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.keys_keys = [
            ["tsaisq","rcencm","bcentr","pasmat"],
            ["cpasma","rout","zout","aout"],
            ["eout","doutu","doutl","vout"],
            ["rcurrt","zcurrt","qsta","betat"],
            ["betap","ali","oleft","origh"],
            ["otop","obott","qpsib","vertn"],
            ["rco2v"],
            ["dco2v"],
            ["rco2r"],
            ["dco2r"],
            ["shearb","bpolav","s1","s2"],
            ["s3","qout","olefs","orighs"],
            ["otops","sibdry","areao","wplasm"],
            ["terror","elongm","qqmagx","cdflux"],
            ["alpha","rttt","psiref","xndnt"],
            ["rseps","zseps","rseps","zseps"],
            ["sepexp","obots","btaxp","btaxv"],
            ["aaq1","aaq2","aaq3","seplim"],
            ["rmagx","zmagx","simagx","taumhd"],
            ["betapd","betatd","wplasmd","fluxx"],
            ["vloopt","taudia","qmerci","tavem"],
            ["nsilop0","magpri0","nfcoil0","nesum0"],
            ["csilop","cmpr2"],
            ["ccbrsp"],
            ["eccurt"],
            ["pbinj","rvsin","zvsin","rvsout"],
            ["zvsout","vsurfa","wpdot","wbdot"],
            ["slantu","slantl","zuperts","chipre"],
            ["cjor95","pp95","ssep","yyy2"],
            ["xnnc","cprof","oring","cjor0"],
            ["fexpan","qqmin","chigamt","ssi01"],
            ["fexpvs","sepnose","ssi95","rqqmin"],
            ["cjor99","cj1ave","rmidin","rmidout"],
            ["psurfa","peak","dminux","dminlx"],
            ["dolubaf","dolubafm","diludom","diludomm"],
            ["ratsol","rvsiu","zvsiu","rvsid"],
            ["zvsid","rvsou","zvsou","rvsod"],
            ["zvsod","xdum","xdum","xdum"],
        ] 
    
    def updateKeys(self,keys_keys):
        self.keys_keys = keys_keys
    
    def write(self,sw_tree):
        ...
    
    def _get_kv_data(self,key):
        value = 0
        if key in self.data:
            value = self.data[key]
        return value
    
    def read(self):
        _,file = os.path.split(self.file_path)
        fmt_file = r'^a(\d+)\.(\d+)'
        fm = re.match(fmt_file, file)
        shot = 0
        if fm:
            shot = fm.group(1)
            time = fm.group(2)
            self.data['shot'] = int(shot)
            self.data['time'] = int(time)
        if not os.path.exists(self.file_path):
            return None
        lines = []
        try:
            lines = open(self.file_path).readlines()
        except Exception as e:
            print(e)
        if not lines or len(lines) == 0:
            print("文件错误")
        fmt_1060 = r'^\s*\*\s*(\d+\.\d+)\s+(\d+)\s+(\d+)\s+([\w]+)\s+(\d+)\s+(\d+)\s([\w ]+)\s+(\d+)\s+(\d+)\s*$'

        fmt_1040 = r'^\s*' + 4*r'([\s\-]\d+\.\d+[Ee][\+\-]\d\d)'
        fmt_1041 = r'^' + 4*r'\s+([ \-]\d+)' 

        counter = 0
        m = None
        #找到 fmt_1060 格式,对应文档中的
        #解析标题 read (neqdsk,1060) time(jj),jflag(jj),lflag,limloc(jj), mco2v,mco2r,qmflag,nlold,nlnew
        while m == None:
            if counter >= len(lines):break
            line = lines[counter]
            # print(line)
            m = re.match(fmt_1060, line)
            # print(m)
            counter += 1
        if m:
            self.data['time'] = float(m.group(1))
            self.data['jflag'] = int(m.group(2))
            self.data['lflag'] = int(m.group(3))
            self.data['limloc'] = m.group(4)
            self.data['mco2v'] = int(m.group(5))
            self.data['mco2r'] = int(m.group(6))
            self.data['qmflag'] = m.group(7).replace(" ", "")
            self.data['nlold'] = int(m.group(8))
            self.data['nlnew'] = int(m.group(9))
        else:
            print(self.file_path)
            raise "数据格式错误"

        # 按照文档给出的矩阵解析 每个字段
        
        for keys in self.keys_keys:
            line = lines[counter]
            
            if len(keys) == 4:
                if keys[0] == 'nsilop0':
                    m1 = re.match(fmt_1041, line)
                    if m1:
                        for index ,key in enumerate(keys):
                            self.data[key] = eval(m1.group(index+1))
                        counter += 1
                else:
                    m = re.match(fmt_1040, line)
                    if m:
                        # print(f"解析 keys: {keys}  line:({counter}) =>  {line.strip()}")
                        for index ,key in enumerate(keys):
                            self.data[key] = eval(m.group(index+1))
                        counter += 1
                    
            
            elif len(keys) == 1:
                if keys[0] == 'rco2v':
                    data_list = []
                    mco2v = self._get_kv_data("mco2v")
                    while len(data_list) < mco2v:
                        #re.sub(r'(^[\s\-]\d+.\d+[Ee][\+\-]\d{2})\s*([\s\-]\d+.\d+[Ee][\+\-]\d{2})\s*([\s\-]\d+.\d+[Ee][\+\-]\d{2})', '\\1,\\2,\\3', line)
                        #line = ' 0.000000000e+00 0.000000000e+00 0.000000000e+00'
                        #提取数组
                        data_list +=  eval('[' + re.sub(r'(\d)\s*([\s\-])\s*(\d)', '\\1, \\2\\3', line) + ']')
                        counter += 1
                    self.data['rco2v'] = data_list
                elif keys[0] == 'dco2v':
                    mco2v = self._get_kv_data("mco2v")
                    # read (neqdsk,1040) (dco2r(k,jj),k=1,mco2r)
                    data_list = []
                    while len(data_list) < mco2v:
                        data_list += eval('[' + re.sub(r'(\d)\s*([\s\-])\s*(\d)', '\\1, \\2\\3', line) + ']')
                        counter += 1
                    self.data['dco2v'] = data_list
                elif keys[0] == 'rco2r':
                    mco2r = self._get_kv_data("mco2r")
                    data_list = []
                    while len(data_list) < mco2r:
                        data_list += eval('[' + re.sub(r'(\d)\s*([\s\-])\s*(\d)', '\\1, \\2\\3', line) + ']')
                        counter += 1
                    self.data['rco2r'] = data_list
                elif keys[0] == 'dco2r':
                    mco2r = self._get_kv_data("mco2r")
                    data_list = []
                    while len(data_list) < mco2r:
                        data_list += eval('[' + re.sub(r'(\d)\s*([\s\-])\s*(\d)', '\\1, \\2\\3', line) + ']')
                        counter += 1
                    self.data['dco2r'] = data_list
                elif keys[0] == 'ccbrsp':
                    n = 0
                    if "nfcoil0" in self.data:
                        n = self.data['nfcoil0']
                    data_list = []
                    while len(data_list) < n:
                        data_list += eval('[' + re.sub(r'(\d)\s*([\s\-])\s*(\d)', '\\1, \\2\\3', line) + ']')
                        counter += 1
                    self.data['ccbrsp'] = data_list
                elif keys[0] == 'eccurt':
                    n = 0
                    if "nesum0" in self.data:
                        n = self.data['nesum0']
                    data_list = []
                    while len(data_list) < n:
                        data_list += eval('[' + re.sub(r'(\d)\s*([\s\-])\s*(\d)', '\\1, \\2\\3', line) + ']')
                        counter += 1
                    self.data['eccurt'] = data_list
                   
            elif len(keys) == 2:
                nsilop0 = 0
                if "nsilop0" in self.data:
                    nsilop0 = self.data['nsilop0']
                
                magpri0 = 0
                if "magpri0" in self.data:
                    magpri0 = self.data['magpri0']
                #这里有两个数组
                data_list = []
                while len(data_list) < nsilop0 + magpri0:
                    data_list += eval('[' + re.sub(r'(\d)\s*([\s\-])\s*(\d)', '\\1, \\2\\3', line) + ']')
                    counter += 1
                self.data['csilop'] = data_list[:nsilop0]
                self.data['cmpr2'] = data_list[magpri0:]
        self.data['time'] = self.data['time']/1000
        tree = SWTree(name=f"afile")
        tree.time_slice = self.data['time']
        tree.shot = self.data['shot']
        tree.create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for key in self.data.keys():
             node = SWNode(name=key,data=self.data[key])
             tree.addNode(node)
        return tree
    
    
    

# class AFile2IDSMapper(Mapper):
#     def __init__(self):
#         self.mapper = {
#         "equilibrium/time[0]":"time",
#         "equilibrium/vacuum_toroidal_field/r0":"rcencm",
#         #"equilibrium/vacuum_toroidal_field/b0(:)":"bcentr",
#         "equilibrium/time_slice(0)/global_quantities/ip": 'pasmat',
#         "equilibrium/time_slice(0)/boundary/outline/r(0)" : 'rout',
#         "equilibrium/time_slice(0)/boundary/outline/z(0)" : 'zout',
#         "equilibrium/time_slice(0)/boundary_separatrix/minor_radius" : 'aout',
#         "equilibrium/time_slice(0)/boundary_separatrix/elongation_upper"    : 'doutu',
#         "equilibrium/time_slice(0)/boundary_separatrix/elongation_lower"    : 'doutl',
#         "equilibrium/time_slice(0)/boundary_separatrix/volume"    : 'vout',
#         "equilibrium/time_slice(0)/global_quantities/beta_tor"    : 'betat',
#         "equilibrium/time_slice(0)/global_quantities/beta_pol"    : 'betap',
#         "equilibrium/time_slice(itime)/global_quantities/li_3" : 'ali',
#         "equilibrium/time_slice(itime)/global_quantities/q_95" : 'qpsib',
#         "equilibrium/time_slice(itime)/global_quantities/psi_boundary" : 'sibdry',
#         "equilibrium/time_slice(itime)/global_quantities/energy_mhd" : 'wplasm',
#         "equilibrium/time_slice(itime)/boundary_separatrix/elongation_lower" : 'elongm',
#         "equilibrium/time_slice(itime)/global_quantities/q_axis" : 'qqmagx',
#         "equilibrium/time_slice(itime)/global_quantities/magnetic_axis/r" : 'rmagx',
#         "equilibrium/time_slice(itime)/global_quantities/magnetic_axis/z" : 'zmagx',
#         "equilibrium/time_slice(itime)/global_quantities/psi_axis" : 'simagx',
#         }
#         self._ids_set = None
    
#     def updateMapper(self,path):
#         with open(path) as f:
#             self.mapper = json.load(f)
#     def setMapper(self,dict_data):
#         self.mapper = dict_data

#     def before_mapping(self):
#         exec_str =''
#         ids_set = self._getIDS_set()
#         for v in ids_set:
#                 exec_str += "data_entry."+v+".ids_properties.homogeneous_time = 1\n"
#                 exec_str += "data_entry."+v+".ids_properties.comment = 'auto putslice'\n"      
#                 exec_str += "data_entry."+v+".time.resize(1)\n" 
#                 exec_str += "data_entry."+v+".put() \n" 
                
#         return exec_str

#     def after_mapping(self):
#         ids_set = self._getIDS_set()
#         exec_str = ""
#         for v in ids_set:
#             kk = "data_entry."+v+".putSlice()\n"
#             exec_str += kk
#         return exec_str
    
#     def _getIDS_set(self):
#         if self._ids_set:
#             return self._ids_set
#         self._ids_set = set()
#         for key,value in self.mapper.items():
#             arr = key.split("/")
#             if len(arr):
#                 ids = arr[0]
#                 self._ids_set.add(ids)
#         return self._ids_set
          
#     def mapping(self,data):
#         data['time'] = data['time']/1000
#         resize_set = set()
#         exec_str =''
#         for key,value in self.mapper.items():
#             value = value.lower()
#             print(f"设置 value:{data[value]} to key:{key}")
#             r_key = re.sub(r'\([\w:]*\)', "[0]", key)
#             r_key = r_key.replace("/", ".")
#             if r_key.find("[0]") >= 0:
#                 arr = r_key.split("[0]")
#                 last = ""
#                 index = 0
#                 for i in arr:
#                     ii = last+i+".resize(1)\n"
#                     if last != "":
#                         last += i+"[0]"
#                         if index == len(arr) -1:
#                             continue
                        
#                     else:
#                         last = i+"[0]"
#                     resize_code = "data_entry."+ii
#                     if resize_code not in resize_set:
#                         resize_set.add(resize_code)
#                         exec_str += resize_code
#                     index += 1
#             if r_key[-3:] == "[0]":
#                 d = data[value]
#                 if isinstance(d,list):
#                     r_key = r_key[:-3]
#                     kk = "data_entry."+ r_key + " = " +"np.array([" +str(d)+"])\n"
#                 else:
#                     kk = "data_entry."+ r_key + " = " + str(d)+"\n"
#                 # print('kkk--------------- ',kk)
#             else:
#                 kk = "data_entry."+ r_key + " = " + str(data[value])+"\n"
#             kk = "data_entry."+ r_key + " = " + str(data[value])+"\n"
#             exec_str += kk
        
#         return exec_str
