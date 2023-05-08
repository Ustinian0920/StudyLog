
from datetime import (timedelta, datetime)
import json
import os

# from v1base import V1Response
# from util.sw_cmd import *
# from util.tools import random_num_str
# from util.sw_path import *


# from util import get_actors,get_sw_path_info
import shutil
import xml
import xml.etree.ElementTree as ET
import re
import yaml
import numpy as np
import math
import matplotlib.pyplot as plt

import imageio
import mpld3
from scipy import interpolate
import imas
from multiprocessing import Pool
import sys
import getpass
import glob
import h5py
from scipy.fft import fft, fftshift, fftfreq
import pathlib
from mpld3 import plugins
from matplotlib import font_manager
from pathlib import Path

# 权限设置
use_all_sudo = False 

pi = math.pi
# 颜色列表
color=['dodgerblue','darkorange','black','darkviolet','olivedrab','hotpink','red','violet','darkgreen','deeppink']

# 默认绘图尺寸
fig_size = (12.06,7.11)


#--------------------------HL-2M大屏绘图--------------------------------
base=os.path.dirname(os.path.realpath(__file__))
digifaw_font_path = base+"/input/digifaw.ttf"
tnr_font_path = base+"/input/Times-New-Roman1.ttf"


# 绘制装置图，包括第一壁，边界TF，三角形遮罩
def screen_Draw_2M_stru_bg(ax1,R_Z={}):
    # 线条透明度
    alpha = 0.9
    # y轴label的字体大小
    font_size = 18
    # xy轴刻度值的字体大小
    tick_size = 12
    
 
    ## 第一壁 ##
    R_fw_up   =   [ 1.9666 , 1.7612 , 1.6937,  1.6928  , 1.6252 ,   1.6243  ,  1.5568 ,   1.5559 ,   1.4872  ,  1.4862  ,  1.4106 ,   1.4096  ,  1.3334 ,
                    1.3325 , 1.2641 , 1.2634 , 1.2103 ,  1.2099  ,  1.1779   , 1.1778  ,  1.1700   , 1.1700  ,  1.1700  ,  1.1700  ,  1.1700  ,   1.1700  ,  1.1700  ,  1.0950 ,  ]
    Z_fw_up   =   [ 0.9697  ,1.0832 , 1.1201 , 1.1206  , 1.1575  ,  1.1580   , 1.1949 ,   1.1953   , 1.2302  ,  1.2303  ,  1.2449  ,  1.2448  ,  1.2338  ,
                    1.2334 , 1.1981  ,1.1973 , 1.1416  , 1.1407  ,  1.0706 ,   1.0696   , 0.9930   , 0.9920  ,  0.9150  ,  0.9140  ,  0.8370  ,  0.8350  ,  0.8100  ,  0.810 ]
    ax1.plot(R_fw_up,Z_fw_up,'#eda3ff',alpha=alpha,zorder=2)
    R_fwi   =   [ 1.145  ,  1.105  , 1.105  ,  1.105  ]
    Z_fwi   =   [-0.802,   -0.800  ,   0    ,  0.800  ]
    ax1.plot(R_fwi,Z_fwi,'#eda3ff',alpha=alpha,zorder=2)
    R_fwo = [ 1.91   , 1.9666  ,  2.0809  ,  2.0818 ,   2.1523  ,  2.1530 ,   2.2345   , 2.2351  ,  2.2973    ,2.2978  ,  2.3605   , 2.3609  ,  2.4012 ,
        2.4015  ,  2.4417  ,  2.4423  ,  2.4847  ,  2.4850 ,   2.4850   , 2.4850  ,  2.4850  ,  2.4850  ,  2.4850  ,  2.4847  ,  2.4423  ,
        2.4417  , 2.4015  ,  2.4012,    2.3609  ,  2.3605 ,   2.2978   , 2.2973  ,  2.2351  ,  2.2345   , 2.1530   , 2.1523  ,  2.0818  ,  2.0809  ,  1.9666   
        ]
    Z_fwo = [ -1.01 ,  -0.9697  , -0.9089 ,  -0.9083 ,  -0.8541  , -0.8534 ,  -0.7521  , -0.7513 ,  -0.6383  , -0.6374 ,  -0.5236 ,   -0.5227  , -0.3991  , 
        -0.3981 , -0.2750  , -0.2730 ,  -0.1429 ,  -0.1413 ,  -0.0540 ,  -0.0530   , 0.0530  ,  0.0540  ,  0.1413 ,   0.1429  ,  0.2730 ,   
        0.2750 ,   0.3981  ,  0.3991 ,   0.5227  ,  0.5236 ,   0.6374  ,  0.6383  ,  0.7513   , 0.7521 ,   0.8534  ,  0.8541  ,  0.9083 ,   0.9089,   0.9697 ]
    ax1.plot(R_fwo,Z_fwo,'#eda3ff',alpha=alpha,zorder=2)
    R_inner_p_new = [ 1.098  ,  1.145  , 1.1666 ,  1.2066 ,  1.2099,   1.1783    ]
    Z_inner_p_new = [ -0.802 , -0.802 , -0.8145  ,-0.8837  ,-0.8984 ,  -1.259  ]
    ax1.plot(R_inner_p_new,Z_inner_p_new,'#eda3ff',alpha=alpha,zorder=2)
    R_dome_new    = [ 1.1947 , 1.2019  ,  1.2871   , 1.302  , 1.3579  ,1.3729 , 1.3886 , 1.5536 , 1.5559  ]
    Z_dome_new    = [-1.2468 ,-1.2447 ,  -1.317 ,  -1.326  , -1.3477,-1.352 , -1.3535 , -1.3535  ,-1.3615 ]
    ax1.plot(R_dome_new,Z_dome_new,'#eda3ff',alpha=alpha,zorder=2)
    R_outer_p_new = [ 1.5546 ,  1.5714 , 1.6134 ,  1.6168  , 1.584  ,  1.581  ,  1.590, 1.6225  , 1.6355 ,   1.6528  , 1.7234  , 1.91]
    Z_outer_p_new = [-1.3845 , -1.3765 ,-1.3765 , -1.3709 , -1.2701 , -1.2398, -1.2156, -1.1647 , -1.1488  , -1.1364  ,-1.0989 , -1.01]
    ax1.plot(R_outer_p_new,Z_outer_p_new,'#eda3ff',alpha=alpha,zorder=2)


    
    ## 边界 TF ##
    R_inner = R_Z["R_inner1"]
    Z_inner = R_Z["Z_inner1"]
    R_outer = R_Z["R_outer1"]
    Z_outer = R_Z["Z_outer1"]
    ax1.plot(R_inner,Z_inner,'#9ce3f7',R_outer,Z_outer,'#9ce3f7')##### 内双圈
    R_inner = R_Z["R_inner2"]
    Z_inner = R_Z["Z_inner2"]
    R_outer = R_Z["R_outer2"]
    Z_outer = R_Z["Z_outer2"]
    ax1.plot(R_inner,Z_inner,'#c2d1d2',R_outer,Z_outer,'#c2d1d2',alpha=alpha-0.2,zorder=2)##### 外双圈
    ax1.fill(R_inner,Z_inner,facecolor='#000105',zorder=1)
    ax1.fill(R_outer,Z_outer,facecolor='#c2d1d2',alpha=alpha-0.5,zorder=0.9)
    
    
    ## 三角形遮罩 ##
    bottom_triangle_x = [2.45,2.7,2.69,2.57]
    bottom_triangle_y = [-1.64,-1.3,-1.62,-1.75]
    ax1.plot(bottom_triangle_x,bottom_triangle_y,'#4d5456',zorder=3)
    ax1.fill(bottom_triangle_x,bottom_triangle_y,facecolor='#4d5456',zorder=3)
    top_triangle_x = [2.45,2.7,2.69,2.57]
    top_triangle_y = [1.64,1.3,1.62,1.75]
    ax1.plot(top_triangle_x,top_triangle_y,'#4d5456',zorder=3)
    ax1.fill(top_triangle_x,top_triangle_y,facecolor='#4d5456',zorder=3)
    ax1.set_yticklabels([-2,-2,-1,0,1,2],fontsize=tick_size)
    ax1.set_xticklabels([0.5,0.5,1.0,1.5,2.0,2.5,3.0],fontsize=tick_size)
    ax1.set_xlabel('R(m)',font=Path(tnr_font_path), fontsize=font_size-2,color="white")
    ax1.set_ylabel('Z(m)',font=Path(tnr_font_path), fontsize=font_size-2,color="white")
    
    return ax1
# 绘制装置图，包括cs线圈，pf线圈
def screen_Draw_2M_stru_color_block(ax1,color_list=[]):
    # 透明度
    alpha = 0.9
    b_list = []




    ## 欧姆线圈 E （cs线圈） ##
    def rect_E(r,z,w,h):  
            r1=r-w/2
            r2=r+w/2
            z1=z-h/2
            z2=z+h/2
            R=[r1,r2,r2,r1]   # R=[r1,r2,r2,r1,r1,r2,r1,r2]   
            Z=[z1,z1,z2,z2]   # Z=[z1,z1,z2,z2,z1,z2,z2,z1]
            b = ax1.plot(R,Z,color_list[8],alpha=alpha,linewidth =0.8,zorder=2)##### 4
            b_list.append(b)
            b = ax1.fill(R,Z,facecolor=color_list[8],zorder=2)
            b_list.append(b)
            
    r=[0.748]
    z=[0,-0.887]
    w=[0.117,0.117]
    h=[3.548,1.774]
    for i in range(len(r)):
        rect_E(r[i],z[i],w[i],h[i])
    
    
    
    
    
    
    ## 极向场线圈（pf线圈） ##
    def rect_F(r,z,w,h,a):
        if a==0:
            r1=r-w/2
            r2=r+w/2
            z1=z-h/2
            z2=z+h/2

            R=[r1,r2,r2,r1]   # R=[r1,r2,r2,r1,r1,r2,r1,r2]
            Z=[z1,z1,z2,z2]   # Z=[z1,z1,z2,z2,z1,z2,z2,z1]
        else:
            r1=r-(w/2+h/2/math.tan(a))
            r2=r+(w/2-h/2/math.tan(a))
            r3=r+(w/2+h/2/math.tan(a))
            r4=r-(w/2-h/2/math.tan(a))

            z1=z-h/2
            z2=z+h/2
            R=[r1,r2,r3,r4] # R=[r1,r2,r3,r4,r1,r3,r4,r2]
            Z=[z1,z1,z2,z2] # Z=[z1,z1,z2,z2,z1,z2,z2,z1]

        # 5U
        if Z==[1.6415, 1.6415, 1.8644999999999998, 1.8644999999999998]:
            b = ax1.plot(R,Z,color_list[4],alpha=alpha,linewidth = 0.1,zorder=2)##### 5 linewidths=0.8
            b_list.append(b)
            b = ax1.fill(R,Z,facecolor=color_list[4],zorder=2)
            b_list.append(b)
        # 6U
        elif Z==[1.7155, 1.7155, 1.8645, 1.8645]:
            b = ax1.plot(R,Z,color_list[5],alpha=alpha,linewidth = 0.1,zorder=2)##### 5 linewidths=0.8
            b_list.append(b)
            b = ax1.fill(R,Z,facecolor=color_list[5],zorder=2)
            b_list.append(b)
        # 7U
        elif Z==[1.0885, 1.0885, 1.3114999999999999, 1.3114999999999999]:
            b = ax1.plot(R,Z,color_list[6],alpha=alpha,linewidth = 0.1,zorder=2)##### 5 linewidths=0.8
            b_list.append(b)
            b = ax1.fill(R,Z,facecolor=color_list[6],zorder=2)
            b_list.append(b)
        # 8U
        elif Z==[0.3685, 0.3685, 0.5915, 0.5915]:
            b = ax1.plot(R,Z,color_list[7],alpha=alpha,linewidth = 0.1,zorder=2)##### 5 linewidths=0.8
            b_list.append(b)
            b = ax1.fill(R,Z,facecolor=color_list[7],zorder=2)
            b_list.append(b)
        # 8L
        elif Z==[-0.5915, -0.5915, -0.3685, -0.3685]:
            b = ax1.plot(R,Z,color_list[7],alpha=alpha,linewidth = 0.1,zorder=2)##### 5 linewidths=0.8
            b_list.append(b)
            b = ax1.fill(R,Z,facecolor=color_list[7],zorder=2)
            b_list.append(b)
        # 7L
        elif Z==[-1.3114999999999999, -1.3114999999999999, -1.0885, -1.0885]:
            b = ax1.plot(R,Z,color_list[6],alpha=alpha,linewidth = 0.1,zorder=2)##### 5 linewidths=0.8
            b_list.append(b)
            b = ax1.fill(R,Z,facecolor=color_list[6],zorder=2)
            b_list.append(b)
          
        # 6L
        elif Z==[-1.8645, -1.8645, -1.7155, -1.7155]:
            b = ax1.plot(R,Z,color_list[5],alpha=alpha,linewidth = 0.1,zorder=2)##### 5 linewidths=0.8
            b_list.append(b)
            b = ax1.fill(R,Z,facecolor=color_list[5],zorder=2)
            b_list.append(b)
        # 5L
        elif Z==[-1.8644999999999998, -1.8644999999999998, -1.6415, -1.6415]:
            b = ax1.plot(R,Z,color_list[4],alpha=alpha,linewidth = 0.1,zorder=2)##### 5 linewidths=0.8
            b_list.append(b)
            b = ax1.fill(R,Z,facecolor=color_list[4],zorder=2)
            b_list.append(b)
        # 1U
        elif Z==[0.0050000000000000044, 0.0050000000000000044, 0.365, 0.365]:
            b = ax1.plot(R,Z,color_list[0],alpha=alpha,linewidth = 0.1,zorder=2)##### 5 linewidths=0.8
            b_list.append(b)
            b = ax1.fill(R,Z,facecolor=color_list[0],zorder=2)
            b_list.append(b)
        # 2U
        elif Z==[0.40599999999999997, 0.40599999999999997, 0.766, 0.766]:
            b = ax1.plot(R,Z,color_list[1],alpha=alpha,linewidth = 0.1,zorder=2)##### 5 linewidths=0.8
            b_list.append(b)
            b = ax1.fill(R,Z,facecolor=color_list[1],zorder=2)
            b_list.append(b)
        # 3U
        elif Z==[0.8069999999999999, 0.8069999999999999, 1.167, 1.167]:
            b = ax1.plot(R,Z,color_list[2],alpha=alpha,linewidth = 0.1,zorder=2)##### 5 linewidths=0.8
            b_list.append(b)
            b = ax1.fill(R,Z,facecolor=color_list[2],zorder=2)
            b_list.append(b)
        # 4U
        elif Z==[1.208, 1.208, 1.5679999999999998, 1.5679999999999998]:
            b = ax1.plot(R,Z,color_list[3],alpha=alpha,linewidth = 0.1,zorder=2)##### 5 linewidths=0.8
            b_list.append(b)
            b = ax1.fill(R,Z,facecolor=color_list[3],zorder=2)
            b_list.append(b)
        # 1L
        elif Z==[-0.365, -0.365, -0.0050000000000000044, -0.0050000000000000044]:
            b = ax1.plot(R,Z,color_list[0],alpha=alpha,linewidth = 0.1,zorder=2)##### 5 linewidths=0.8
            b_list.append(b)
            b = ax1.fill(R,Z,facecolor=color_list[0],zorder=2)
            b_list.append(b)
        # 2L
        elif Z==[-0.766, -0.766, -0.40599999999999997, -0.40599999999999997]:
            b = ax1.plot(R,Z,color_list[1],alpha=alpha,linewidth = 0.1,zorder=2)##### 5 linewidths=0.8
            b_list.append(b)
            b = ax1.fill(R,Z,facecolor=color_list[1],zorder=2)
            b_list.append(b)
        # 3L
        elif Z==[-1.167, -1.167, -0.8069999999999999, -0.8069999999999999]:
            b = ax1.plot(R,Z,color_list[2],alpha=alpha,linewidth = 0.1,zorder=2)##### 5 linewidths=0.8
            b_list.append(b)
            b = ax1.fill(R,Z,facecolor=color_list[2],zorder=2)
            b_list.append(b)
        # 4L
        elif Z==[-1.5679999999999998, -1.5679999999999998, -1.208, -1.208]:
            b = ax1.plot(R,Z,color_list[3],alpha=alpha,linewidth = 0.1,zorder=2)##### 5 linewidths=0.8
            b_list.append(b)
            b = ax1.fill(R,Z,facecolor=color_list[3],zorder=2)
            b_list.append(b)
        
        
        else:
            b = ax1.plot(R,Z,'#393939',alpha=alpha,linewidth = 0.1,zorder=2)##### 5 linewidths=0.8
            b_list.append(b)
            b = ax1.fill(R,Z,facecolor="#393939",zorder=2)
            b_list.append(b)
    r=[0.912,0.912,0.912,0.912,1.092,1.501,2.500,2.760,0.912,0.912,0.912,0.912,1.092,1.501,2.500,2.760]
    z=[0.185,0.586,0.987,1.388,1.753,1.79,1.20,0.48,-0.185,-0.586,-0.987,-1.388,-1.753,-1.79,-1.20,-0.48]
    w=[0.048,0.048,0.048,0.048,0.186,0.260,0.196,0.186,0.048,0.048,0.048,0.048,0.186,0.260,0.196,0.186]
    h=[0.360,0.360,0.360,0.360,0.223,0.149,0.223,0.223,0.360,0.360,0.360,0.360,0.223,0.149,0.223,0.223]
    a=[0,0,0,0,0,0,116*pi/180,0,0,0,0,0,0,0,-116*pi/180,0]

    for i in range(len(r)):
        rect_F(r[i],z[i],w[i],h[i],a[i])
 
    return b_list
# 绘制等高图
def screen_draw_psi_fig(ax1,gfile_data,struct,lab):
    c_list = []
    
    # 线圈数量
    contour_num = 5
    
    # 线圈范围
    # 通过ax1.contour()的第四个参数指定
    
    GridR,GridZ=np.meshgrid(gfile_data['rgefit'],gfile_data['zgefit'])
    psirzp = (gfile_data['psirz'] - gfile_data['ssimag']) / (gfile_data['ssibry'] - gfile_data['ssimag'])    

    ax1.contour(GridR,GridZ,psirzp,np.linspace(0,0.0009,contour_num*2),colors='red',linewidths=1)# 2中心
    
    c = ax1.contour(GridR,GridZ,psirzp,np.linspace(0.05,0.95,contour_num*2),colors='#fed631',linewidths=0.8)# 4内围
    c_list.append(c)
    B = ax1.contour(GridR,GridZ,psirzp,[1],colors='#d82d2d',linewidths=1.5)# [1]
    c_list.append(B)
    c = ax1.contour(GridR,GridZ,psirzp,np.linspace(1.1,5,contour_num*4),colors='#3dfffe',linewidths=0.8,alpha=0.6,zorder=1.1)# 1外围
    c_list.append(c)
    c = ax1.contour(GridR, GridZ, psirzp,[1], colors='red', linewidths=0.8)# 分割
    c_list.append(c)

    v = B.collections[0].get_paths()[0].vertices 
    # 列坐标 列表
    xlist = v[:,0] 
    # 行坐标 列表
    ylist = v[:,1]
    
    y1=scal_x(xlist,ylist,1.396) # 1.396
    y2=scal_x(xlist,ylist,1.635) # 1.635

    if struct=='2A':
        ax1.text(1.7,1.5,lab,fontsize=8,color='black')
    if (y1!=0) & (y2!=0):
            ax1.scatter([1.396,1.635],[y1,y2],s=15,c='black',marker='x')
            lab_I='I_strike('+str(1.396)+','+'%.3f'%y1+')'
            lab_O='O_strike('+str(1.635)+','+'%.3f'%y2+')'
            ax1.text(1.9,-1.45,lab_I,fontsize=6,color='black')
            ax1.text(1.9,-1.55,lab_O,fontsize=6,color='black')
    elif struct=='2M':
        ax1.text(1.8,-2.6,lab,fontsize=8,color='black')

    return c_list
# 绘制五个曲线图
def screen_draw_prof(ax2,ax3,ax4,ax5,ax6,json_data,max_json_data,afile_data_list,max_afile_data_list,time_list,max_time_list,shot,time,is_defa):
    # 曲线颜色
    col = "#f8d403"
    # 曲线宽度
    line_width=3
    # y轴label的字体大小
    font_size = 18
    # xy轴刻度值的字体大小
    tick_size = 12
    # ylabel格式
    f = "%.2f"
    # 网格透明度
    grid_alpha=0.5
    # ylabel文本内容 设置
    ax2_lb,ax3_lb,ax4_lb,ax5_lb,ax6_lb = r'$I_p(kA)$',r'R(m)',r'a(m)' ,r'$\kappa$',r'$\delta$'
    
    y = {
        "R":[],
        "r":[],
        "k":[],
        "d":[] 
        }
    
    for afile_data in afile_data_list:
        
        y["R"].append(afile_data["rout"])
        y["r"].append(afile_data["aout"])
        y["k"].append(afile_data["eout"])
        y["d"].append((afile_data["doutu"]+afile_data["doutl"])/2)
    
    max_y = {
        "R":[],
        "r":[],
        "k":[],
        "d":[] 
        }
    for max_afile_data in max_afile_data_list:
        
        max_y["R"].append(max_afile_data["rout"])
        max_y["r"].append(max_afile_data["aout"])
        max_y["k"].append(max_afile_data["eout"])
        max_y["d"].append((max_afile_data["doutu"]+max_afile_data["doutl"])/2)
    
    
    # 备用更换数据源，p3-6为afile的字段名，分别绘制到ax3-6
    def set_parameter(p3,p4,p5,p6,afile_data_list,max_afile_data_list):
        y = {
        "R":[],
        "r":[],
        "k":[],
        "d":[] 
        }
    
        for afile_data in afile_data_list:
            
            y["R"].append(afile_data[p3])
            y["r"].append(afile_data[p4])
            y["k"].append(afile_data[p5])
            y["d"].append(afile_data[p6])
        
        max_y = {
            "R":[],
            "r":[],
            "k":[],
            "d":[] 
            }
        for max_afile_data in max_afile_data_list:
            
            max_y["R"].append(max_afile_data[p3])
            max_y["r"].append(max_afile_data[p4])
            max_y["k"].append(max_afile_data[p5])
            max_y["d"].append(max_afile_data[p6])
        return y,max_y
    
    if is_defa:
        max_json_data["Yact"] = [i*1000 for i in max_json_data["Yact"]]
        json_data["Yact"] = [i*1000 for i in json_data["Yact"]]
    
    bottom_ylim = min(max_y["d"])
    top_ylim = max(max_y["d"])
    btw_ylim = top_ylim-bottom_ylim
    mid_ylim = (top_ylim+bottom_ylim)/2
    bottom_xlim = min(max_json_data["X"])
    top_xlim = max(max_json_data["X"])
    
    btw_xlim = top_xlim-bottom_xlim
    
    y_tick = [float(f%bottom_ylim),float(f%mid_ylim),float(f%top_ylim)]
    
   
    
    ax6.plot(time_list,y["d"],col,linewidth=line_width)
    ax6.set_ylim(bottom_ylim-btw_ylim*0.05,top_ylim+btw_ylim*0.05)
    
    ax6.set_xlim(max_time_list[0],max_time_list[-1])
    ax6.set_ylabel(ax6_lb,font=Path(tnr_font_path),color="white",fontsize=font_size)
    ax6.set_xlabel("Time(ms)",font=Path(tnr_font_path),color="white",fontsize=font_size-2)
  
    # ax6.set_xticks(x_tick)
    # ax6.set_xticklabels(x_tick,fontsize=tick_size)
    ax6.set_yticks(y_tick)
    ax6.set_yticklabels(y_tick,fontsize=tick_size)
    ax6.grid(True,color="#00FFFB",linestyle='--',alpha=grid_alpha)
    
    x_tick = list(ax6.get_xticks())[1:-1]
    x_tick_tmp = list(ax6.get_xticks())
    x_tick_tmp = [int(i) for i in x_tick_tmp]
    ax6.set_xticklabels(x_tick_tmp,fontsize=tick_size)
  
    
    
    bottom_ylim = min(max_json_data["Yact"])
    top_ylim = max(max_json_data["Yact"])
    mid_ylim = (top_ylim+bottom_ylim)/2
    btw_ylim = top_ylim-bottom_ylim
    bottom_xlim = min(max_json_data["X"])
    top_xlim = max(max_json_data["X"])
    mid_xlim = (top_xlim+bottom_xlim)/2
    btw_xlim = top_xlim-bottom_xlim
    # x 和 y坐标的刻度值构造生成
    # x_tick = np.linspace(bottom_xlim,top_xlim,7,dtype=int)
    y_tick = [int(bottom_ylim),int(mid_ylim),int(top_ylim)]
    # 绘制曲线
    ax2.plot(json_data['X'],json_data['Yact'],col,linewidth=line_width)
    # y轴刻度值
    ax2.set_ylim(bottom_ylim-btw_ylim*0.05,top_ylim+btw_ylim*0.05)
    # x轴刻度值
    ax2.set_xlim(max_time_list[0],max_time_list[-1])
    # 设置y轴的label
    ax2.set_ylabel(ax2_lb,font=Path(tnr_font_path),color="white",fontsize=font_size-3)
    # x轴刻度
    ax2.set_xticks(x_tick)
    # y轴刻度
    ax2.set_yticks(y_tick)
    # x轴的刻度值颜色设为背景颜色，从而达到去除的效果
    ax2.set_xticklabels(x_tick,color="#000105")
    ax2.set_yticklabels(y_tick,fontsize=tick_size)
    ax2.grid(True,color="#00FFFB",linestyle='--',alpha=grid_alpha)

    # 文本ms位置跟随time的位数调整
    len_time = len(str(int(time)))
    if len_time==1:
        x_shift = 0.74
    elif len_time==2:
        x_shift = 0.78
    elif len_time==3:
        x_shift = 0.82
    elif len_time==4:
        x_shift = 0.86
    else:
        x_shift = 0.9
    
    # 预置数据特殊处理（去除 SHOT# ）
    if is_defa:
        ax2.text(bottom_xlim+btw_xlim*0,top_ylim+btw_ylim*0.4,"          "+"               TIME:          ",color="#9ae2f7",size=17)#"          "
    else:
        # 文本  SHOT#               TIME:          
        ax2.text(bottom_xlim+btw_xlim*0,top_ylim+btw_ylim*0.4,"SHOT#               TIME:          ",color="#9ae2f7",size=17)#"          "
        # 文本 shot的值
        ax2.text(bottom_xlim+btw_xlim*0.24,top_ylim+btw_ylim*0.4,str(shot),color="#00fefc",size=17,horizontalalignment="left",font=Path(digifaw_font_path))
    # 文本 time的值
    ax2.text(bottom_xlim+btw_xlim*0.67,top_ylim+btw_ylim*0.4,str(int(time))+" ",color="#ffc72e",size=17,horizontalalignment="left",font=Path(digifaw_font_path))
    # 文本 ms
    ax2.text(bottom_xlim+btw_xlim*x_shift,top_ylim+btw_ylim*0.4,"ms",color="#ffc72e",size=17,horizontalalignment="left")
    
    
    bottom_ylim = min(max_y["R"])
    top_ylim = max(max_y["R"])
    btw_ylim = top_ylim-bottom_ylim
    mid_ylim = (top_ylim+bottom_ylim)/2
    
    bottom_xlim = min(max_json_data["X"])
    top_xlim = max(max_json_data["X"])
    mid_xlim = (top_xlim+bottom_xlim)/2
    btw_xlim = top_xlim-bottom_xlim
    
    if bottom_ylim==top_ylim:
        y_tick = [mid_ylim-10,mid_ylim,mid_ylim+10]
    else:
        y_tick = [float(f%(bottom_ylim)),float(f%(mid_ylim)),float(f%(top_ylim))]
    # x_tick = np.linspace(bottom_xlim,top_xlim,7,dtype=int)
    
    ax3.plot(time_list,y["R"],col,linewidth=line_width)
    ax3.set_xlim(max_time_list[0],max_time_list[-1])
    ax3.set_ylim(bottom_ylim-btw_ylim*0.05,top_ylim+btw_ylim*0.05)
    # ax3.set_ylim(bottom_ylim,top_ylim)
    ax3.set_ylabel(ax3_lb,font=Path(tnr_font_path),color="white",fontsize=font_size-2)
    ax3.set_xticks(x_tick)
    ax3.set_xticklabels(x_tick,color="#000105")
    #---------------临时添加-----------------------
    y_tick = [150,175,200]
    ax3.set_yticks(y_tick)
    # ---------------临时注释-----------------------
    # y_tick = [float(f%(bottom_ylim/100)),float(f%(mid_ylim/100)),float(f%(top_ylim/100))]
    #---------------临时添加-----------------------
    y_tick = [float(f%(y_tick[0]/100)),float(f%(y_tick[1]/100)),float(f%(y_tick[2]/100))]
    
    
    
    ax3.set_yticklabels(y_tick,fontsize=tick_size)
    ax3.grid(True,color="#00FFFB",linestyle='--',alpha=grid_alpha)
    
    
    
    bottom_ylim = min(max_y["r"])
    top_ylim = max(max_y["r"])
    btw_ylim = top_ylim-bottom_ylim
    mid_ylim = (top_ylim+bottom_ylim)/2
    
    y_tick = [float(f%(bottom_ylim)),float(f%(mid_ylim)),float(f%(top_ylim))]
    ax4.plot(time_list,y["r"],col,linewidth=line_width)
    ax4.set_ylim(bottom_ylim-btw_ylim*0.05,top_ylim+btw_ylim*0.05)
    ax4.set_xlim(max_time_list[0],max_time_list[-1])
    ax4.set_ylabel(ax4_lb,font=Path(tnr_font_path),color="white",fontsize=font_size-2)
    ax4.set_xticks(x_tick)
    ax4.set_xticklabels(x_tick,color="#000105")
    
    #---------------临时添加-----------------------
    y_tick = [40,57,75]
    ax4.set_yticks(y_tick)
    # ---------------临时注释-----------------------
    # y_tick = [float(f%(bottom_ylim/100)),float(f%(mid_ylim/100)),float(f%(top_ylim/100))]
    #---------------临时添加-----------------------
    y_tick = [float(f%(y_tick[0]/100)),float(f%(y_tick[1]/100)),float(f%(y_tick[2]/100))]
    
    
    ax4.set_yticklabels(y_tick,fontsize=tick_size)
    ax4.grid(True,color="#00FFFB",linestyle='--',alpha=grid_alpha)
   
    
    bottom_ylim = min(max_y["k"])
    top_ylim = max(max_y["k"])
    btw_ylim = top_ylim-bottom_ylim
    mid_ylim = (top_ylim+bottom_ylim)/2
    
    y_tick = [float(f%bottom_ylim),float(f%mid_ylim),float(f%top_ylim)]
    
    ax5.plot(time_list,y["k"],col,linewidth=line_width)
    ax5.set_ylim(bottom_ylim-btw_ylim*0.05,top_ylim+btw_ylim*0.05)
    ax5.set_xlim(max_time_list[0],max_time_list[-1])
    ax5.set_ylabel(ax5_lb,font=Path(tnr_font_path),color="white",fontsize=font_size)
    ax5.set_xticks(x_tick)
    ax5.set_xticklabels(x_tick,color="#000105")
    ax5.set_yticks(y_tick)
    y_tick = [float(f%(bottom_ylim)),float(f%(mid_ylim)),float(f%(top_ylim))]
    ax5.set_yticklabels(y_tick,fontsize=tick_size)
    ax5.grid(True,color="#00FFFB",linestyle='--',alpha=grid_alpha)
    
    



    
# ----------------------------------- efit 绘图 ------------------------
## HL-2A 装置结构初始化 ##
# 绘制 ax1 的初始图像
def Draw_2A_stru(figsize=fig_size):
    fig = plt.figure(figsize=figsize)
    fig.subplots_adjust(hspace=0.65,wspace=0.25)
    ax1 = plt.subplot2grid((5,2),(0,0),rowspan=5)
    ax2 = plt.subplot2grid((5,2),(0,1))
    ax3 = plt.subplot2grid((5,2),(1,1))
    ax4 = plt.subplot2grid((5,2),(2,1))
    ax5 = plt.subplot2grid((5,2),(3,1))
    ax6 = plt.subplot2grid((5,2),(4,1))
    ## 真空室 VV ##
    X1=[1.070 ,1.840 ,2.310 ,2.310, 1.840, 1.070, 1.070]
    X2=[1.095, 1.815, 2.270 ,2.270 ,1.815,1.095 ,1.095]
    Y1=[1.215, 1.215 ,0.436 ,-0.436, -1.215, -1.215 ,1.215]
    Y2=[1.185 ,1.185 ,0.430, -0.430 ,-1.185, -1.185 ,1.185]
    ax1.plot(X1,Y1,'lime',X2,Y2,'lime')
    ## 欧姆线圈 E ##
    def rect_E(r,z,w,h):
        r1=r-w/2
        r2=r+w/2
        z1=z-h/2
        z2=z+h/2
        R=[r1,r2,r2,r1,r1,r2,r1,r2]
        Z=[z1,z1,z2,z2,z1,z2,z2,z1]
        ax1.plot(R,Z,'violet')

    r=[0.905, 0.905, 0.905, 0.905, 0.905, 0.905, 0.9745, 1.087, 1.208, 1.725, 2.049, 2.475,
       0.905, 0.905, 0.905, 0.905, 0.905, 0.905, 0.9745, 1.087, 1.208, 1.725, 2.049, 2.475]
    z=[.100,  .286,  .472,  .658,  .844,  1.030,  1.236,  1.359,  1.411,  1.398,  1.172,  .3888,
      -.100, -.286, -.472, -.658, -.844, -1.030, -1.236, -1.359, -1.411, -1.398, -1.172, -.3888]
    w=[0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.062, 0.062, 0.062, 0.066, 0.066, 0.066,
       0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.062, 0.062, 0.062, 0.066, 0.066, 0.066]
    h=[0.145, 0.145, 0.145, 0.145, 0.145, 0.145, 0.158, 0.135, 0.112, 0.059, 0.059, 0.036,
       0.145, 0.145, 0.145, 0.145, 0.145, 0.145, 0.158, 0.135, 0.112, 0.059, 0.059, 0.036]

    for i in range(len(r)):
        rect_E(r[i],z[i],w[i],h[i])
    ## 极向场线圈  ##
    def rect_E1(r,z,w,h):
        r1=r-w/2
        r2=r+w/2
        z1=z-h/2
        z2=z+h/2
        R=[r1,r2,r2,r1,r1,r2,r1,r2]
        Z=[z1,z1,z2,z2,z1,z2,z2,z1]
        ax1.plot(R,Z,'c')
    r=[1.008, 1.008, 1.008, 1.008, 1.9866, 2.345, 2.438, 2.460,
       1.008, 1.008, 1.008, 1.008, 1.9866, 2.345, 2.438, 2.460,
       1.008, 1.825, 2.284, 2.3841,
       1.355, 1.5165, 1.727,
       1.355, 1.5165, 1.727,
       1.006, 2.380,
       1.006, 2.380]

    z=[ .055,  .340,   .450,  .560,  1.210,  .776,  .563,  .325,
       -.055, -.340,  -.450, -.560, -1.210, -.776, -.563, -.325,
       -.165, -1.312, -.745, -.371,
       -.498, -.6753, -.560,
    .498,  .6753,  .560,
        .800, .537,
       -.800, -.537]

    w=[0.028, 0.028, 0.028, 0.028, 0.028, 0.028, 0.028, 0.079,
       0.028, 0.028, 0.028, 0.028, 0.028, 0.028, 0.028, 0.079,
       0.028, 0.028, 0.028, .079,
        .0919, .1237, .0919,
    .0919, .1237, .0919,
        .026, .020,
        .026, .020]

    h=[0.079, 0.079, 0.079, 0.079, 0.079, 0.079, 0.079, 0.028,
       0.079, 0.079, 0.079, 0.079, 0.079, 0.079, 0.079, 0.028,
       0.079, 0.079, 0.079, 0.028,
       .0919, .1237, .0919,
       .0919, .1237, .0919,
       .056, .025,
       .056, .025]
    for i in range(len(r)):
        rect_E1(r[i],z[i],w[i],h[i])

    ##偏滤器线圈挡板##
    Xc=[1.355,1.500,1.5165,1.5165,1.727,1.53]
    Yc=[0.498,0.735,0.6753,0.6753,0.56,0.745]
    Rc=[0.085,0.177,0.1175,0.1175,0.085,0.185]

    PX1=[1.2,1.36]
    PY1=[0.33,0.33]
    Phi=np.linspace(-pi/4,pi/4,10)
    for num in Phi:
        PX1.append(Xc[0]+Rc[0]*math.cos(num))
        PY1.append(Yc[0]+Rc[0]*math.sin(num))
    Phi=np.linspace(5*pi/4,3*pi/4,10)
    for num in Phi:
        PX1.append(Xc[1]+Rc[1]*math.cos(num))
        PY1.append(Yc[1]+Rc[1]*math.sin(num))
    ax1.plot(PX1,PY1,'orange')  #上偏滤器左挡板
    ax1.plot(PX1,[i*(-1) for i in PY1],'orange')  #下偏滤器左挡板

    PX2=[1.4,1.4]
    PY2=[0.96,0.96]
    Phi=np.linspace(pi,5*pi/4,10)
    for num in Phi:
        PX2.append(Xc[2]+Rc[2]*math.cos(num))
        PY2.append(Yc[2]+Rc[2]*math.sin(num))

    PX2.append(1.4915),PX2.append(1.4915)
    PY2.append(0.5203),PY2.append(0.5203)
    Phi=np.linspace(-pi/4,0,10)
    for num in Phi:
        PX2.append(Xc[3]+Rc[3]*math.cos(num))
        PY2.append(Yc[3]+Rc[3]*math.sin(num))
    PX2.append(1.6335),PX2.append(1.6335)
    PY2.append(0.96),PY2.append(0.96)

    
    ax1.plot(PX2,PY2,'orange')  #上偏滤器中挡板
    ax1.plot(PX2,[i*(-1) for i in PY2],'orange')  #下偏滤器中挡板

    PX3=[1.862,1.75]
    PY3=[0.416,0.416]
    Phi=np.linspace(5*pi/4,3*pi/4,10)
    for num in Phi:
        PX3.append(Xc[4]+Rc[4]*math.cos(num))
        PY3.append(Yc[4]+Rc[4]*math.sin(num))
    Phi=np.linspace(-pi/4,pi/4,10)
    for num in Phi:
        PX3.append(Xc[5]+Rc[5]*math.cos(num))
        PY3.append(Yc[5]+Rc[5]*math.sin(num))
    ax1.plot(PX3,PY3,'orange')  #上偏滤器右挡板
    ax1.plot(PX3,[i*(-1) for i in PY3],'orange')  #下偏滤器右挡板
    
    return fig,ax1,ax2,ax3,ax4,ax5,ax6
    ## 初始化结束 ##
    

## HL-2M 装置结构初始化 ##
# 绘制 ax1 的初始图像
def Draw_2Mstru(figsize=fig_size):
    fig = plt.figure(figsize=figsize)
    fig.subplots_adjust(hspace=0.65,wspace=0.28)
    ax1 = plt.subplot2grid((5,2),(0,0),rowspan=5)
    ax2 = plt.subplot2grid((5,2),(0,1))
    ax3 = plt.subplot2grid((5,2),(1,1))
    ax4 = plt.subplot2grid((5,2),(2,1))
    ax5 = plt.subplot2grid((5,2),(3,1))
    ax6 = plt.subplot2grid((5,2),(4,1))
    alpha = 1
    ## 第一壁 ##
    # R_inner_p = [ 1.09,1.145,1.167,1.187,1.200,1.178]
    # Z_inner_p = [-0.802,-0.802,-0.818,-0.890,-1.030,-1.260]
    # R_dome    = [ 1.195,1.202,1.263,1.304,1.357,1.386,1.489,1.554]
    # Z_dome    = [-1.247,-1.245,-1.296,-1.327,-1.348,-1.353,-1.353,-1.353];
    # R_outer_p = [ 1.555,1.572,1.619,1.585,1.580,1.594,1.634,1.653,1.700,1.730,1.751,1.818];
    # Z_outer_p = [-1.388,-1.376,-1.377,-1.272,-1.241,-1.210,-1.152,-1.136,-1.120,-1.108,-1.108,-1.101]; 
    # ax1.plot( R_inner_p,Z_inner_p, R_dome,Z_dome, R_outer_p,Z_outer_p,'k')

    # R_inner_p = [  1.15 ,   1.237 ,  1.194 ]
    # Z_inner_p = [ 0.901 , 1.076   ,1.236 ]
    # R_dome    = [ 1.210  ,  1.397  , 1.510 ]
    # Z_dome    = [ 1.240 ,   1.185 ,  1.310]
    # R_outer_p = [ 1.522   , 1.621  , 1.855 ]
    # Z_outer_p = [ 1.324  ,  1.250 ,  1.153]
    # ax1.plot( R_inner_p,Z_inner_p, R_dome,Z_dome, R_outer_p,Z_outer_p,'k')

    # R_fwi   =   [ 1.145 ,   1.10  , 1.10  ,  1.10    , 1.15]
    # Z_fwi   =   [-0.802 , -0.800   ,0   ,   0.801 ,   0.901]
    # R_fwo   =   [ 1.855  ,1.910   ,2.050   ,2.185 ,   2.367  , 2.462  ,  2.462    ,2.367 ,  2.185  ,  1.910  , 1.855,  1.690]
    # Z_fwo   =   [ 1.153 , 1.018   ,0.889   ,0.763  ,  0.509   ,0.275  , -0.275,   -0.509,  -0.763  , -1.018 , -1.123 , -1.126];
    # ax1.plot( R_fwi,Z_fwi, R_fwo,Z_fwo,'k')

    R_fw_up   =   [ 1.9666 , 1.7612 , 1.6937,  1.6928  , 1.6252 ,   1.6243  ,  1.5568 ,   1.5559 ,   1.4872  ,  1.4862  ,  1.4106 ,   1.4096  ,  1.3334 ,
                    1.3325 , 1.2641 , 1.2634 , 1.2103 ,  1.2099  ,  1.1779   , 1.1778  ,  1.1700   , 1.1700  ,  1.1700  ,  1.1700  ,  1.1700  ,   1.1700  ,  1.1700  ,  1.0950 ,  ]
    Z_fw_up   =   [ 0.9697  ,1.0832 , 1.1201 , 1.1206  , 1.1575  ,  1.1580   , 1.1949 ,   1.1953   , 1.2302  ,  1.2303  ,  1.2449  ,  1.2448  ,  1.2338  ,
                    1.2334 , 1.1981  ,1.1973 , 1.1416  , 1.1407  ,  1.0706 ,   1.0696   , 0.9930   , 0.9920  ,  0.9150  ,  0.9140  ,  0.8370  ,  0.8350  ,  0.8100  ,  0.810 ]
    ax1.plot(R_fw_up,Z_fw_up,'k',alpha=alpha,zorder=2)
    R_fwi   =   [ 1.145  ,  1.105  , 1.105  ,  1.105  ]
    Z_fwi   =   [-0.802,   -0.800  ,   0    ,  0.800  ]
    ax1.plot(R_fwi,Z_fwi,'k',alpha=alpha,zorder=2)
    R_fwo = [ 1.91   , 1.9666  ,  2.0809  ,  2.0818 ,   2.1523  ,  2.1530 ,   2.2345   , 2.2351  ,  2.2973    ,2.2978  ,  2.3605   , 2.3609  ,  2.4012 ,
        2.4015  ,  2.4417  ,  2.4423  ,  2.4847  ,  2.4850 ,   2.4850   , 2.4850  ,  2.4850  ,  2.4850  ,  2.4850  ,  2.4847  ,  2.4423  ,
        2.4417  , 2.4015  ,  2.4012,    2.3609  ,  2.3605 ,   2.2978   , 2.2973  ,  2.2351  ,  2.2345   , 2.1530   , 2.1523  ,  2.0818  ,  2.0809  ,  1.9666   
        ]
    Z_fwo = [ -1.01 ,  -0.9697  , -0.9089 ,  -0.9083 ,  -0.8541  , -0.8534 ,  -0.7521  , -0.7513 ,  -0.6383  , -0.6374 ,  -0.5236 ,   -0.5227  , -0.3991  , 
        -0.3981 , -0.2750  , -0.2730 ,  -0.1429 ,  -0.1413 ,  -0.0540 ,  -0.0530   , 0.0530  ,  0.0540  ,  0.1413 ,   0.1429  ,  0.2730 ,   
        0.2750 ,   0.3981  ,  0.3991 ,   0.5227  ,  0.5236 ,   0.6374  ,  0.6383  ,  0.7513   , 0.7521 ,   0.8534  ,  0.8541  ,  0.9083 ,   0.9089,   0.9697 ]
    ax1.plot(R_fwo,Z_fwo,'k',alpha=alpha,zorder=2)
    R_inner_p_new = [ 1.098  ,  1.145  , 1.1666 ,  1.2066 ,  1.2099,   1.1783    ]
    Z_inner_p_new = [ -0.802 , -0.802 , -0.8145  ,-0.8837  ,-0.8984 ,  -1.259  ]
    ax1.plot(R_inner_p_new,Z_inner_p_new,'k',alpha=alpha,zorder=2)
    R_dome_new    = [ 1.1947 , 1.2019  ,  1.2871   , 1.302  , 1.3579  ,1.3729 , 1.3886 , 1.5536 , 1.5559  ]
    Z_dome_new    = [-1.2468 ,-1.2447 ,  -1.317 ,  -1.326  , -1.3477,-1.352 , -1.3535 , -1.3535  ,-1.3615 ]
    ax1.plot(R_dome_new,Z_dome_new,'k',alpha=alpha,zorder=2)
    R_outer_p_new = [ 1.5546 ,  1.5714 , 1.6134 ,  1.6168  , 1.584  ,  1.581  ,  1.590, 1.6225  , 1.6355 ,   1.6528  , 1.7234  , 1.91]
    Z_outer_p_new = [-1.3845 , -1.3765 ,-1.3765 , -1.3709 , -1.2701 , -1.2398, -1.2156, -1.1647 , -1.1488  , -1.1364  ,-1.0989 , -1.01]
    ax1.plot(R_outer_p_new,Z_outer_p_new,'k',alpha=alpha,zorder=2)




    ## 真空室 VV ##
    base=os.path.dirname(os.path.realpath(__file__))
    # base = get_sw_path_info()
   
    # sw_workflow_home = info['sw_workflow_home']
    f=open(base+'/input/HL2M-vv.txt')
    f.readline()
    R_inner=[]
    for i in range(119):
        R_inner.append(float(f.readline()))

    f.readline()
    Z_inner=[]
    for i in range(119):
        Z_inner.append(float(f.readline()))

    f.readline()
    R_outer=[]
    for i in range(119):
        R_outer.append(float(f.readline()))

    f.readline()
    Z_outer=[]
    for i in range(119):
        Z_outer.append(float(f.readline()))

    ax1.plot(R_inner,Z_inner,'lime',R_outer,Z_outer,'lime')
    f.close()
    ## 边界 TF ##
    
    f=open(base+'/input/HL2M-TF.txt')

    f.readline()
    R_inner=[]
    for i in range(2200):
        R_inner.append(float(f.readline()))

    f.readline()
    Z_inner=[]
    for i in range(2200):
        Z_inner.append(float(f.readline()))

    f.readline()
    R_outer=[]
    for i in range(4000):
        R_outer.append(float(f.readline()))

    f.readline()
    Z_outer=[]
    for i in range(4000):
        Z_outer.append(float(f.readline()))

    ax1.plot(R_inner,Z_inner,'black',R_outer,Z_outer,'black')
    ax1.fill(R_outer,Z_outer,facecolor='bisque')
    ax1.fill(R_inner,Z_inner,facecolor='white')
    ## 欧姆线圈 E ##
    def rect_E(r,z,w,h):  
            r1=r-w/2
            r2=r+w/2
            z1=z-h/2
            z2=z+h/2
            R=[r1,r2,r2,r1]   # R=[r1,r2,r2,r1,r1,r2,r1,r2]   
            Z=[z1,z1,z2,z2]   # Z=[z1,z1,z2,z2,z1,z2,z2,z1]
            ax1.plot(R,Z,'#fff4fc')
            ax1.fill(R,Z,facecolor="#fbb3b3")
    r=[0.748,0.748]
    z=[0.887,-0.887]
    w=[0.117,0.117]
    h=[1.774,1.774]
    for i in range(len(r)):
        rect_E(r[i],z[i],w[i],h[i])
    ## 极向场线圈 ##
    def rect_F(r,z,w,h,a):
        if a==0:
            r1=r-w/2
            r2=r+w/2
            z1=z-h/2
            z2=z+h/2

            R=[r1,r2,r2,r1]   # R=[r1,r2,r2,r1,r1,r2,r1,r2]
            Z=[z1,z1,z2,z2]   # Z=[z1,z1,z2,z2,z1,z2,z2,z1]
        else:
            r1=r-(w/2+h/2/math.tan(a))
            r2=r+(w/2-h/2/math.tan(a))
            r3=r+(w/2+h/2/math.tan(a))
            r4=r-(w/2-h/2/math.tan(a))

            z1=z-h/2
            z2=z+h/2
            R=[r1,r2,r3,r4] # R=[r1,r2,r3,r4,r1,r3,r4,r2]
            Z=[z1,z1,z2,z2] # Z=[z1,z1,z2,z2,z1,z2,z2,z1]
        ax1.plot(R,Z,'#fff4fc')
        ax1.fill(R,Z,facecolor="#fbb3b3")
    r=[0.912,0.912,0.912,0.912,1.092,1.501,2.500,2.760,0.912,0.912,0.912,0.912,1.092,1.501,2.500,2.760]
    z=[0.185,0.586,0.987,1.388,1.753,1.79,1.20,0.48,-0.185,-0.586,-0.987,-1.388,-1.753,-1.79,-1.20,-0.48]
    w=[0.048,0.048,0.048,0.048,0.186,0.260,0.196,0.186,0.048,0.048,0.048,0.048,0.186,0.260,0.196,0.186]
    h=[0.360,0.360,0.360,0.360,0.223,0.149,0.223,0.223,0.360,0.360,0.360,0.360,0.223,0.149,0.223,0.223]
    a=[0,0,0,0,0,0,116*pi/180,0,0,0,0,0,0,0,-116*pi/180,0]

    for i in range(len(r)):
        rect_F(r[i],z[i],w[i],h[i],a[i])
    return fig,ax1,ax2,ax3,ax4,ax5,ax6
    ## 初始化结束 ##
 

# 坐标系调整
# draw_psi_fig中调用
def scal_x(xlist,ylist,par):
    X=[]
    Y=[]
    for i in range(len(xlist)):
        if (abs(xlist[i]-par)<0.01) & (ylist[i]<(-0.7)):
            X.append(xlist[i])
            Y.append(ylist[i])
        if len(X)!=0:
            if (X[0]-X[-1])==0:
                k = np.nan
            else:
                k=(Y[0]-Y[-1])/(X[0]-X[-1])
            b=Y[-1]-k*X[-1]
            h=k*par+b
            return(h)
        else:
            return 0
        
# gfile 为数据源 绘制 ax1 等高图
def draw_psi_fig(ax1,gfile_data,struct,lab):

    # ax1：父容器
    # gfile_data：gfile数据
    # struct：结果，2A（反演）或者2M(平衡）
    # lab:显示在图上的标签，一般为shot+时间片
    GridR,GridZ=np.meshgrid(gfile_data['rgefit'],gfile_data['zgefit'])
    psirzp = (gfile_data['psirz'] - gfile_data['ssimag']) / (gfile_data['ssibry'] - gfile_data['ssimag'])    
    ax1.set_xlabel('R(m)', fontsize=10)
    ax1.set_ylabel('Z(m)', fontsize=10)
    ax1.set_title('psi_norm',fontsize=10)
    contour_num = 5
    # ax1.contour(GridR,GridZ,psirzp,np.linspace(0,0.0009,contour_num*2),colors='#d82d2d',linewidths=1)# 2
    # ax1.contour(GridR,GridZ,psirzp,np.linspace(0.05,0.95,contour_num*4),colors='#d82d2d',linewidths=0.8)# 4
    # B=ax1.contour(GridR,GridZ,psirzp,[1],colors='#d82d2d',linewidths=1.5)# [1]
    # ax1.contour(GridR,GridZ,psirzp,np.linspace(0.96,0.99,contour_num),colors='#d82d2d',linewidths=0.8)# 1
    # ax1.contour(GridR, GridZ, psirzp,[1.1], colors='blue', linewidths=0.8)
    
    # ax1.contour(GridR,GridZ,psirzp,np.linspace(0,0.0009,contour_num*2),colors='#126363',linewidths=1)# 2
    # ax1.contour(GridR,GridZ,psirzp,np.linspace(0.05,0.95,contour_num*4),colors='#126363',linewidths=0.8)# 4
    # B=ax1.contour(GridR,GridZ,psirzp,[1],colors='red',linewidths=1.5)# [1]
    # ax1.contour(GridR,GridZ,psirzp,np.linspace(0.96,0.99,contour_num),colors='#126363',linewidths=0.8)# 1
    # ax1.contour(GridR, GridZ, psirzp,[1.1], colors='red', linewidths=0.8)

    ax1.contour(GridR,GridZ,psirzp,np.linspace(0,0.0009,contour_num*2),colors='red',linewidths=1.2)# 2中心
    ax1.contour(GridR,GridZ,psirzp,np.linspace(0.05,0.95,contour_num*2),colors='#126363',linewidths=1)# 4内围
    B = ax1.contour(GridR,GridZ,psirzp,[1],colors='#126363',linewidths=1.5)# [1]
    ax1.contour(GridR,GridZ,psirzp,np.linspace(1.1,5,contour_num*4),colors='#126363',linewidths=1.2,alpha=0.6,zorder=1.1)# 1外围
    ax1.contour(GridR, GridZ, psirzp,[1], colors='red', linewidths=1)# 分割



    v = B.collections[0].get_paths()[0].vertices 
    # 列坐标 列表
    xlist = v[:,0] 
    # 行坐标 列表
    ylist = v[:,1]
    
    y1=scal_x(xlist,ylist,1.396) # 1.396
    y2=scal_x(xlist,ylist,1.635) # 1.635

    if struct=='2A':
        ax1.text(1.7,1.5,lab,fontsize=8,color='black')
    if (y1!=0) & (y2!=0):
            ax1.scatter([1.396,1.635],[y1,y2],s=15,c='black',marker='x')
            lab_I='I_strike('+str(1.396)+','+'%.3f'%y1+')'
            lab_O='O_strike('+str(1.635)+','+'%.3f'%y2+')'
            ax1.text(1.9,-1.45,lab_I,fontsize=6,color='black')
            ax1.text(1.9,-1.55,lab_O,fontsize=6,color='black')
    elif struct=='2M':
        ax1.text(1.8,-2.6,lab,fontsize=8,color='black')
# gfile 为数据源 绘制 ax1 等高图


def draw_prof(ax2,ax3,ax4,ax5,ax6,gfile_data,col):
    # ax2,ax3,ax4,ax5,ax6：5个线形图的父容器
    # gfile_data：gfile解析结果数据
    # col：线条颜色

    ax2.plot(gfile_data['R_Pprof'],gfile_data['Pprof'],col)
    ax2.set_ylabel('P(pa)', fontsize=10)
    # y_major_locator=plt.MultipleLocator(20000)
    # ax2.yaxis.set_major_locator(y_major_locator)
   
    ax3.plot(gfile_data['R_qprof'],gfile_data['qprof'],col)
    ax3.set_ylabel('q', fontsize=10)
    # y_major_locator=plt.MultipleLocator(40)
    # ax3.yaxis.set_major_locator(y_major_locator)

    ax4.plot(gfile_data['R_Jprof'],gfile_data['Jprof_mid'],col)
    ax4.set_ylabel('J(MA/m2)', fontsize=10)  
    ax4.set_xlabel('R(m)', fontsize=9)
    # y_major_locator=plt.MultipleLocator(4)
    # ax4.yaxis.set_major_locator(y_major_locator)
    
    if len(gfile_data['rhovn'])!=0:
        ax5.plot(gfile_data['rhovn'],gfile_data['ffprim'],col)
        ax5.set_ylabel('ff\'', fontsize=10)
        # y_major_locator=plt.MultipleLocator(2)
        # ax3.yaxis.set_major_locator(y_major_locator)
        
        ax6.plot(gfile_data['rhovn'],gfile_data['pprime'],col)
        ax6.set_ylabel('p\'', fontsize=10)
        ax6.set_xlabel('rhovn', fontsize=10) 


# gfile 为数据源 绘制 ax1 叠加图的 单个图
def Surface(ax1,gfile_data,color,la):
    GridR,GridZ=np.meshgrid(gfile_data['rgefit'],gfile_data['zgefit'])
    psirzp = (gfile_data['psirz'] - gfile_data['ssimag']) / (gfile_data['ssibry'] - gfile_data['ssimag'])
    
    ax1.contour(GridR,GridZ,psirzp,np.linspace(0,0.0009,2),colors=color,linewidths=1.8)
    ax1.contour(GridR,GridZ,psirzp,np.linspace(0.05,1.02,5),colors=color,linewidths=1.8)
    x=[1,1.00001]
    y=[-1,-1]
    co=color
    ax1.plot(x,y,color=co,label=la)
    ax1.legend(loc=4,fontsize=6)


def get_parameter(afile_data):
    # 删掉 'bcentr','areao','simagx','taumhd','betapd','betatd','wplasmd','fluxx','nsilop0','magpri0'
    parameters=['shot','time','rcencm','pasmat','rout','zout','aout','eout','doutu','doutl','vout','betat','betap','ali','qpsib','wplasm','elongm','qqmagx','rmagx','zmagx','bcentr','areao','simagx','taumhd','betapd','betatd','wplasmd','fluxx','nsilop0','magpri0']
   
    parameter_dic = {}
   
  
    
    for parameter in parameters:
        parameter_dic[parameter] = afile_data[parameter]
        
    return parameter_dic

 # 根据afile列表和所选的目标参数列表，画参数波形图
def draw_wave_form(afile_data_list,parameter_list,connect_type):
    # afile_path_list: afile的路径列表
    # parameter_list: 勾选的参数列表
    # connect_type: 绘图的连接类型，linear折线图，spline曲线图
    # 返回值 fig

    # 多个axes的标注列表
    global po_annotation_list
    po_annotation_list = []


    # 根据 绘图数量 计算尺寸
    if (len(parameter_list)%2)==1:
        row=len(parameter_list)//2+1
        num=1
    else:
        row=len(parameter_list)//2
        num=0          
    fig,ax=plt.subplots(row,2,figsize=(11.94,5.93),constrained_layout = True)#fig_size[0],2*row
    # fig.subplots_adjust(hspace=0.3,wspace=0.3)

    # 生成 x坐标
    x = []
    for afile_data in afile_data_list:
        x.append(afile_data['time'])
    
    
    for i in range(len(parameter_list)):
        y = []
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

        ax[item].set_ylabel(parameter_list[i],fontsize=12)

        # 生成 y坐标
        for afile_data in afile_data_list:
            y.append(afile_data[parameter_list[i]])


    #   勾选的linear 将散点直线连接
        if connect_type == 'linear':
            ax[item].plot(x,y,label='linear')
            ax[item].scatter(x,y,marker = 'o',s=4,color='red')

            # 生成 标注
            po_annotation = []
            for i in range(len(x)):
                # 标注点的坐标
                point_x = x[i]
                point_y = y[i]
                point, = ax[item].plot(point_x, point_y, 'o', c='lightblue')
                # 标注框偏移量
                offset1 = -8
                offset2 = -2
                if i/len(x)>0.4:
                    offset1 = -70
                
                # 标注框
                bbox1 = dict(boxstyle="round", fc='lightblue', alpha=0.6)
                # 标注箭头
                arrowprops1 = dict(arrowstyle="->", connectionstyle="arc3,rad=0.")
                # 标注
                annotation = ax[item].annotate(str(x[i])+","+str(y[i]), xy=(x[i], y[i]), xytext=(offset1, offset2), textcoords='offset points',
                                        bbox=bbox1, arrowprops=arrowprops1, size=8)
                # 默认鼠标未指向时不显示标注信息
                annotation.set_visible(False)
                po_annotation.append([point, annotation])
            po_annotation_list.append(po_annotation)

    #   勾选的spline 将散点曲线连接
        if connect_type == 'spline':
            x2=np.linspace(x[0],x[-1],100)
            # 拟合曲线
            spline=interpolate.splrep(x,y)
            # 用新的x轴值求得拟合曲线的y值
            y_bspline=interpolate.splev(x2,spline)
            ax[item].plot(x2,y_bspline,'magenta',label='spline')
            ax[item].scatter(x,y,marker = 'o',s=4,color='red')

            # 生成 标注
            po_annotation = []
            for i in range(len(x)):
                # 标注点的坐标
                point_x = x[i]
                point_y = y[i]
                point, = ax[item].plot(point_x, point_y, 'o', c='lightblue')
                # 标注框偏移量
                offset1 = -8
                offset2 = -2
                if i/len(x)>0.4:
                    offset1 = -70
                # 标注框
                bbox1 = dict(boxstyle="round", fc='lightblue', alpha=0.6)
                # 标注箭头
                arrowprops1 = dict(arrowstyle="->", connectionstyle="arc3,rad=0.")
                # 标注
                annotation = ax[item].annotate(str(x[i])+","+str(y[i]), xy=(x[i], y[i]), xytext=(offset1, offset2), textcoords='offset points',
                                        bbox=bbox1, arrowprops=arrowprops1, size=8)
                # 默认鼠标未指向时不显示标注信息
                annotation.set_visible(False)
                po_annotation.append([point, annotation])
            po_annotation_list.append(po_annotation)


    if num:
        if row==1:
            ax[1].remove()
        else:
            ax[row-1,1].remove()
   
    return(fig)
 
def read_a(afile_path):
    
    base=os.path.dirname(os.path.realpath(__file__))
    sw_framework_root = os.path.abspath(base+"/../../")
    if not sw_framework_root in sys.path:
        sys.path.append(sw_framework_root)
        
    from data_parser import ParserFactory,SWMapper
    

  
    # 解析
    parser = ParserFactory.getParser("afile", afile_path)
    # 转字典
    afile_data = parser.read().toDict()
    
 
    return afile_data


def read_g_and_extra(gfile_path):
    base=os.path.dirname(os.path.realpath(__file__))
    sw_framework_root = os.path.abspath(base+"/../../")
    if not sw_framework_root in sys.path:
        sys.path.append(sw_framework_root)
        
    from data_parser import ParserFactory,SWMapper

    # 解析
    parser = ParserFactory.getParser("gfile", gfile_path)
    # 转字典
    gfile_data = parser.read().toDict()
  
    rleft = gfile_data["rleft"]
    rdim = gfile_data["rdim"]
    nw = gfile_data["nw"]
    zmid = gfile_data["zmid"]
    zdim = gfile_data["zdim"]
    current = gfile_data["current"]
    pprime = gfile_data["pprime"]
    ffprime = gfile_data["ffprime"]

    gfile_data["rgefit"] = np.linspace(rleft,rleft+rdim,nw)
    gfile_data["zgefit"] = np.linspace(zmid-zdim/2,zmid+zdim/2,nw)
    gfile_data["psirz"] = np.mat(gfile_data["psirz"]).reshape(gfile_data["nw"],gfile_data["nh"])
    gfile_data["ssimag"] = gfile_data["simag"]
    gfile_data["ssibry"] = gfile_data["sibry"]
    gfile_data["ffprim"] = [-np.sign(current)*ffprime[i]  for i in range(nw)]
    gfile_data["pprime"] = [-np.sign(current)*pprime[i] / 100000 for i in range(nw)]

    gfile_data = read_g_extra(gfile_path,nw,gfile_data)
    return gfile_data

    
def read_g_extra(gfile_path,nw,gfile_data):
    
    gfile_num_regx = re.compile(r'^[\s\-][e\d\.\+\-]{15}')
    gfile_path = gfile_path[:-6] + "_" + gfile_path[-5:]
    with open(gfile_path+"_extra.txt", 'r') as f:
        dum = []

        for line in f:
            if re.match(gfile_num_regx, line): #该行匹配到gfile_num_regx模式
                #提取该行所有科学计数法数字，float转换后加入到dum数组
                dum += [float(line[i: i + 16]) for i in range(0, len(line.strip()), 16)]

            else: #特殊行
                line_info_arr = line.split()
                if(len(line_info_arr)==2):  #有两组数字的特殊行
                    nbbbs=int(line_info_arr[0])
                    limitr=int(line_info_arr[1])

    gfile_data['rhovn']=dum[:nw]
    del dum[:nw]

    gfile_data['R_Pprof']=dum[:nw]

    gfile_data['Pprof']=dum[nw:2*nw]
    gfile_data['R_qprof']=dum[2*nw:3*nw]
    gfile_data['qprof']=dum[3*nw:4*nw]
    gfile_data['R_Jprof']=dum[4*nw:5*nw]
    pum=dum[5*nw:6*nw]
    gfile_data['Jprof_mid']=[pum[i] / 100000 for i in range(nw)]

    return gfile_data

# 读取单个Gfile
def read_g(gfile_path):
    base=os.path.dirname(os.path.realpath(__file__))
    sw_framework_root = os.path.abspath(base+"/../../")
    if not sw_framework_root in sys.path:
        sys.path.append(sw_framework_root)
        
    from data_parser import ParserFactory,SWMapper

    # 解析
    parser = ParserFactory.getParser("gfile", gfile_path)
    # 转字典
    gfile_data = parser.read().toDict()
  
    rleft = gfile_data["rleft"]
    rdim = gfile_data["rdim"]
    nw = gfile_data["nw"]
    zmid = gfile_data["zmid"]
    zdim = gfile_data["zdim"]
    current = gfile_data["current"]
    pprime = gfile_data["pprime"]
    ffprime = gfile_data["ffprime"]
    
    gfile_data["rgefit"] = np.linspace(rleft,rleft+rdim,nw)
    gfile_data["zgefit"] = np.linspace(zmid-zdim/2,zmid+zdim/2,nw)
    gfile_data["psirz"] = np.mat(gfile_data["psirz"]).reshape(gfile_data["nw"],gfile_data["nh"])
    gfile_data["ssimag"] = gfile_data["simag"]
    gfile_data["ssibry"] = gfile_data["sibry"]
    gfile_data["ffprim"] = [-np.sign(current)*ffprime[i]  for i in range(nw)]
    gfile_data["pprime"] = [-np.sign(current)*pprime[i] / 100000 for i in range(nw)]

   
    return gfile_data

def ids_read_g(user,db,shot,run,time):
    base=os.path.dirname(os.path.realpath(__file__))
    sw_framework_root = os.path.abspath(base+"/../../")
    if not sw_framework_root in sys.path:
        sys.path.append(sw_framework_root)
        
    # info = get_sw_path_info()
    # sw_framework_root = info['sw_framework_root']
    # if not sw_framework_root in sys.path:
    #     sys.path.append(sw_framework_root)
    # from data_parser import ParserFactory,SWMapper,NetcdfParser
        
    from data_parser import ParserFactory,SWMapper
    shot = str(shot)
    time = str(time)

    

    
    
    
    gfile_mapper = SWMapper()
    gfile_yaml_path = sw_framework_root+"/mappers/gfile_ids_mapper.yaml"
    gfile_mapper.updateMapperYAMLFile(gfile_yaml_path)
    gfile_tree = gfile_mapper.ids_reflect_mapping(db,int(shot),int(run),int(time))
    gfile_data = gfile_tree.toDict()
    

    data_entry = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,db,int(shot),int(run),str(user))

    data_entry.open()
    equilibrium = data_entry.get('equilibrium')
    c_str = equilibrium.ids_properties.comment
    
    time_list = list(equilibrium.time)
    index = time_list.index(int(time)/1000.0)
    # print(index)
    
    bcentr,areao,simagx,taumhd,betapd,betatd,wplasmd,fluxx,nsilop0,magpri0,nw,nh,nbbbs,limitr = c_str.split(",")[:14]
    gfile_data["shot"] = shot
    gfile_data["time"] = time
    gfile_data["nw"] = nw
    gfile_data["nh"] = nh
    gfile_data["nbbbs"] = nbbbs
    gfile_data["limitr"] = limitr

    
    nw = int(gfile_data["nw"])
    nh = int(gfile_data["nh"])
    nbbbs = int(gfile_data["nbbbs"])
    limitr = int(gfile_data["limitr"])
    
    rleft = equilibrium.time_slice[index].boundary.b_flux_pol_norm
    rdim = equilibrium.grids_ggd[index].grid[0].space[0].objects_per_dimension[0].object[0].measure

    zmid = equilibrium.time_slice[index].boundary.geometric_axis.z
    zdim = equilibrium.time_slice[index].boundary.psi

    current = equilibrium.time_slice[index].global_quantities.ip
    pprime = equilibrium.time_slice[index].profiles_1d.dpressure_dpsi
    ffprime = equilibrium.time_slice[index].profiles_1d.f_df_dpsi
    

    
    





    gfile_data["rgefit"] = np.linspace(rleft,rleft+rdim,nw)
    gfile_data["zgefit"] = np.linspace(zmid-zdim/2,zmid+zdim/2,nw)

    
    gfile_data["psirz"] = np.mat(gfile_data["psirz"]).reshape(nw,nh)





    gfile_data["ssimag"] = gfile_data["simag"]
    gfile_data["ssibry"] = gfile_data["sibry"]
    gfile_data["ffprim"] = [-np.sign(current)*ffprime[i]  for i in range(nw)]
    gfile_data["pprime"] = [-np.sign(current)*pprime[i] / 100000 for i in range(nw)]
    gfile_data["rhovn"] = equilibrium.time_slice[index].profiles_1d.j_parallel
    gfile_data["Pprof"] = equilibrium.time_slice[index].profiles_1d.magnetic_shear
    gfile_data["R_Pprof"] = equilibrium.time_slice[index].profiles_1d.r_inboard
    gfile_data["qprof"] = equilibrium.time_slice[index].profiles_1d.r_outboard
    gfile_data["R_qprof"] = equilibrium.time_slice[index].profiles_1d.rho_tor_norm
    gfile_data["R_Jprof"] = equilibrium.time_slice[index].profiles_1d.rho_tor
    gfile_data["Jprof_mid"] = equilibrium.time_slice[index].profiles_1d.j_tor
    
    
    return gfile_data

def ids_read_a(user,db,shot,run,time):
    base=os.path.dirname(os.path.realpath(__file__))
    sw_framework_root = os.path.abspath(base+"/../../")
    if not sw_framework_root in sys.path:
        sys.path.append(sw_framework_root)
        
    from data_parser import ParserFactory,SWMapper
    
    
    
    afile_mapper = SWMapper()
    afile_yaml_path = sw_framework_root+"/mappers/afile_ids_mapper.yaml"
    afile_mapper.updateMapperYAMLFile(afile_yaml_path)
  
    afile_tree = afile_mapper.ids_reflect_mapping(db,int(shot),int(run),int(time))
    afile_data = afile_tree.toDict()
    
    
    data_entry = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,db,int(shot),int(run),str(user))
    data_entry.open()
    equilibrium = data_entry.get('equilibrium')
    c_str = equilibrium.ids_properties.comment
    
    bcentr,areao,simagx,taumhd,betapd,betatd,wplasmd,fluxx,nsilop0,magpri0,nw,nh,nbbbs,limitr = c_str.split(",")[:14]
    afile_data["rcencm"] = afile_data["rcencm"]*100
    afile_data["bcentr"] = bcentr
    afile_data["areao"] = areao
    afile_data["simagx"] = simagx
    afile_data["taumhd"] = taumhd
    afile_data["betapd"] = betapd
    afile_data["betatd"] = betatd
    afile_data["wplasmd"] = wplasmd
    afile_data["fluxx"] = fluxx
    afile_data["nsilop0"] = nsilop0
    afile_data["magpri0"] = magpri0
    afile_data["shot"] = shot
    afile_data["time"] = time
    
    return afile_data
    

def built_shot(shot):
    shot = "%06d"%int(shot)
    return shot

def built_time(time): 
    time = "%05d"%int(time)
    return time


# 返回目录的 所有全为数字的子文件夹名 
def get_dir_name(path):
    dir_name_list = []
    file_list = os.listdir(path)
    for file_name in file_list:
        if file_name.isdigit():
            dir_name_list.append(file_name)
    dir_name_list.sort()
    return dir_name_list
   
# 返回目录的 所有全为数字的子文件名
def get_file_name(path):
    file_name_list = []
    file_list = os.listdir(path)
    for file_name in file_list:
        if file_name.isdigit():
            file_name_list.append(file_name)
    file_name_list.sort()
    return file_name_list

# dic转json，自定义序列化方法
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

class IMASPathParser:
    def __init__(self,user) -> None:
         # 之前的用户名列表
        presentUserNameList = []

        self.dic = {}
        # 获取 本机 用户名
        username = getpass.getuser()

        # 获取本机用户名的路径
        userPath = os.path.abspath(os.path.join(
                        os.path.dirname(__file__), os.environ['HOME'], '..'))
        userPath = userPath + "/" + username


        if os.path.exists(userPath) is False or \
                            username in presentUserNameList:
                        print("user path does not exist")
        # 用户列表            
        presentUserNameList.append(username)
    

        # IMASDB路径
        imasdbPath = userPath + "/public/imasdb"
     

        # 数据库列表
        databaseList = [dI for dI in os.listdir(imasdbPath)
                                    if os.path.isdir(os.path.join(imasdbPath, dI))]
        databaseList.sort()

        # self.db_dic["db"] = databaseList


        for db in databaseList:
            # 0-9 对应炮号 
            # 0-9999 在0目录，10000-19999在1目录下，20000-29999在2目录下，依次类推到9目录
            shot_dic = {}
            for d in range(10):  
                
                # /3/ 是 IMAS的版本号
                # 炮号的路径
                shotRunPath = imasdbPath + "/" + db + "/3/" + str(d)
                if os.path.exists(shotRunPath) is False:
                    continue
                
                # shotList 不能重复
                shotList = []
                run_list = []

                # 获取以 .datafile 结尾的文件数量
                dataFileCounter = len(glob.glob1(shotRunPath, "*.datafile"))
                dataFileList = [""]*dataFileCounter

                # 将以 .datafile 结尾的文件加入dataFileList
                i = 0
                for f in os.listdir(shotRunPath):
                    if f.endswith(".datafile"):
                        dataFileList[i] = f
                        i += 1

                # 必须 排序 之后会有位置的对应关系
                dataFileList.sort()
                counter = -1
                for i in range(len(dataFileList)):
                    # 提取 shot 和 run_number
                    # 提取规则： 最后四位是run_number 剩下的是shot
                    rs = dataFileList[i].split(".")[0] # ids_1210001
                    rs = rs.split("_")[1] # 1210001
                    try:
                        if d == 0:
                            run = int(rs[-4:])# 0001 -> 1
                        else:
                            run = int(str(d)+rs[-4:])
                    except:
                        # In case non-valid .datafile name is found
                        # e.g. 'ids_model.datafile', skip this file
                        continue
                    run = str(run)
                    shot = rs[:-4] # 121

                    if shot not in shotList:
                        shotList.append(shot)
                        run_list.append([])
                        counter += 1
                    run_list[counter].append(run)
            
                for index,shot in enumerate(shotList):
                    shot_dic[shot] = run_list[index]
                
            
            self.dic[str(db)] = shot_dic
       
    # 获取当前用户下的 所有数据库           
    def get_db(self):
        return self.dic.keys()

    # 获取当前数据库下的 所有shot
    def get_shot(self,db):
        return self.dic[str(db)].keys()
    
    # 获取当前 shot 下的 所有 time
    def get_run_number_list(self,db,shot):
        return self.dic[str(db)][str(shot)]
    
    # 获取所有时间片
    def get_time_list(self,user,database,shot,run,mod):
        #得到一个Data Entry的句柄
        data_entry = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,database,int(shot),int(run),user)
        data_entry.open() #打开Data Entry

        #获取所有时间片 
        if mod == "equilibrium":
            equilibrium = data_entry.get(mod)
            return equilibrium.time
        elif mod == "core_profiles":
            core_profiles = data_entry.get(mod)
            return core_profiles.time
        elif mod == "mhd_linear":
            mhd_linear = data_entry.get(mod)
            return mhd_linear.time
        
        data_entry.close()
        
    def get_afile_data(self,user,database,shot,run,mod,time):
        afile_data = {}
         #得到一个Data Entry的句柄
        data_entry = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,database,int(shot),int(run),user)
        data_entry.open() #打开Data Entry

        #获取所有时间片 
        equilibrium = data_entry.get(mod)
        
        
        
        return afile_data
        
    def get_all(self):
        return self.dic





# -----------------------------------OneTwo绘图---------------------------------------

def read_file(file_path,gfile_path):
    base=os.path.dirname(os.path.realpath(__file__))
    sw_framework_root = os.path.abspath(base+"/../../")
    if not sw_framework_root in sys.path:
        sys.path.append(sw_framework_root)
    from data_parser import ParserFactory,SWMapper,NetcdfParser
    
    # file_path = Var.select_time_list[0]["path"] + "/statefile_2.000000E+01.nc"
    parser = NetcdfParser.NetcdfParser(file_path)
    tree = parser.read()
    data = tree.toDict()
 
    # gfile_path = config["work_flow_path"]+"/data/EFIT/out/"+Var.select_time_list[0]["shot"]+"/"+Var.select_time_list[0]["time"]+"/g"+Var.select_time_list[0]["shot"]+"."+Var.select_time_list[0]["time"]

    # 转字典
    gfile_data = read_g_and_extra(gfile_path)
 
    q = np.array(gfile_data["qpsi"])
    rho = np.array(gfile_data["rhovn"])
    data["q"] = q
    data["rho"] = rho
    return data


def read_ids(user,db,shot,run,time):
    time = int(time)
    data_entry = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,db,int(shot),int(run),str(user))
    data_entry.open()
    core_profiles = data_entry.get('core_profiles')
    # data_entry2 = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,db,int(shot),int(run)-1,str(user))
    # data_entry2.open()
    # equilibrium = data_entry2.get("equilibrium")
    equilibrium = data_entry.get("equilibrium")
    
    time_list = list(equilibrium.time)
    index = time_list.index(time/1000.0)

    curden = core_profiles.profiles_1d[index].j_total[:]
    curboot = core_profiles.profiles_1d[index].j_bootstrap[:]
    curohm = core_profiles.profiles_1d[index].j_ohmic[:]
    rhovn = equilibrium.time_slice[index].profiles_1d.j_parallel[:]
    press = equilibrium.time_slice[index].profiles_1d.pressure[:]
    q_value = equilibrium.time_slice[index].profiles_1d.q[:]
    qpsi = equilibrium.time_slice[index].profiles_1d.q[:]
    currf = core_profiles.profiles_1d[index].conductivity_parallel[:]
    curbeam = core_profiles.profiles_1d[index].current_parallel_inside[:]
    rho_grid = core_profiles.profiles_1d[index].phi_potential[:]
    
    data = {}
    
    data["curden"] = curden
    data["curboot"] = curboot
    data["curohm"] = curohm
    data["currf"] =currf
    data["curbeam"] = curbeam
    data["rhog_beam"] = rho_grid
    data["rho"] = rhovn
    data["q"] = qpsi

    return data

def draw(data):
    fs1 = 22
    fs2 = 18
    fs3 = 12
    font = {
        "family":"serif",
        "size":fs3
    }

    rho = np.array(data["rhog_beam"])
    J_tot = np.array(data["curden"])
    J_beam = np.array(data["curbeam"])
    J_boot = np.array(data["curboot"])
    J_ohm = np.array(data["curohm"])
    J_rf = np.array(data["currf"])


    fig = plt.figure(figsize=fig_size)
    plt.subplot(121)
    plt.plot(rho,J_tot/6e6,'-m',label="Tot")
    plt.plot(rho,J_beam/6e6,'-g',label="Beam")
    plt.plot(rho,J_boot/6e6,'-y',label="BS")
    plt.plot(rho,J_ohm/6e6,'-r',label="Ohmic")
    plt.plot(rho,J_rf/6e6,'-k',label="Rf")

    plt.legend(loc=0)
    plt.xlabel(r'$\rho$',font)
    plt.ylabel('$Jt(MA.m^{-2}$',font)

    q = data["q"]
    rho = data["rho"]
    plt.subplot(122)
    plt.plot(rho,q)
    plt.ylim([0,10])
    plt.plot(np.array([0,1]),np.array([2,2]),'--r')
    plt.plot(np.array([0,1]),np.array([1.5,1.5]),'--r')
    plt.plot(np.array([0,1]),np.array([1,1]),'--r')
    plt.yticks(np.linspace(1,9,9))
    plt.xticks()
    plt.xlabel(r'$\rho$',font)
    plt.ylabel(r'q',font)

    plt.close("all")

    return fig








# -----------------------------------ACT绘图---------------------------------------
class Var:
    user = ""
    db = ""
    struct = ""
    is_ids = ""
    shot = ""
    time = ""
    run = ""


SMALL_SIZE = 20
MEDIUM_SIZE = 25
BIGGER_SIZE = 30


def plotsub_1d(id, x, y, xl, yl):
    plt.subplot(id)
    plt.plot(x, y)
    plt.xlabel(xl)
    plt.ylabel(yl)
    return


def plotsub_1d_2(ax, x, y, x2, y2, xl, yl, l1, l2):
    # plt.subplot(id)
    ax.plot(x, y)
    ax.plot(x2, y2, "--")
    ax.set_xlabel(xl)
    ax.set_ylabel(yl)
    ax.legend([l1, l2])
    return


def plotsub_scatter(id, x, y, xl, yl, size=1):
    plt.subplot(id)
    plt.scatter(x, y, s=size)
    plt.xlabel(xl)
    plt.ylabel(yl)
    return


def plotsub_scatter_2(id, x, y, x2, y2, xl, yl, l1, l2):
    plt.subplot(id)
    plt.scatter(x, y, 8)
    plt.scatter(x2, y2, 4)
    plt.xlabel(xl)
    plt.ylabel(yl)
    plt.legend([l1, l2])
    return


def plotsub_contourf(ax, x, y, f, title,fig, lvl=60):
    # plt.subplot(id)
   
    vticks = np.linspace(f.min(), f.max(), lvl)
    c = ax.contour(x, y, f, levels=vticks, colors="k")
    ax.contourf(x, y, f, levels=vticks, vmin=f.min(), vmax=f.max())
    ax.set_xlabel("R (m)")
    ax.set_ylabel("Z (m)")
    ax.set_title(title)

    # plt.axis('equal')
    vticks = list(vticks)
    # ax.colorbar( mappable=c,ticks=vticks,format="%.3e")# ax=ax,
    
    



    # ax.colorbar()
    return 


def savesub_contourf(ax, x, y, f, title,fig, lvl=60):
    # plt.subplot(id)
   
    vticks = np.linspace(f.min(), f.max(), lvl)
    ax.contour(x, y, f, levels=vticks, colors="k")
    c = ax.contourf(x, y, f, levels=vticks, vmin=f.min(), vmax=f.max())
    ax.set_xlabel("R (m)")
    ax.set_ylabel("Z (m)")
    ax.set_title(title)

    # plt.axis('equal')
    vticks = list(vticks)
    plt.colorbar(mappable=c, ax=ax, ticks=vticks,format="%.3e")

    # ax.colorbar()
    return 

def plotsub_contour(id, x, y, f, title, lvl=60):
    plt.subplot(id)
    plt.contour(x, y, f, lvl)
    plt.xlabel("R (m)")
    plt.ylabel("Z (m)")
    plt.title(title)
    plt.axis("equal")
    plt.colorbar()
    return


def plot_fs(hf):
    name = [
        "f3",
        "f4",
        "f5",
        "f7",
        "f8",
        "f9",
        "f10",
        "f11",
        "f12",
        "f13",
        "f14",
        "f20",
        "f22",
    ]
    gp = "/map/"
    r = np.array(hf.get(gp + "r"))
    z = np.array(hf.get(gp + "z"))
    rlen = r.max() - r.min()
    zlen = z.max() - z.min()
    whr = rlen / zlen
    figh = 8
    figs = 1.5
    figw = (figh - figs) * whr + figs + 1.5

    for i in range(len(name)):
        f = np.array(hf.get(gp + name[i]))
        fig = plt.figure(figsize=(figw, figh))
        plotsub_contourf(111, r, z, f, name[i],fig, 10)
       
def plot_RZ(hf):
    is_ids = Var.is_ids
    if is_ids:
        mhd_linear, time = get_ids()
        r = np.array(
            mhd_linear.time_slice[0].toroidal_mode[0].plasma.mass_density_perturbed.real
        )
        z = np.array(
            mhd_linear.time_slice[0]
            .toroidal_mode[0]
            .plasma.mass_density_perturbed.imaginary[::]
        )
    else:
        gp = "/map/"
        r = np.array(hf.get(gp + "r"))
        z = np.array(hf.get(gp + "z"))

    rlen = r.max() - r.min()
    zlen = z.max() - z.min()
    whr = rlen / zlen
    figh = 16
    figs = 1.5
    figw = (figh - figs) * whr + figs + 1.5

    fig = plt.figure(figsize=fig_size, constrained_layout=True)
    plotsub_scatter(111, r, z, "R", "Z", 1)
    # plt.show()
    # pdf.add_page()
    # pdf.chapter_title("Contours of F")
    # pdf.image_plt(fig, pdf.get_x(), pdf.get_y(), min(190, figw * 220 / figh))
    plt.close("all")
    return fig


def plot_profile(hf):
    names = ["q", "f", "p", "ffp", "pp"]

    fig = plt.figure(figsize=fig_size)

    ax = []
    ax.append(plt.subplot2grid((3, 2), (0, 0)))
    ax.append(plt.subplot2grid((3, 2), (0, 1)))
    ax.append(plt.subplot2grid((3, 2), (1, 0)))
    ax.append(plt.subplot2grid((3, 2), (1, 1)))
    ax.append(plt.subplot2grid((3, 2), (2, 0)))

    for i in range(len(names)):
        s1, f1 = get_profile_s(hf, names[i])
        s2, f2 = get_profile_s_eq(hf, names[i])
        plotsub_1d_2(ax[i], s1, f1, s2, f2, "s", names[i], "map", "eqin")
    # plt.show()
    plt.close("all")
    return fig


def plot_ev_fft1(hf):

    nmax = 10

    s, m, fk = get_ef_fft2(hf, "xi01", nmax)
    whr = 1
    figh = 8
    figs = 1.5
    figw = (figh - figs) * whr + figs + 1.5

    fig = plt.figure(figsize=fig_size, constrained_layout=True)
    ax = []
    ax.append(plt.subplot2grid((2, 3), (0, 0)))
    ax.append(plt.subplot2grid((2, 3), (0, 1)))
    ax.append(plt.subplot2grid((2, 3), (0, 2)))
    ax.append(plt.subplot2grid((2, 3), (1, 0)))
    ax.append(plt.subplot2grid((2, 3), (1, 1)))
    ax.append(plt.subplot2grid((2, 3), (1, 2)))

    # plt.subplot(111)
    for i in range(nmax):
        ax[0].plot(s, fk.real[:, i], label="m = %d" % m[i])
    ax[0].set_xlabel(r"$s$")
    ax[0].set_ylabel(r"$Re(\frac{\xi\cdot\nabla\psi}{|\nabla\psi|})$")
    ax[0].set_title(r"$Re(\frac{\xi\cdot\nabla\psi}{|\nabla\psi|})$")
    ax[0].legend(prop = {'size':6})
    # ax[0].tight_layout()

    # pdf.image_plt(fig, pdf.get_x(), pdf.get_y(), min(190, figw * 220 / figh))

    # pdf.add_page()
    # fig = plt.figure()
    # plt.subplot(111)
    for i in range(nmax):
        ax[1].plot(s, fk.imag[:, i], label="m = %d" % m[i])
    ax[1].set_xlabel(r"$s$")
    ax[1].set_ylabel(r"$Im(\frac{\xi\cdot\nabla\psi}{|\nabla\psi|})$")
    ax[1].set_title(r"$Im(\frac{\xi\cdot\nabla\psi}{|\nabla\psi|})$")
    ax[1].legend(prop = {'size':6})
    # ax[1].tight_layout()
    # pdf.image_plt(fig, pdf.get_x(), pdf.get_y(), min(190, figw * 220 / figh))

    # pdf.add_page()
    # fig = plt.figure()
    # plt.subplot(111)
    for i in range(nmax):
        ax[2].plot(s, np.abs(fk[:, i]), label="m = %d" % m[i])
    ax[2].set_xlabel(r"$s$")
    ax[2].set_ylabel(r"$Norm(\frac{\xi\cdot\nabla\psi}{|\nabla\psi|})$")
    ax[2].set_title(r"$Norm(\frac{\xi\cdot\nabla\psi}{|\nabla\psi|})$")
    ax[2].legend(prop = {'size':6})
    # ax[2].tight_layout()
    # pdf.image_plt(fig, pdf.get_x(), pdf.get_y(), min(190, figw * 220 / figh))
    # plt.show()

    # fig = plt.figure()
    # plt.subplot(111)
    for i in range(nmax):
        ax[3].plot(s, fk.real[:, i], label="m = %d" % m[i])
    ax[3].set_xlabel(r"$s$")
    ax[3].set_ylabel(r"$Re(\xi\cdot\nabla\psi)$")
    ax[3].set_title(r"$Re(\xi\cdot\nabla\psi)$")
    ax[3].legend(prop = {'size':6})
    # ax[3].tight_layout()
    # pdf.image_plt(fig, pdf.get_x(), pdf.get_y(), min(190, figw * 220 / figh))

    # pdf.add_page()
    # fig = plt.figure()
    # plt.subplot(111)
    for i in range(nmax):
        ax[4].plot(s, fk.imag[:, i], label="m = %d" % m[i])
    ax[4].set_xlabel(r"$s$")
    ax[4].set_ylabel(r"$Im(\xi\cdot\nabla\psi)$")
    ax[4].set_title(r"$Im(\xi\cdot\nabla\psi)$")
    ax[4].legend(prop = {'size':6})
    # ax[4].tight_layout()
    # pdf.image_plt(fig, pdf.get_x(), pdf.get_y(), min(190, figw * 220 / figh))

    # pdf.add_page()
    # fig = plt.figure()
    # plt.subplot(111)
    for i in range(nmax):
        ax[5].plot(s, np.abs(fk[:, i]), label="m = %d" % m[i])
    ax[5].set_xlabel(r"$s$")
    ax[5].set_ylabel(r"$Norm(\xi\cdot\nabla\psi)$")
    ax[5].set_title(r"$Norm(\xi\cdot\nabla\psi)$")
    ax[5].legend(prop = {'size':6})
    # ax[5].tight_layout()
    plt.close("all")
    return fig


def plot_ev_fft2(hf):
    nmax = 10

    s, m, fk = get_ef_fft2(hf, "xi1", nmax)
    # s, m, fk = rd.get_ef_fft(hf, "xi1r", nmax)
    whr = 1
    figh = 8
    figs = 1.5
    figw = (figh - figs) * whr + figs + 1.5

    fig = plt.figure()
    plt.subplot(111)
    for i in range(nmax):
        plt.plot(s, fk.real[:, i], label="m = %d" % m[i])
    plt.xlabel(r"$s$")
    plt.ylabel(r"$Re(\xi\cdot\nabla\psi)$")
    plt.title(r"$Re(\xi\cdot\nabla\psi)$")
    plt.legend()
    plt.tight_layout()
    # pdf.image_plt(fig, pdf.get_x(), pdf.get_y(), min(190, figw * 220 / figh))

    # pdf.add_page()
    fig = plt.figure()
    plt.subplot(111)
    for i in range(nmax):
        plt.plot(s, fk.imag[:, i], label="m = %d" % m[i])
    plt.xlabel(r"$s$")
    plt.ylabel(r"$Im(\xi\cdot\nabla\psi)$")
    plt.title(r"$Im(\xi\cdot\nabla\psi)$")
    plt.legend()
    plt.tight_layout()
    # pdf.image_plt(fig, pdf.get_x(), pdf.get_y(), min(190, figw * 220 / figh))

    # pdf.add_page()
    fig = plt.figure()
    plt.subplot(111)
    for i in range(nmax):
        plt.plot(s, np.abs(fk[:, i]), label="m = %d" % m[i])
    plt.xlabel(r"$s$")
    plt.ylabel(r"$Norm(\xi\cdot\nabla\psi)$")
    plt.title(r"$Norm(\xi\cdot\nabla\psi)$")
    plt.legend()
    plt.tight_layout()
    # pdf.image_plt(fig, pdf.get_x(), pdf.get_y(), min(190, figw * 220 / figh))
    plt.show()


def plot_ev2d(hf):
    r, z = get_meshrz_ev(hf)
    rlen = r.max() - r.min()
    zlen = z.max() - z.min()
    whr = rlen / zlen
    figh = 8
    figs = 1.5
    figw = (figh - figs) * whr + figs + 1.5

    # pdf.add_page()
    # pdf.chapter_title("Contours of xi(r,z)")

    # pdf.section_title("Contours of Re[xi01(r,z)]")
    fig = plt.figure()
    f = get_ef(hf, "xi01r")
    plotsub_contourf(111, r, z, f, r"$Re(\frac{\xi\cdot\nabla\psi}{|\nabla\psi|})$",fig, 10)
    # pdf.image_plt(fig, pdf.get_x(), pdf.get_y(), min(190, figw * 220 / figh))

    # pdf.add_page()
    # pdf.section_title("Contours of Im[xi01(r,z)]")
    fig = plt.figure()
    f = get_ef(hf, "xi01i")
    plotsub_contourf(111, r, z, f, r"$Im(\frac{\xi\cdot\nabla\psi}{|\nabla\psi|})$",fig, 10)
    # pdf.image_plt(fig, pdf.get_x(), pdf.get_y(), min(190, figw * 220 / figh))
    plt.show()


def plot_ev_rzp(hf):
    dic_list = []
    
    r, z = get_meshrz_ev(hf)
    rlen = r.max() - r.min()
    zlen = z.max() - z.min()
    whr = rlen / zlen
    figh = 8
    figs = 1.5
    figw = (figh - figs) * whr + figs + 1.5
    phi = [0, 0.5 * math.pi, math.pi]


  
    fig_size= (5.04,3.45)
 
    fig00 = plt.figure(figsize=fig_size, constrained_layout=True)
    ax00 = []
    ax00.append(plt.subplot2grid((1, 1), (0, 0))) 
    f = get_ef_rzp(hf, "xi01", phi[0])
    plotsub_contourf(
        ax00[0], r, z, f, r"$Im(\frac{\xi\cdot\nabla\psi}{|\nabla\psi|})$",fig00, 10
    )
    
    fig01 = plt.figure(figsize=fig_size, constrained_layout=True)
    ax01 = []
    ax01.append(plt.subplot2grid((1, 1), (0, 0))) 
    f = get_ef_rzp(hf, "xi01",phi[0])
    savesub_contourf(
        ax01[0], r, z, f, r"$Im(\frac{\xi\cdot\nabla\psi}{|\nabla\psi|})$",fig01, 10
    )
    
    fig10 = plt.figure(figsize=fig_size, constrained_layout=True)
    ax10 = []
    ax10.append(plt.subplot2grid((1, 1), (0, 0))) 
    f = get_ef_rzp(hf, "xi01", phi[1])
    plotsub_contourf(
        ax10[0], r, z, f, r"$Im(\frac{\xi\cdot\nabla\psi}{|\nabla\psi|})$",fig10, 10
    )
    
    fig11 = plt.figure(figsize=fig_size, constrained_layout=True)
    ax11 = []
    ax11.append(plt.subplot2grid((1, 1), (0, 0))) 
    f = get_ef_rzp(hf, "xi01",phi[1])
    savesub_contourf(
        ax11[0], r, z, f, r"$Im(\frac{\xi\cdot\nabla\psi}{|\nabla\psi|})$",fig11, 10
    )
    
    fig20 = plt.figure(figsize=fig_size, constrained_layout=True)
    ax20 = []
    ax20.append(plt.subplot2grid((1, 1), (0, 0))) 
    f = get_ef_rzp(hf, "xi01", phi[2])
    plotsub_contourf(
        ax20[0], r, z, f, r"$Im(\frac{\xi\cdot\nabla\psi}{|\nabla\psi|})$",fig20, 10
    )
    
    fig21 = plt.figure(figsize=fig_size, constrained_layout=True)
    ax21 = []
    ax21.append(plt.subplot2grid((1, 1), (0, 0))) 
    f = get_ef_rzp(hf, "xi01",phi[2])
    savesub_contourf(
        ax21[0], r, z, f, r"$Im(\frac{\xi\cdot\nabla\psi}{|\nabla\psi|})$",fig21, 10
    )
    
    fig30 = plt.figure(figsize=fig_size, constrained_layout=True)
    ax30 = []
    ax30.append(plt.subplot2grid((1, 1), (0, 0))) 
    f = get_ef(hf, "xi01r")
    plotsub_contourf(
        ax30[0], r, z, f, r"$Im(\frac{\xi\cdot\nabla\psi}{|\nabla\psi|})$",fig30, 10
    )
    
    fig31 = plt.figure(figsize=fig_size, constrained_layout=True)
    ax31 = []
    ax31.append(plt.subplot2grid((1, 1), (0, 0))) 
    f = get_ef(hf, "xi01r")
    savesub_contourf(
        ax31[0], r, z, f, r"$Im(\frac{\xi\cdot\nabla\psi}{|\nabla\psi|})$",fig31, 10
    )
    
    fig40 = plt.figure(figsize=fig_size, constrained_layout=True)
    ax40 = []
    ax40.append(plt.subplot2grid((1, 1), (0, 0))) 
    f = get_ef(hf, "xi01i")
    plotsub_contourf(
        ax40[0], r, z, f, r"$Im(\frac{\xi\cdot\nabla\psi}{|\nabla\psi|})$",fig40, 10
    )
    
    fig41 = plt.figure(figsize=fig_size, constrained_layout=True)
    ax41 = []
    ax41.append(plt.subplot2grid((1, 1), (0, 0))) 
    f = get_ef(hf, "xi01i")
    savesub_contourf(
        ax41[0], r, z, f, r"$Im(\frac{\xi\cdot\nabla\psi}{|\nabla\psi|})$",fig41, 10
    )
    
    

    
    
    
    
    plt.close("all")
    
    return ([fig00,fig10,fig20,fig30,fig40],[fig01,fig11,fig21,fig31,fig41])


def plot2pdf(infile, outfile):
    hf = h5py.File(infile, "r")
    # pdf = PDF('Report of Mapping')
    SMALL_SIZE = 18
    MEDIUM_SIZE = 25
    BIGGER_SIZE = 25

    plt.rc("font", size=SMALL_SIZE)  # controls default text sizes
    plt.rc("axes", titlesize=SMALL_SIZE)  # fontsize of the axes title
    plt.rc("axes", labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
    plt.rc("xtick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc("ytick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc("legend", fontsize=SMALL_SIZE)  # legend fontsize
    plt.rc("figure", titlesize=BIGGER_SIZE)  # fontsize of the figure title

    plot_RZ(hf)
    plot_profile(hf)
    plot_ev_fft1(hf)
    plot_ev_fft2(hf)
    plot_ev_rzp(hf)
    plot_ev2d(hf)

    # plot_fs(pdf, hf)
    # pdf.output(outfile, 'F')
    hf.close()

    return


def help_msg():
    print("\tUsage: plt_map.py [-h] filename")


def perror_msg():
    print("Command Inline Parameters error!")
    help_msg()



def get_ids():

    user = Var.user
    db = Var.db
    shot = Var.shot
    run = Var.run
    time = Var.time

    data_entry = imas.DBEntry(
        imas.imasdef.MDSPLUS_BACKEND, db, int(shot), int(run), str(user)
    )
    data_entry.open()
    mhd_linear = data_entry.get("mhd_linear")
    time_list = list(mhd_linear.time)
    index = time_list.index(int(time)/1000.0)
    # data_entry.close()
    return mhd_linear, index


def get_meshrz_ev(file: h5py.File):
    is_ids = Var.is_ids
    if is_ids:
        mhd_linear, index = get_ids()
        r = np.array(
            mhd_linear.time_slice[index]
            .toroidal_mode[0]
            .vacuum.a_field_perturbed.coordinate3.imaginary
        )
        z = np.array(
            mhd_linear.time_slice[index]
            .toroidal_mode[0]
            .vacuum.a_field_perturbed.coordinate2.imaginary
        )
    else:
        r = np.array(file.get("/eigen/r"))
        z = np.array(file.get("/eigen/z"))

    return r, z


# ---------NULL----------#
def get_s(file: h5py.File):
    is_ids = Var.is_ids
    if is_ids:
        mhd_linear, index = get_ids()
        f = np.array(
            mhd_linear.time_slice[index]
            .toroidal_mode[0]
            .plasma.phi_potential_perturbed.imaginary[::]
        )
    else:
        f = np.array(file.get("/map/psi"))

    f = np.sqrt((f - f[0]) / (f[f.size - 1] - f[0]))
    return f


# ---------NULL--------------#
def get_profile_s(file: h5py.File, name: str):
    is_ids = Var.is_ids
    if is_ids:
        mhd_linear, index = get_ids()
        if name == "q":
            f = np.array(
                mhd_linear.time_slice[index].toroidal_mode[0].plasma.coordinate_system.z[::]
            )
        elif name == "f":
            f = np.array(
                mhd_linear.time_slice[index]
                .toroidal_mode[0]
                .plasma.coordinate_system.jacobian[::]
            )
        elif name == "p":
            f = np.array(
                mhd_linear.time_slice[index]
                .toroidal_mode[0]
                .plasma.psi_potential_perturbed.real[::]
            )
        elif name == "ffp":
            f = np.array(
                mhd_linear.time_slice[index]
                .toroidal_mode[0]
                .plasma.psi_potential_perturbed.imaginary[::]
            )
        elif name == "pp":
            f = np.array(
                mhd_linear.time_slice[index]
                .toroidal_mode[0]
                .plasma.phi_potential_perturbed.real[::]
            )

    else:

        f = np.array(file.get("/map/" + name))
    s = get_s(file)

    return s, f


##
def get_profile_s_eq(file: h5py.File, name: str):
    is_ids = Var.is_ids
    if is_ids:
        mhd_linear, index = get_ids()
        s = np.array(
            mhd_linear.time_slice[0].toroidal_mode[0].plasma.pressure_perturbed.real
        )
        if name == "q":
            f = np.array(
                mhd_linear.time_slice[index]
                .toroidal_mode[0]
                .plasma.temperature_perturbed.imaginary
            )
        elif name == "f":
            f = np.array(
                mhd_linear.time_slice[index]
                .toroidal_mode[0]
                .plasma.pressure_perturbed.imaginary
            )
        elif name == "p":
            f = np.array(
                mhd_linear.time_slice[index]
                .toroidal_mode[0]
                .vacuum.a_field_perturbed.coordinate1.real
            )
        elif name == "ffp":
            f = np.array(
                mhd_linear.time_slice[index]
                .toroidal_mode[0]
                .vacuum.a_field_perturbed.coordinate1.imaginary
            )
        elif name == "pp":
            f = np.array(
                mhd_linear.time_slice[index]
                .toroidal_mode[0]
                .plasma.temperature_perturbed.real
            )
    else:
        s = np.array(file.get("/eqin/psi"))
        f = np.array(file.get("/eqin/" + name))

    s = np.sqrt((s - s[0]) / (s[s.size - 1] - s[0]))

    return s, f


##
def get_ef(file: h5py.File, name: str):
    is_ids = Var.is_ids
    if is_ids:
        mhd_linear, index = get_ids()
        if name == "xi01r":
            f = np.array(
                mhd_linear.time_slice[index]
                .toroidal_mode[0]
                .plasma.displacement_perpendicular.real[::]
            )
        elif name == "xi01i":
            f = np.array(
                mhd_linear.time_slice[index]
                .toroidal_mode[0]
                .plasma.displacement_perpendicular.imaginary[::]
            )
        elif name == "xi03r":
            f = np.array(
                mhd_linear.time_slice[index]
                .toroidal_mode[0]
                .plasma.displacement_parallel.real[::]
            )
        elif name == "xi03i":
            f = np.array(
                mhd_linear.time_slice[index]
                .toroidal_mode[0]
                .plasma.displacement_parallel.imaginary[::]
            )
    else:
        fname = "/eigen/eigen0/" + name
        f = np.array(file.get(fname))
    return f


##
def get_ef_fft2(file: h5py.File, name: str, nmax: int):
    is_ids = Var.is_ids

    name1 = name + "r"
    fr = get_ef(file, name1)
    name1 = name + "i"
    fi = get_ef(file, name1)
    fc = fr + 1j * fi
    npsi = np.shape(fr)[0]
    nchi = np.shape(fi)[1]
    if is_ids:
        mhd_linear, index = get_ids()
        s = np.array(
            mhd_linear.time_slice[index]
            .toroidal_mode[0]
            .vacuum.a_field_perturbed.coordinate2.real[:, 0]
        )
    else:
        s = np.array(file.get("/eigen/psi")[:, 0])
 
    s = np.sqrt((s - s[0]) / (s[npsi - 1] - s[0]))

    fk = np.zeros([npsi, nchi], dtype=complex)
    for i in range(npsi):
        yk = fft(fc[i, :])
        fk[i, :] = fftshift(yk)

    xk = fftfreq(nchi, 1 / nchi)
    xk = fftshift(xk)
    max1 = np.nanmax(np.abs(fk), 0)

    fm = np.zeros([npsi, nmax], dtype=complex)
    ms = np.zeros(nmax)
    for i in range(nmax):
        n = np.argmax(max1)
        ms[i] = xk[n]
        fm[:, i] = fk[:, n]
        max1[n] = 0
    return s, ms, fm


# --------NULL----------#
def get_ef_rzp(file: h5py.File, name: str, phi: float):
    is_ids = Var.is_ids
    name1 = name + "r"
    fr = get_ef(file, name1)
    name1 = name + "i"
    fi = get_ef(file, name1)
    if is_ids:
        mhd_linear, index = get_ids()
        ntor = mhd_linear.time_slice[index].toroidal_mode[0].plasma.coordinate_system.r[0]
        # print(ntor)
    else:
        ntor = file.get("/eigen/ntor")[0]
    f = 2 * (fr * math.cos(ntor * phi) - fi * math.sin(ntor * phi))
    return f



def delete_dir(delete_path):
    '''
     作用: 删除本地目录
     参数：需要删除的目录
     返回：无
    '''
    path = pathlib.Path(delete_path)
    for i in path.glob("**/*"):
        # 删除文件
        if(os.path.exists(i)):
            if(os.path.isfile(i)):
                os.remove(i)
    
    # 将目录内容存为数组，方便排序
    a = []
    for i in path.glob("**/*"):
        a.append(str(i))
    
    # 降序排序后从内层开始删除
    a.sort(reverse = True)
    for i in a:
        # 删除目录
        if(os.path.exists(i)):
            if(os.path.isdir(i)):
                os.removedirs(i)

def read_R_Z():
    R_Z = {}
    ## 真空室 VV ##
    base=os.path.dirname(os.path.realpath(__file__))
    # base = get_sw_path_info()
   
    # sw_workflow_home = info['sw_workflow_home']
    f=open(base+'/input/HL2M-vv.txt')
    f.readline()
    R_inner=[]
    for i in range(119):
        R_inner.append(float(f.readline()))

    f.readline()
    Z_inner=[]
    for i in range(119):
        Z_inner.append(float(f.readline()))

    f.readline()
    R_outer=[]
    for i in range(119):
        R_outer.append(float(f.readline()))

    f.readline()
    Z_outer=[]
    for i in range(119):
        Z_outer.append(float(f.readline()))
    R_Z["R_inner1"] = R_inner
    R_Z["Z_inner1"] = Z_inner
    R_Z["R_outer1"] = R_outer
    R_Z["Z_outer1"] = Z_outer
    f.close()
    ## 边界 TF ##
    
    f=open(base+'/input/HL2M-TF.txt')

    f.readline()
    R_inner=[]
    for i in range(2200):
        R_inner.append(float(f.readline()))

    f.readline()
    Z_inner=[]
    for i in range(2200):
        Z_inner.append(float(f.readline()))

    f.readline()
    R_outer=[]
    for i in range(4000):
        R_outer.append(float(f.readline()))

    f.readline()
    Z_outer=[]
    for i in range(4000):
        Z_outer.append(float(f.readline()))
    R_Z["R_inner2"] = R_inner
    R_Z["Z_inner2"] = Z_inner
    R_Z["R_outer2"] = R_outer
    R_Z["Z_outer2"] = Z_outer
    return R_Z



# json解析
class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        """
        判断是否为bytes类型的数据是的话转换成str
        :param obj:
        :return:
        """
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)