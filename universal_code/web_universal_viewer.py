import tkinter
from tkinter import ttk
import os
import json
import numpy
import imas
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as ET
import xmltodict
from sw_viewer_tools import MyEncoder
from flask import Flask, request,current_app,jsonify,send_file,Response
from flask_restful import Api, Resource
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity,get_jwt,verify_jwt_in_request
)
from v1base import V1Response
from io import BytesIO
import base64
from util import get_actors,get_sw_path_info
from util.sw_cmd import *

# 获取IDS根节点
class IDSRoot(Resource):
	def __init__(self):
		self.rep = V1Response()

	@jwt_required()
	def post(self):
		data = request.get_data()

		json_path = os.path.abspath(os.path.abspath(os.path.dirname(os.path.dirname(__file__)))+"/../input/IDSDef.json")
		print(json_path)
		with open(json_path,"r") as f:
			dic = json.load(f)
		
		ids_roots = list(dic.keys())

		self.rep.set_data("data",ids_roots)
		return self.rep.get_response()



# 获取单个IDS节点
class IDSNode(Resource):
	def __init__(self):
		self.rep = V1Response()

	@jwt_required()
	def post(self):
		data = request.get_data()
		json_data = json.loads(data)

		ids_root = json_data["ids_root"]
		user = json_data["user"]
		db = json_data["db"]
		shot = json_data["shot"]
		run = json_data["run"]

		dic = sw_get_data_cmd("sw_universal_ids_obj "+ids_root+" "+user+" "+db+" "+str(shot)+" "+str(run))["data"]
		self.rep.set_data("data",dic)
		return self.rep.get_response()


# 获取节点的描述信息
class IDSNodeInfo(Resource):
	def __init__(self):
		self.rep = V1Response()

	@jwt_required()
	def post(self):
		data = request.get_data()
		json_data = json.loads(data)
		loc = locals()
		ids_path = json_data["ids_path"]

		json_path = os.path.abspath(os.path.abspath(os.path.dirname(os.path.dirname(__file__)))+"/../input/IDSDef.json")
		print(json_path)
		with open(json_path,"r") as f:
			node_info = json.load(f)

		exec(f"dic = node_info{built_info_path(ids_path)}")
		dic = loc["dic"]
		self.rep.set_data("data",dic)
		return self.rep.get_response()




class IDSPlot(Resource):
	def __init__(self):
		self.rep = V1Response()

	@jwt_required()
	def post(self):
		data = request.get_data()
		json_data = json.loads(data)

		ids_path = json_data["ids_path"]
		user = json_data["user"]
		db = json_data["db"]
		data_list = json_data[data_list]
		# shot = json_data["shot"]
		# run = json_data["run"]

		dic = sw_get_data_cmd("sw_universal_plot "+ids_path+" "+user+" "+db+" "+"\""+str(data_list).replace(" ","")+"\"")["data"]
		self.rep.set_data("data",dic)
		return self.rep.get_response()
		

class IDSShotRun(Resource):
	def __init__(self):
		self.rep = V1Response()

	@jwt_required()
	def post(self):
		data = request.get_data()
		json_data = json.loads(data)

	
		user = json_data["user"]
		db = json_data["db"]
	
		dic = sw_get_data_cmd("sw_universal_shot_run "+user+" "+db)["data"]
		self.rep.set_data("data",dic)
		return self.rep.get_response()


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

# 根据路径字符串，构建出节点描述信息的字典取值
def built_info_path(str_path):
	# str_path = "equilibruim.time_slice.array[0].profiles_1d.psi"
	str_path = str_path.replace(".array[0]","")
	a = str_path.split(".")
	exec_str = ""
	for i in a:
		exec_str += f"['{i}']"
	return exec_str

# 根据路径字符串，构建出节点数据的字典取值
def built_data_path(str_path,index):
	str_path = str_path.replace("array[0]",f"array.{index}")
	a = str_path.split(".")
	exec_str = ""
	for i in a:
		exec_str += f"['{i}']"
	exec_str = exec_str.replace(f"\'{index}\'",f"{index}")
	return exec_str







	