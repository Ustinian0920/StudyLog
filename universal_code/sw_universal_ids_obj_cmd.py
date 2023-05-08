import imas
import sys
import matplotlib.pyplot as plt
import json
import os
import sys
import scipy.io as scio
import random
from io import BytesIO
import base64
import shutil
from sw_viewer_tools import NpEncoder
import numpy
import cProfile


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

def get_data():

    # ids_root = sys.argv[1]
    # user = sys.argv[2]
    # db = sys.argv[3]
    # shot = sys.argv[4]
    # run = sys.argv[5]

    ids_root = "equilibrium"
    user = "lianke"
    db = "iterdb"
    shot = 100001
    run = 1

    ids = imas.ids(int(shot),int(run))
    ids.open_env(user,db,"3")
    exec(f"ids.{ids_root}.get()")
    loc = locals()

    exec(f"dic = ids_to_dic(ids.{ids_root})")
    dic = loc["dic"]
    print(type(dic))
    data = {"data":dic}
    data_json_str = json.dumps(data,cls=NpEncoder)

    return data_json_str

if __name__=="__main__":
    cProfile.run("get_data()",filename="/home/lianke/zoujunwei/ids_tree_viewer/result_ids_obj.out")
    # data_json_str = get_data()
    # print(data_json_str)