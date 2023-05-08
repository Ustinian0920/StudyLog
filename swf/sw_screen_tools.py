# sw_screen_tools.py
# 大屏绘图函数

import json
import os
import numpy as np
import math
import imas
import getpass
import glob
from scipy.fft import fft, fftshift, fftfreq
from pathlib import Path

pi = math.pi

# 将字体放入/home/lianke/swswf/framework/server/util/input中在此导入
base=os.path.dirname(os.path.realpath(__file__))
digifaw_font_path = base+"/input/digifaw.ttf"
tnr_font_path = base+"/input/Times-New-Roman1.ttf"

#--------------------------HL-2M大屏绘图--------------------------------
# sw_screen_tools.py
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
# sw_screen_tools.py
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

# sw_screen_tools.py
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
    c = ax1.contour(GridR,GridZ,psirzp,np.linspace(1.1,5,contour_num*8),colors='#3dfffe',linewidths=0.8,alpha=0.6,zorder=1.1)# 1外围
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

# sw_screen_tools.py
# 绘制五个曲线图
def screen_draw_prof(ax2,ax3,ax4,ax5,ax6,limit_data,data,shot,time,is_defa):
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
    

 


    time_min,time_max =limit_data[0] 
    ax2_min,ax2_max = limit_data[1]
    ax3_min,ax3_max = limit_data[2]
    ax4_min,ax4_max = limit_data[3]
    ax5_min,ax5_max = limit_data[4]
    ax6_min,ax6_max = limit_data[5]

    time_list = data[0]
    ax2_y = data[1]
    ax3_y = data[2]
    ax4_y = data[3]
    ax5_y = data[4]
    ax6_y = data[5]

    
 
    
    if is_defa:
        ax2_min = ax2_min*1000
        ax2_max = ax2_max*1000
        ax2_y = [i*1000 for i in ax2_y]
    

    top_xlim = time_max
    bottom_xlim = time_min
    bottom_ylim = ax6_min
    top_ylim = ax6_max
    btw_ylim = top_ylim-bottom_ylim
    mid_ylim = (top_ylim+bottom_ylim)/2
    
    
    btw_xlim = top_xlim-bottom_xlim
    
    y_tick = [float(f%bottom_ylim),float(f%mid_ylim),float(f%top_ylim)]
    
   
    
    ax6.plot(time_list,ax6_y,col,linewidth=line_width)
    ax6.set_ylim(bottom_ylim-btw_ylim*0.05,top_ylim+btw_ylim*0.05)
    
    ax6.set_xlim(time_min,time_max)
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
  
    
    
    bottom_ylim = ax2_min
    top_ylim = ax2_max
    mid_ylim = (top_ylim+bottom_ylim)/2
    btw_ylim = top_ylim-bottom_ylim
   
    mid_xlim = (top_xlim+bottom_xlim)/2
    btw_xlim = top_xlim-bottom_xlim
    # x 和 y坐标的刻度值构造生成
    # x_tick = np.linspace(bottom_xlim,top_xlim,7,dtype=int)
    y_tick = [int(bottom_ylim),int(mid_ylim),int(top_ylim)]
    # 绘制曲线
    ax2.plot(time_list,ax2_y,col,linewidth=line_width)
    # y轴刻度值
    ax2.set_ylim(bottom_ylim-btw_ylim*0.05,top_ylim+btw_ylim*0.05)
    # x轴刻度值
    ax2.set_xlim(time_min,time_max)
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
    
    
    bottom_ylim = ax3_min
    top_ylim = ax3_max
    btw_ylim = top_ylim-bottom_ylim
    mid_ylim = (top_ylim+bottom_ylim)/2
    
   
    mid_xlim = (top_xlim+bottom_xlim)/2
    btw_xlim = top_xlim-bottom_xlim
    
    if bottom_ylim==top_ylim:
        y_tick = [mid_ylim-10,mid_ylim,mid_ylim+10]
    else:
        y_tick = [float(f%(bottom_ylim)),float(f%(mid_ylim)),float(f%(top_ylim))]
    # x_tick = np.linspace(bottom_xlim,top_xlim,7,dtype=int)
    
    ax3.plot(time_list,ax3_y,col,linewidth=line_width)
    ax3.set_xlim(time_min,time_max)
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
    
    
    
    bottom_ylim = ax4_min
    top_ylim = ax4_max
    btw_ylim = top_ylim-bottom_ylim
    mid_ylim = (top_ylim+bottom_ylim)/2
    
    y_tick = [float(f%(bottom_ylim)),float(f%(mid_ylim)),float(f%(top_ylim))]
    ax4.plot(time_list,ax4_y,col,linewidth=line_width)
    ax4.set_ylim(bottom_ylim-btw_ylim*0.05,top_ylim+btw_ylim*0.05)
    ax4.set_xlim(time_min,time_max)
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
   
    
    bottom_ylim =ax5_min
    top_ylim = ax5_max
    btw_ylim = top_ylim-bottom_ylim
    mid_ylim = (top_ylim+bottom_ylim)/2
    
    y_tick = [float(f%bottom_ylim),float(f%mid_ylim),float(f%top_ylim)]
    
    ax5.plot(time_list,ax5_y,col,linewidth=line_width)
    ax5.set_ylim(bottom_ylim-btw_ylim*0.05,top_ylim+btw_ylim*0.05)
    ax5.set_xlim(time_min,time_max)
    ax5.set_ylabel(ax5_lb,font=Path(tnr_font_path),color="white",fontsize=font_size)
    ax5.set_xticks(x_tick)
    ax5.set_xticklabels(x_tick,color="#000105")
    ax5.set_yticks(y_tick)
    y_tick = [float(f%(bottom_ylim)),float(f%(mid_ylim)),float(f%(top_ylim))]
    ax5.set_yticklabels(y_tick,fontsize=tick_size)
    ax5.grid(True,color="#00FFFB",linestyle='--',alpha=grid_alpha)
    


#--------------------------绘图工具函数--------------------------------

# sw_screen_tools.py
# 读取装置数据
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

# sw_screen_tools.py
# 返回目录的 所有全为数字的子文件名
def get_file_name(path):
    file_name_list = []
    file_list = os.listdir(path)
    for file_name in file_list:
        if file_name.isdigit():
            file_name_list.append(file_name)
    file_name_list.sort()
    return file_name_list

# sw_screen_tools.py
# 构建shot
def built_shot(shot):
    shot = "%06d"%int(shot)
    return shot

# sw_screen_tools.py
# 构建time
def built_time(time): 
    time = "%05d"%int(time)
    return time

# sw_screen_tools.py
# 坐标系调整
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
      
# sw_screen_tools.py  
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

# sw_screen_tools.py
# IMAS路径解析
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

# sw_screen_tools.py
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