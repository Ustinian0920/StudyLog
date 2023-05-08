
from config import config
import mpld3
import matplotlib.pyplot as plt
import json
import os
import sys
import scipy.io as scio
import random
from io import BytesIO
import base64
import shutil
from sw_viewer_tools import MyEncoder
import numpy
import imas
import re
import cProfile
import numpy as np



# ids对象转为dic字典
def ids_to_dic(node):
	if type(node) in [bool,dict,str,int,float,numpy.ndarray,numpy.float64]:
		return node
	elif type(node) in [list]: 
		l = []
		for n in node:
			l.append(ids_to_dic(n))
		return l
	else:
		dic = node.__dict__
		for k,v in list(dic.items()):
			dic[k] = ids_to_dic(v)
			if k in ["_base_path","_idx","hli_utils"]:
				del dic[k]
		return dic


# 获取节点的描述信息
def get_node_info(ids_path_dic):
    loc = locals()
    json_path = os.path.abspath(os.path.dirname(__file__))+"/input/IDSDef.json"
   
    with open(json_path,"r") as f:
        node_info = json.load(f)
    print(f"dic['data'] = node_info{ids_path_dic}")
    exec(f"dic = node_info{ids_path_dic}")
    dic = loc["dic"]
    
    return dic

# 路径转换
class PathBuilter():
    @classmethod
    def for_data(cls,str_path,index=0):
        if "." in str_path:
            exec_str = cls.built_data_path(str_path,index)
        elif "/" in str_path:
            exec_str = cls.built_coordinate_path_for_dic(str_path,index)
        return exec_str
    @classmethod
    def for_info(cls,str_path):
        if "." in str_path:
            exec_str = cls.built_info_path(str_path=str_path)
        elif "/" in str_path:
            exec_str = cls.built_info(str_path)
        return exec_str
    @classmethod
    def for_ids(cls,str_path,index=0):
        if "." in str_path:
            exec_str = cls.built_ids(str_path,index)
        elif "/" in str_path:
            exec_str = cls.built_coordinate_path(str_path,index)
        return exec_str


    # equilibrium.time_slice.array[0] -> ['equilibrium']['time_slice']
    # 根据路径字符串，构建出节点描述信息的字典取值
    @classmethod
    def built_info_path(self,str_path):
        # str_path = "equilibruim.time_slice.array[0].profiles_1d.psi"
        str_path = str_path.replace(".array[0]","")
        a = str_path.split(".")
        exec_str = ""
        for i in a:
            exec_str += f"['{i}']"
        return exec_str

    # equilibrium.time_slice.array[0] -> ['equilibrium']['time_slice'][0]
    # 根据路径字符串，构建出节点数据的字典取值
    @classmethod
    def built_data_path(self,str_path,index):
        str_path = str_path.replace("array[0]",f"array.{index}")
        a = str_path.split(".")
        exec_str = ""
        for i in a:
            exec_str += f"['{i}']"
        exec_str = exec_str.replace(f"\'{index}\'",f"{index}")
        return exec_str

    # equilibrium/time_slice(item) -> equilibrium.time_slice[0]
    # 根据描述文件的路径字符串，构建出节点数据的取值
    @classmethod
    def built_coordinate_path(self,str_path:str,index):
        str_path = str_path.replace("/",".")
        str_path = str_path.replace("(","[")
        str_path = str_path.replace(")","]")
        str_path = str_path.replace("itime",str(index))
        str_path = re.sub("i\d","0",str_path)
        return str_path

    # equilibrium/time_slice(item) -> ['equilibrium']['time_slice'][0]
    # 根据描述文件的路径字符串，构建出节点信息的取值
    @classmethod
    def built_coordinate_path_for_dic(self,str_path:str,index):
        str_path = str_path.replace(")/","][\'")
        str_path = str_path.replace("(","\'][\'array\'][")
        str_path = str_path.replace("/","\'][\'")
        str_path = str_path.replace("itime",str(index))
        str_path = re.sub("i\d","0",str_path)
        str_path = f"[\'{str_path}\']"
        return str_path

    # equilibrium/time_slice(item) -> ['equilibrium']['time_slice']
    @classmethod
    def built_info(self,str_path):
        str_path = str_path.replace("(itime)","")
        str_path = re.sub("(i\d)","",str_path)
        str_path = str_path.replace("/","\'][\'")
        str_path = f"[\'{str_path}\']"
        return str_path

    # equilibrium.time_slice.array[0] -> equilibrium.time_slice[0]
    @classmethod
    def built_ids(self,str_path:str,index=0):
        str_path = str_path.replace(".array","")
        return str_path

    @classmethod
    def get_time_index(self,str_path:str):
        index = 0
        if "time_slice" in str_path:
            index = re.search("\d",str_path).group()
        return int(index)

def plot_0d(ax:plt.Axes, ids_path:str, root,info_dic:dict,shot,run):
    loc = locals()
    current_time = 0
    exec(f"current_y = root.{PathBuilter.for_ids(ids_path.split('.',1)[1],0)}")
    current_y = loc["current_y"]
    y_lab = f"{info_dic['@name']}({info_dic['@units']})"

    if "time_slice" in ids_path:

        index = PathBuilter.get_time_index(ids_path)
        exec(f"current_y = root.{PathBuilter.for_ids(ids_path.split('.',1)[1],index)}")
        current_y = loc["current_y"]
       
        times = root.time
        current_time = times[index]

        y_list = []
        for i in range(len(times)):
            exec(f"y = root.{PathBuilter.for_ids(ids_path.split('.',1)[1],i)}")
            y = loc["y"]
            y_list.append(y)
        ax.plot(times,y,label=f"shot:{shot} run:{run}")
    
    ax.scatter(current_time,current_y)
    ax.set_ylabel(y_lab)
    ax.set_xlabel("Time(ms)")
    ax.legend()

def plot_1d(ax:plt.Axes, ids_path:str,root,info_dic:dict,shot,run):
    
    loc = locals()

    index = PathBuilter.get_time_index(ids_path)
    coordinate1 = PathBuilter.for_ids(info_dic['@coordinate1'],index)
    y_lab = f'{info_dic["@name"]}({info_dic["@units"]})'

    exec(f"y = root.{PathBuilter.for_ids(ids_path.split('.',1)[1],index)}")
    y = loc["y"]
    if coordinate1=="1...N":
        x = range(1,len(y)+1)
        x_lab = "1...N"
    else:
        exec(f"x = root.{coordinate1}")
        x = loc["x"]
        info_dic = get_node_info(PathBuilter.for_info(ids_path.split(".")[0]+"/"+info_dic['@coordinate1']))
        x_lab = f'{info_dic["@name"]}({info_dic["@units"]})'
    
    ax.set_ylabel(y_lab)
    ax.set_xlabel(x_lab)
   
    ax.plot(x,y,label=f"shot:{shot} run:{run}")
    ax.legend()

def plot_2d(ax:plt.Axes, ids_path,root,info_dic:dict):
    loc = locals()

    index = PathBuilter.get_time_index(ids_path)
    
    exec(f"y = root.{PathBuilter.for_ids(ids_path.split('.',1)[1],index)}")
    y = loc["y"]
    title = info_dic["@name"]
    ax.set_title(title)
    c = ax.imshow(y,cmap=plt.cm.gray)

    vticks = np.linspace(y.min(), y.max(), 5)
    plt.colorbar(mappable=c,ax=ax,ticks=vticks, format='%.3e')


def get_data():
    # 提取数据
 
    # ids_path = sys.argv[1]
    # user = sys.argv[2]
    # db = sys.argv[3]
    # shot = sys.argv[4]
    # run = sys.argv[5]
    # data_list = eval(sys.argv[4])

    width = 12
    # ids_path = "equilibrium.time_slice.array[0].profiles_1d.q"
    _2d_list = ["equilibrium.time_slice.array[0].profiles_2d.array[0].z","equilibrium.time_slice.array[0].profiles_2d.array[0].r","equilibrium.time_slice.array[0].profiles_2d.array[0].psi"]
    _1d_list = ["equilibrium.time_slice.array[0].profiles_1d.pressure","equilibrium.time_slice.array[0].profiles_1d.f","equilibrium.time_slice.array[0].profiles_1d.psi"]
    _0d_list = ["equilibrium.time_slice.array[0].global_quantities.psi_boundary","equilibrium.time_slice.array[0].global_quantities.psi_axis","equilibrium.time_slice.array[0].global_quantities.ip"]
    ids_path_list = _0d_list
    user = "lianke"
    db = "hl2m"
    # shot = 800
    # run = 1
    data_list = [[800,1]]# ,[1000,7],[1578,1]

    file = BytesIO()



    # 根据 绘图数量 计算尺寸
    if (len(ids_path_list)%2)==1:
        row=len(ids_path_list)//2+1
        num=1
    else:
        row=len(ids_path_list)//2
        num=0  
    fig,ax=plt.subplots(row,2,figsize=(width,width*1.5/row),dpi=100)
    
    # 移除多余的子图
    if num:
        if row==1:
            ax[1].remove()
        else:
            ax[row-1,1].remove()
    
    
    # 循环获取到shot和run
    for data in data_list:
        shot = data[0]
        run = data[1]
        root_str = ids_path_list[0].split(".")[0]
        data_entry = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,db,int(shot),int(run),str(user))
        data_entry.open()
        root = data_entry.get(root_str)

        # 循环获取到节点路径
        for i,ids_path in enumerate(ids_path_list):

            info_dic = get_node_info(PathBuilter.for_info(str_path=ids_path))
            data_type = info_dic["@data_type"]

            # 计算出绘图的ax图例
            if (i%2)==1:
                # row
                ro=i//2
                # clomn
                cl=1
            else:
                ro=i//2
                cl=0
            if row==1:
                item=i
            else:
                item=(ro,cl)

            # 根据数据类型绘图
            if data_type=="FLT_0D":
                plot_0d(ax[item],ids_path,root,info_dic,shot,run)
            elif data_type=="FLT_1D":
                plot_1d(ax[item],ids_path,root,info_dic,shot,run)
            elif data_type=="FLT_2D":
                plot_2d(ax[item],ids_path,root,info_dic)
                
    
    # 调整子图之间的间距
    fig.subplots_adjust(hspace=0.3,wspace=0.4)
    # 图像保存到内存，读取为二进制数据，再转换为json字符串
    fig.savefig(file,format="png",bbox_inches = 'tight')
    file.seek(0)
    dic = base64.b64encode(file.read())
    data = {"data":dic}
    data_json_str = json.dumps(data,cls=MyEncoder)
    
    plt.show()
    return data_json_str




if __name__=="__main__":
    
    _0d = "equilibrium.time_slice.array[0].global_quantities.psi_boundary"
    _1d_f = "equilibrium.time_slice.array[0].profiles_1d.pressure"
    _1d_psi = "equilibrium.time_slice.array[0].profiles_1d.psi"
    _2d_r = "equilibrium.time_slice.array[0].profiles_2d.array[0].r"
    _2d_z = "equilibrium.time_slice.array[0].profiles_2d.array[0].z"
    _2d_psi = "equilibrium.time_slice.array[0].profiles_2d.array[0].psi"
    cProfile.run("get_data()",filename="/home/lianke/zoujunwei/ids_tree_viewer/result_ids_plot.out")
    # data_json_str = get_data()
    # print(data_json_str)