# sw_draw_hl2m_screen.py
# HL-2M可视化大屏，数据读取与图像绘制

import sys
import re 
import os
module_path=os.path.join(os.path.dirname(os.path.realpath(__file__)),"module")
sys.path.append(module_path)
framework_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__))+"/../")
sys.path.append(framework_path)
import matplotlib.pyplot as plt
from sw_screen_tools import *
import time as tm
import matplotlib.animation as anime
import multiprocessing as mp
from PIL import Image
from io import BytesIO, TextIOWrapper
import imageio.v2 as imageio
from data_parser import ParserFactory,SWMapper
user = os.environ.get("USER")
 
# 读取单个afile
def read_a_(afile_path):
    parser = ParserFactory.getParser("afile", afile_path)
    # 转字典
    afile_data = parser.read().toDict()
    return afile_data

# 读取单个Gfile
def read_g_(gfile_path):
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

# 伪造数据
def biult_data():
    R_Z = read_R_Z()

    limit_data = []
    data = []
    for i in range(6):
        inner_data = range(10)
        inner_limit_data = [0,9]
        if i == 2:
            inner_data = np.linspace(150,200,10)
            inner_limit_data = [150,200]
        if i == 3:
            inner_data = np.linspace(40,75,10)
            inner_limit_data = [40,75]
        limit_data.append(inner_limit_data)
        data.append(inner_data)
    shot = 36000
    time = 10

    return limit_data,data,shot,time,R_Z

# 颜色设置
def set_color(fig,ax1,ax2,ax3,ax4,ax5,ax6):

    # 边框的颜色
    c_border = "#00FFFB"
    # 刻度线颜色
    c_tick = "#00FFFB"
    # 图的背景颜色
    c_bg = "#000105"
    # 画布背景颜色
    plt.rcParams['axes.facecolor']='#000105'

    axs = [ax1,ax2,ax3,ax4,ax5,ax6]

    line_width=2
    fig.patch.set_facecolor(c_bg)
    for ax in axs:
        directions = ["right","left","top","bottom"]
        for direction in directions:
            ax.spines[direction].set_color(c_border)
            ax.spines[direction].set_linewidth(line_width)
        ax.tick_params(axis='x',colors=c_tick)
        ax.tick_params(axis='y',colors=c_tick)
        ax.patch.set_color(c_bg)

# 初始化fig和axs
def init_fig():
    fig = plt.figure(figsize=(10.4,6.08),dpi=100)#10.4
    plt.subplots_adjust(top = 0.98, bottom = 0, right = 1, left = 0, hspace=0.5,wspace=0.28)
    plt.margins(0,0)
    ax1 = plt.subplot2grid((58,128),(0,10),rowspan=53,colspan=38)
    ax2 = plt.subplot2grid((58,128),(4,70),rowspan=9,colspan=49)#54 46
    ax3 = plt.subplot2grid((58,128),(14,70),rowspan=9,colspan=49)# 49
    ax4 = plt.subplot2grid((58,128),(24,70),rowspan=9,colspan=49)
    ax5 = plt.subplot2grid((58,128),(34,70),rowspan=9,colspan=49)
    ax6 = plt.subplot2grid((58,128),(44,70),rowspan=9,colspan=49)
    return fig,ax1,ax2,ax3,ax4,ax5,ax6

# 主函数
def main(g_draw):
    
    gfile_data = read_g_("/Users/lianke/Desktop/StudyLog/swf/036000/00310/g036000.00310")

    fig,ax1,ax2,ax3,ax4,ax5,ax6 = init_fig()

    set_color(fig,ax1,ax2,ax3,ax4,ax5,ax6)
    limit_data,data,shot,time,R_Z = biult_data()
    if g_draw=="2A":
        screen_Draw_2A_stru_bg(ax1)
    else:
        screen_Draw_2M_stru_bg(ax1,R_Z)
    screen_draw_psi_fig(ax1,gfile_data,g_draw,"12311")
    screen_draw_prof(ax2,ax3,ax4,ax5,ax6,limit_data,data,shot,time,False)

    fig.align_ylabels()
    plt.show()

if __name__ == "__main__":
    main("2A")