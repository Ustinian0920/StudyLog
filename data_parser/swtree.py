
from enum import Enum
import numpy as np
import json
import re 
import logging
import yaml

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

# node节点类型
class SWNodeType(Enum):
    ROOT = "root"
    NODE = "node"
    #存放相同结构数组型子节点
    ARRAY = "array" 
    DATA = "data"

class SWDataType(Enum):
    UNKOWN = "UNKOWN"
    INT_0D = "INT_0D"
    INT_1D = "INT_1D"
    INT_2D = "INT_2D"
    INT_3D = "INT_3D"

    FLT_0D = "FLT_0D"
    FLT_1D = "FLT_1D"
    FLT_2D = "FLT_2D"
    FLT_3D = "FLT_3D"
    FLT_4D = "FLT_4D"
    FLT_5D = "FLT_5D"
    FLT_6D = "FLT_6D"

    STR_0D = "STR_0D"
    STR_1D = "STR_1D"

    CPX_0D = "CPX_0D"
    CPX_1D = "CPX_1D"
    CPX_2D = "CPX_2D"
    BYT_1D = 'BYT_1D'







class SWNode(object):
    '''
    SWTree树型结构的节点抽象,提供各种操作方法
    '''
    def __init__(self,name=None,data=None,node_type=SWNodeType.NODE.value):
        self.data_type = SWDataType.UNKOWN.value
        self.node_type = node_type
        self.name = name
        self._data = None
        self.setData(data)
        self.create_time = ""
        #预留字段存放相同结构 数组型子节点
        self._children = []
        #存放子节点
        self._dict = {}

    #添加子节点方法
    def addNode(self,node,key=None):
        self._assert_is_node(node)
        if key == None:
            key = node.name
        self._dict[key] = node
        # setattr(self, key, node)
    #获取子节点
    def getNode(self,key):
        if key in self._dict.keys():
            return self._dict[key]
        return None
    #设置数据
    @property
    def data(self):
        return self._data
    
    # @data.setter
    def setData(self,data):
        # if data != None:
        #     self.node_type = SWNodeType.DATA
        # setattr(self, "data", data)
        #在设置数据时候自动判断数据类型，还是getDataType方法中自动推断，后期可以看情况处理
        if isinstance(data, list):
            if len(data):
                arr = np.array(data)
                d = arr.ndim
                f = data[0]
                if isinstance(f, int):
                    self.data_type = "INT_{}D".format(d)
                elif isinstance(f, float):
                    self.data_type = "FLT_{}D".format(d)
                elif isinstance(f, str):
                    self.data_type = "STR_{}D".format(d)

        elif isinstance(data, np.ndarray):
            if len(data):
                d = data.ndim
                f = data[0]
                if isinstance(f, int):
                    self.data_type = "INT_{}D".format(d)
                elif isinstance(f, float):
                    self.data_type = "FLT_{}D".format(d)
                elif isinstance(f, str):
                    self.data_type = "STR_{}D".format(d)
        else:
            if isinstance(data, int):
                self.data_type = SWDataType.INT_0D.value
            elif isinstance(data, str):
                self.data_type = SWDataType.STR_0D.value

        self._data = data 
    
    #获取数据
    def getData(self):
        return self._data

    def getDataType(self):
        #TODO 根据self._data自动推断 数据类型
        ...
    
    #把树型结构转换成python字典
    def toDict(self):
        if len(self._dict.keys()) > 0:
            d = {}
            for key in self:
                d[key] = self.getNode(key).toDict()
            return d
        else:
            return self.getData()

    #转换成json
    def toJSON(self):
        return json.dumps(self.toDict(),indent=4)

    #转换成key-value形式，方便后面匹配ids映射表
    def toKeyValueDict(self,last_key,key_value):
        if len(self._dict.keys()) > 0:
            for key in self:
                r_key = last_key +"/" + key
                node = self.getNode(key)
                node.toKeyValueDict(r_key,key_value)
        else:
            key_value[last_key] = self.getData()

    #获取数组类型子节点       
    def getChildren(self):
        return self._children
    
    def __len__(self):
        if self.node_type == SWNodeType.ARRAY.value:
            return len(self._children)
        return len(self._dict)

    def __getitem__(self, key):

        if self.node_type == SWNodeType.ARRAY.value:
            return self._children[key]
        return self.getNode(key)
    
    def __setitem__(self, key, node):
        self._assert_is_node(node)
        self._dict[key] = node

    def __delitem__(self, key):
        del self._dict[key]
    
    # def __set__(self,)
    # def __setattr__(self, attr, value):
    #    if attr == "data":
    #        self._data = value
    #    else:
    #        self._dict[attr] = value

    
    def __getattr__(self, attr):
        if attr == "data":
            return self._data
        return self._dict[attr]
            
        
    def __call__(self):
        return self.getData()
    
    def __iter__(self):
        return iter(self._dict)

    def __repr__(self):
        return ""+self.__class__.__name__ +"."+self.name + " " + str(self._data)
    
    def copy(self):
        return self.__copy__()
    
    def __copy__(self):
        node = SWNode()
        node.name = self.name
        ... 
        return node
    def clear(self):
        self._children.clear()
        self._children = []
        self._dict.clear()
        self._dict = {}
        self._data = None
     
    def _assert_is_node(self, e):
        #判断类型是否正确
        if not isinstance(e, SWNode):
            raise TypeError('expected an Node, not %s' % type(e).__name__)
    
    

class SWTree(SWNode):
    #树型结构的根节点
    def __init__(self,name=None):
        super().__init__(name=name)
        self.node_type = SWNodeType.ROOT.value
        self.time_slice = 0.0
        self.shot = 0
        self.run = 0

    def toDict(self):
        data = {}
        data['create_time'] = self.create_time
        data['name'] = self.name
        data['time_slice'] = self.time_slice
        data['shot'] = self.shot
        data['run'] = self.run
        for key in self:
            node = self[key]
            data[key] = self.getNode(key).toDict()
        return data

    def toKeyValueDict(self):
        key_value = {}
        for key in self:
            node = self.getNode(key)
            node.toKeyValueDict(key,key_value)
        return key_value

    def save(self,path):
        json_str = self.toJSON()
        with open(path,'w') as f:
            f.write(json_str)
        
        
    def loadFromPath(self,path):
        with open(path,'r') as f:
            data = json.load(f)
            self.loadFromDict(data)
    
    def extendFromDict(self,data):
        self.loadFromDict(data,extend=True)
        
    
    def loadFromDict(self,data,extend=False):
        if not extend :
            self.clear()
        if 'create_time' in data.keys():
            self.create_time = data['create_time']
        if 'name' in data.keys():
            self.create_time = data['name']
        if 'time_slice' in data.keys():
            self.create_time = data['time_slice']
        if 'shot' in data.keys():
            self.create_time = data['shot']
        if 'run' in data.keys():
            self.create_time = data['run']
            
            
        def visit(name,obj):
            name_arr = name.split('/')
            first_name = name_arr[0]
            cur_node = self.getNode(first_name)
            cur_data = data[first_name]
            if cur_node == None:
               cur_node = SWNode(name=first_name)
               self.addNode(cur_node)
            for n_i in name_arr[1:]:
                node = cur_node.getNode(n_i)
                if node == None:
                    node = SWNode(name=n_i)
                    cur_node.addNode(node)
                cur_data = cur_data[n_i]
                cur_node = node
            if not isinstance(obj, dict):
                cur_node.setData(obj)
        self._foreach("",data,visit)
    
        
    def foreach(self,func=None):
        data = self.toDict()
        self._foreach('',data,func)
    
    
    def _foreach(self,init_key="",data=None,func=None):
        if isinstance(data, dict):
            for key ,value in data.items():
                full_key = init_key+"/"+key
                if init_key == None or init_key == "":
                    full_key = key 
                r = func(full_key,value)
                if r :
                    break
                if isinstance(value, dict):
                    self._foreach(full_key,value,func)
        
    def delete(self,path):
        def visit(key,value):
            if path == key:
                arr = path.split('/')
                first_key = arr[0]
                last_key = first_key
                cur_node = self.getNode(first_key)
                last_node = cur_node
                left_arr = arr[1:]
                while len(left_arr) > 0 and cur_node != None:
                    key = left_arr[0]
                    last_key = key
                    last_node = cur_node
                    cur_node = cur_node.getNode(key)
                    left_arr = left_arr[1:]
                del last_node[last_key]
                return True
            return False
        self.foreach(visit)

    def __repr__(self):
        return self.toJSON()


class SWMapper():

    def __init__(self):
        self._mapper = {}
        self._ids_set = None
    
    def getMapper():
        return self._mapper
        
    def updateMapperDict(self,dictObj):
        self._ids_set = None
        self._mapper = dictObj
    
    def updateMapperJSONFile(self,json_path):
        self._ids_set = None
        with open(json_path,'r') as f:
            obj = json.load(f)
            self._mapper = obj
    
    def updateMapperYAMLFile(self,yaml_path):
        #todo
        self._ids_set = None
        with open(yaml_path,'r') as f:
            obj = yaml.safe_load(f)
            self._mapper = obj
    
    def open_env(self,database,shot,run):
        exec_str = "import imas\n"
        exec_str += "import numpy as np\n"
        exec_str += "import os\n\n"
        exec_str += f"data_entry = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'{database}',{shot},{run},os.environ.get('USER'))\n"
        # exec_str += "s1,s2 =  data_entry.open()\n"
        # exec_str += "if s1 < 0:\n"
        # exec_str += "\tdata_entry.create()\n"
        exec_str += "data_entry.create()\n"
        return exec_str

    def close(self):
        exec_str = "data_entry.close()\n"
        return exec_str

    def ids_reflect_mapping(self,database,shot,run,time_slice):
        tree = SWTree(name="ids")
        tree.time_slice = time_slice
        tree.shot = shot
        tree.run = run
        data = {
            "name":"ids",
            "time_slice":time_slice,
            "shot":shot,
            "run":run,
        }
        c_str = ""
        import imas 
        import numpy as np
        import os 
        data_entry = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,database,shot,run,os.environ.get('USER'))
        s1,s2 =  data_entry.open()
        if s1 >= 0:
            time_slice = time_slice / 1000.0
            exec_str = ""
            ids_set = self.getIDSSet()
            for i,ids_name in enumerate(ids_set):
                # exec_str += f"{ids_name} = data_entry.get_slice('{ids_name}',{time_slice},imas.imasdef.LINEAR_INTERP)\n"
                exec_str += f"{ids_name} = data_entry.get('{ids_name}')\n"
                exec_str += f"c_str = {ids_name}.ids_properties.comment\n"
                if i==0:
                    time_list = list(data_entry.get(ids_name).time)
                    index = time_list.index(time_slice)
            items = self._mapper['items']
            for item in items:
                ids_path = item['ids_path']
                data_path = item['data_path']
                data_type = item['data_type']
                # print(f"从ids:{ids_path} => 获取数据到{data_path}")
                r_key = re.sub(r'\([\w:,]*\)', "[0]", ids_path)
                r_key = r_key.replace("/", ".")
                if r_key[-3:] == "[0]":
                    r_key = r_key[:-3]
                r_key = r_key.replace("time_slice[0]","time_slice[index]")
                exec_str += f"data['{data_path}'] = {r_key}\n"
                
            exec(exec_str)
            if c_str != "":
                c_items = c_str.split(";")
                for item in c_items:
                    if item != "":
                        m = re.match(r"(\w+)\=\(\w+)", item)
                        if m:
                            key = m.group(1)
                            value = m.group(2)
                            data[key]=value
            
        tree.loadFromDict(data)    
        return tree
    
    def to_ids(self,sw_tree,last_ids_dict=None):
        # if self.type == "gfile":
        #     print(last_ids_dict)
        #     equilibrium = last_ids_dict['equilibrium']
        #     print(equilibrium.time_slice[0].global_quantities.volume)
        #     exit()
        
        key_value_data = sw_tree.toKeyValueDict()
        time_slice = sw_tree.time_slice
        time_slice = time_slice / 1000.0
        ids_dict = {}
        if last_ids_dict :
            ids_dict = last_ids_dict
            
        ids_set = self.getIDSSet()
        resize_set = set()
        exec_str = ""
        for ids_name in ids_set:
            
            if ids_name not in ids_dict:
                ids = eval(f"imas.{ids_name}()")
                # if self.type == "gfile":
                #     print(ids_dict)
                #     equilibrium = ids_dict['equilibrium']
                #     print(equilibrium.time_slice[0].global_quantities.volume)
                #     print(ids_name)
                #     print(ids_dict.keys())
                #     if ids_name not in ids_dict:
                #         print("ids_name in")
                #     exit()
                ids_dict[ids_name] = ids
                ids.time.resize(1)
                ids.time[0] = time_slice
                ids.ids_properties.homogeneous_time = 1
            exec_str += "{} = ids_dict['{}']\n".format(ids_name,ids_name)
        
        items = []
        if 'items'  in self._mapper:
            items = self._mapper['items']
        for item in items:
            kk = ""
            ids_path = item['ids_path']
            data_path = item['data_path']
            data_type = item['data_type']
            dim = 0
            m = re.match(r"^\w+(\d)D$", data_type)
            if m :
                dim = m.group(1)
            dim = int(dim)
            # print(f"设置数据:{data_path} => ids: {ids_path}")
            r_key = re.sub(r'\([\w:,]*\)', "[0]", ids_path)
            r_key = r_key.replace("/", ".")
            if data_path not in key_value_data.keys():
                continue
            if r_key.find("[0]") >= 0:
                arr = r_key.split("[0]")
                last = ""
                index = 0
                for i in arr:
                    ii = last+i+".resize(1)\n"
                    if last != "":
                        last += i+"[0]"
                        if index == len(arr) -1:
                            continue
                    else:
                        last = i+"[0]"
                    resize_code = ""+ii
                    if resize_code not in resize_set:
                        resize_set.add(resize_code)
                        tmp_code  = resize_code.replace(".resize(1)","").replace("\n","")
                        code = f"if len({tmp_code}) < 1:"+resize_code
                        exec_str += code
                    index += 1
            if r_key[-3:] == "[0]":
                if data_path not in key_value_data.keys():
                    continue
                d = key_value_data[data_path]
                if isinstance(d,list):
                    r_key = r_key[:-3]
                    if data_type == "UNKOWN":
                        kk = ""+ r_key + " = " +"np.array(" +str(d)+")\n"
                    else: 
                        n_list = np.array(d)
                        if dim != n_list.ndim:
                            if n_list.ndim - dim == 1:
                                n_d = d[0]
                                kk = ""+ r_key + " = " +"np.array(" +str(n_d)+")\n"
                            elif n_list.ndim - dim == 2:
                                n_d = d[0][0]
                                kk = ""+ r_key + " = " +"np.array(" +str(n_d)+")\n"
                            elif n_list.ndim - dim == -1:
                                n_d = []
                                n_d.append(d)
                                kk = ""+ r_key + " = " +"np.array(" +str(n_d)+")\n"
                            else:
                                kk = ""+ r_key + " = " +"np.array(" +str(d)+")\n"
                        else:
                            kk = ""+ r_key + " = " +"np.array(" +str(d)+")\n"
                        # if dim < n_list.ndim-1:
                        #     if len(d) > 0:
                        #         n_d = d[0]
                        #         kk = ""+ r_key + " = " +"np.array(" +str(n_d)+")\n"
                        # else:
                        #     kk = ""+ r_key + " = " +"np.array(" +str(d)+")\n"
                else:
                    kk = ""+ r_key + " = " + str(d)+"\n"
            else:
                kk = ""+ r_key + " = " + str(key_value_data[data_path])+"\n"
            exec_str += kk
        exec(exec_str)
        return ids_dict
    
    def to_ids_from_xml(self,xml,last_ids_dict=None):
        ids_dict = {}
        if last_ids_dict != None:
            ids_dict = last_ids_dict
        ids_set = self.getIDSSet()
        resize_set = set()
        exec_str = ""
        for ids_name in ids_set:
            if ids_name not in ids_dict.keys():
                ids = eval(f"imas.{ids_name}()")
                ids_dict[ids_name] = ids
                ids.time.resize(1)
                ids.ids_properties.homogeneous_time = 1
            exec_str += "{} = ids_dict['{}']\n".format(ids_name,ids_name)
            
        items = self._mapper['items']
        for item in items:
            kk = ""
            ids_path = item['ids_path']
            data_path = item['data_path']
            data_type = item['data_type']
            dim = 0
            m = re.match(r"^\w+(\d)D$", data_type)
            if m :
                dim = m.group(1)
            dim = int(dim)
            r_key = re.sub(r'\([\w:,]*\)', "[0]", ids_path)
            r_key = r_key.replace("/", ".")
            xml_ele = xml.find("./"+data_path)
            
            if xml_ele == None:
                continue
            d = xml_ele.text 
            # print(f"设置数据:{data_path} => ids: {ids_path} = {d}")

            if r_key.find("[0]") >= 0:
                arr = r_key.split("[0]")
                last = ""
                index = 0
                for i in arr:
                    ii = last+i+".resize(1)\n"
                    if last != "":
                        last += i+"[0]"
                        if index == len(arr) -1:
                            continue
                    else:
                        last = i+"[0]"
                    resize_code = ""+ii
                    if resize_code not in resize_set:
                        resize_set.add(resize_code)
                        exec_str += resize_code
                    index += 1
            if r_key[-3:] == "[0]":
                
                if isinstance(d,list):
                    r_key = r_key[:-3]
                    if data_type == "UNKOWN":
                        kk = ""+ r_key + " = " +"np.array(" +str(d)+")\n"
                    else: 
                        n_list = np.array(d)
                        if dim < n_list.ndim-1:
                            if len(d) > 0:
                                n_d = d[0]
                                kk = ""+ r_key + " = " +"np.array(" +str(n_d)+")\n"
                        else:
                            kk = ""+ r_key + " = " +"np.array(" +str(d)+")\n"
                else:
                    kk = ""+ r_key + " = " + str(d)+"\n"
            else:
                kk = ""+ r_key + " = " + str(d)+"\n"
            exec_str += kk
        print(exec_str)
        exec(exec_str)
        return ids_dict
        
    def to_ids_from_data(self,key_value_data,last_ids_dict):
        
        key_value_data = sw_tree.toKeyValueDict()
        time_slice = sw_tree.time_slice
        time_slice = time_slice / 1000.0
        ids_dict = {}
        if last_ids_dict != None:
            ids_dict = last_ids_dict
        ids_set = self.getIDSSet()
        resize_set = set()
        exec_str = ""
        for ids_name in ids_set:
            if ids_name not in ids_dict.keys():
                ids = eval(f"imas.{ids_name}()")
                ids_dict[ids_name] = ids
            ids.time.resize(1)
            ids.time[0] = time_slice
            ids.ids_properties.homogeneous_time = 1
            exec_str += "{} = ids_dict['{}']\n".format(ids_name,ids_name)
            
        items = self._mapper['items']
        for item in items:
            kk = ""
            ids_path = item['ids_path']
            data_path = item['data_path']
            data_type = item['data_type']
            dim = 0
            m = re.match(r"^\w+(\d)D$", data_type)
            if m :
                dim = m.group(1)
            dim = int(dim)
            # print(f"设置数据:{data_path} => ids: {ids_path}")
            r_key = re.sub(r'\([\w:,]*\)', "[0]", ids_path)
            r_key = r_key.replace("/", ".")
            
            if r_key.find("[0]") >= 0:
                arr = r_key.split("[0]")
                last = ""
                index = 0
                for i in arr:
                    ii = last+i+".resize(1)\n"
                    if last != "":
                        last += i+"[0]"
                        if index == len(arr) -1:
                            continue
                    else:
                        last = i+"[0]"
                    resize_code = ""+ii
                    if resize_code not in resize_set:
                        resize_set.add(resize_code)
                        exec_str += resize_code
                    index += 1
            if r_key[-3:] == "[0]":
                if data_path not in key_value_data.keys():
                    continue
                d = key_value_data[data_path]
                if isinstance(d,list):
                    r_key = r_key[:-3]
                    if data_type == "UNKOWN":
                        kk = ""+ r_key + " = " +"np.array(" +str(d)+")\n"
                    else: 
                        n_list = np.array(d)
                        if dim < n_list.ndim-1:
                            if len(d) > 0:
                                n_d = d[0]
                                kk = ""+ r_key + " = " +"np.array(" +str(n_d)+")\n"
                        else:
                            kk = ""+ r_key + " = " +"np.array(" +str(d)+")\n"
                else:
                    kk = ""+ r_key + " = " + str(d)+"\n"
            else:
                kk = ""+ r_key + " = " + str(key_value_data[data_path])+"\n"
            exec_str += kk
        exec(exec_str)
        return ids_dict
        
        
            
    def mapping(self,sw_tree,skip_init_ids=[]):
        key_value_data = sw_tree.toKeyValueDict()
        name = self._mapper['name']
        # print(f"映射{name} 到 ids ")
        # print("映射关系如下:")
        # print(self._mapper)
        c_str = "";
        if 'control' in self._mapper:
            control = self._mapper['control']
            c_items = control.split(";")
            
            for item in c_items:
                if item != "":
                    m = re.match(r"(\w+)\=\{\}", item)
                    if m:
                        key = m.group(1)
                        v = key_value_data[key]
                        c_str += f"{key}={v};"
        time_slice = sw_tree.time_slice
        time_slice = time_slice / 1000.0
        exec_str = "\n";
        ids_set = self.getIDSSet()
        # before
        for v in ids_set:
            if v in skip_init_ids:
                continue
            exec_str += f"{v} = data_entry.get('{v}')\n"
            exec_str += f"{v}.ids_properties.homogeneous_time = 1\n"
            exec_str += f"{v}.ids_properties.comment = '{c_str}'\n"
            exec_str += f"if len({v}.time) == 0:"   
            exec_str += f"\t{v}.time.resize(1)\n" 
            # exec_str += f"data_entry.put({v}) \n" 
            exec_str += f"{v}.time[0] = {time_slice}\n"

        # set data
        resize_set = set()
       
        items = self._mapper['items']
        for item in items:
            kk = ""
            ids_path = item['ids_path']
            data_path = item['data_path']
            data_type = item['data_type']
            dim = 0
            m = re.match(r"^\w+(\d)D$", data_type)
            if m :
                dim = m.group(1)
            dim = int(dim)
            # print(f"设置数据:{data_path} => ids: {ids_path}")
            r_key = re.sub(r'\([\w:,]*\)', "[0]", ids_path)
            r_key = r_key.replace("/", ".")
            
            if r_key.find("[0]") >= 0:
                arr = r_key.split("[0]")
                last = ""
                index = 0
                for i in arr:
                    ii = last+i+".resize(1)\n"
                    if last != "":
                        last += i+"[0]"
                        if index == len(arr) -1:
                            continue
                    else:
                        last = i+"[0]"
                    resize_code = ""+ii
                    if resize_code not in resize_set:
                        resize_set.add(resize_code)
                        exec_str += resize_code
                    index += 1
            if r_key[-3:] == "[0]":
                if data_path not in key_value_data.keys():
                    continue
                d = key_value_data[data_path]
                if isinstance(d,list):
                    r_key = r_key[:-3]
                    if data_type == "UNKOWN":
                        kk = ""+ r_key + " = " +"np.array(" +str(d)+")\n"
                    else: 
                        n_list = np.array(d)
                        if dim < n_list.ndim-1:
                            if len(d) > 0:
                                n_d = d[0]
                                kk = ""+ r_key + " = " +"np.array(" +str(n_d)+")\n"
                        else:
                            kk = ""+ r_key + " = " +"np.array(" +str(d)+")\n"
                else:
                    kk = ""+ r_key + " = " + str(d)+"\n"
            else:
                kk = ""+ r_key + " = " + str(key_value_data[data_path])+"\n"
            exec_str += kk

        
        exec_str += "\n"
        for v in ids_set:
            exec_str += f"data_entry.put_slice({v})\n"
        #end

        return exec_str

    #获取配置表中IDS的集合，比如 amns_data，equilibrium
    def getIDSSet(self):
        if self._ids_set:
            return self._ids_set
        self._ids_set = set()
        if "items" in self._mapper:
            items = self._mapper['items']
            for item in items:
                ids_path = item['ids_path']
                arr = ids_path.split('/')
                if len(arr):
                    ids = arr[0]
                    self._ids_set.add(ids)
        return self._ids_set



if __name__ == "__main__":
    import argparse
    import os
    import sys 
    base_dir = os.path.dirname( os.path.realpath(__file__))
    sys.path.append(os.path.dirname(base_dir))

    from data_parser import AfileParser
    from data_parser import GfileParser
    from data_parser import Hdf5Parser
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-in_file',help='指定待解析的输入文件',default='')
    parser.add_argument('-in_type',help='指定输入文件的类型',default='gfile')
    parser.add_argument('-out_file',help='指定输出文件',default='')
    parser.add_argument('-out_type',help='指定输出文件类型',default='json')
    args = parser.parse_args()
    
    in_file = args.in_file
    in_type = args.in_type
    out_file = args.out_file
    out_type = args.out_type
    if in_file == None or in_file == "":
        print(f"{in_file} 输入文件不存在")
        exit(1)
    if not os.path.exists(in_file):
        print(f"{in_file} 输入文件不存在")
        exit(1)   
    parser = None
    tree = None
    if in_type == "gfile":
        parser = GfileParser(in_file)
        tree =  parser.read()
    elif in_type == "afile":
        parser = AfileParser(in_file)
        tree =  parser.read()
    elif in_type == "h5":
        parser = Hdf5Parser(in_file)
        tree =  parser.read()
    
    if tree:
        print(tree)
    if out_file != "":
        if not tree:
            print("解析错误...")
        else:
            tree.save(out_file)

"""
 alias sw_tree="python3 /home/lianke/houfeng/code/framework/data_parser/swtree.py"

 cd /home/lianke/houfeng/code/framework/test_data

 python3 /home/lianke/houfeng/code/framework/data_parser/swtree.py -in_file a004001.00220 -in_type afile 


sw_tree -in_file a004001.00220 -in_type afile -out_file a004001_test.json
sw_tree -in_file actsim_out.h5 -in_type h5 -out_file h5test.json
"""