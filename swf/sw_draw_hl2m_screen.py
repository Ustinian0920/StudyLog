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
from util.sw_screen_tools import *
from db import SwDB
import time as tm
import matplotlib.animation as anime
import multiprocessing as mp
from PIL import Image
from io import BytesIO, TextIOWrapper
import imageio.v2 as imageio
import sw_ftp_hl2m_screem_gif
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

# # 背景颜色和xy左边颜色设置
def set_color(fig,ax1,ax2,ax3,ax4,ax5,ax6,c_border,c_tick,c_bg):
    line_width=2
    fig.patch.set_facecolor(c_bg)
    ax1.spines['right'].set_color(c_border)
    ax1.spines['left'].set_color(c_border)
    ax1.spines['top'].set_color(c_border)
    ax1.spines['bottom'].set_color(c_border)
    ax1.spines['right'].set_linewidth(line_width)
    ax1.spines['left'].set_linewidth(line_width)
    ax1.spines['top'].set_linewidth(line_width)
    ax1.spines['bottom'].set_linewidth(line_width)
    
    ax1.tick_params(axis='x',colors=c_tick)
    ax1.tick_params(axis='y',colors=c_tick)
    
    ax2.spines['right'].set_color(c_border)
    ax2.spines['left'].set_color(c_border)
    ax2.spines['top'].set_color(c_border)
    ax2.spines['bottom'].set_color(c_border)
    ax2.spines['right'].set_linewidth(line_width)
    ax2.spines['left'].set_linewidth(line_width)
    ax2.spines['top'].set_linewidth(line_width)
    ax2.spines['bottom'].set_linewidth(line_width)

    ax2.tick_params(axis='x',colors=c_tick)
    ax2.tick_params(axis='y',colors=c_tick)
    
    ax3.spines['right'].set_color(c_border)
    ax3.spines['left'].set_color(c_border)
    ax3.spines['top'].set_color(c_border)
    ax3.spines['bottom'].set_color(c_border)
    ax3.spines['right'].set_linewidth(line_width)
    ax3.spines['left'].set_linewidth(line_width)
    ax3.spines['top'].set_linewidth(line_width)
    ax3.spines['bottom'].set_linewidth(line_width)

    ax3.tick_params(axis='x',colors=c_tick)
    ax3.tick_params(axis='y',colors=c_tick)
    
    ax4.spines['right'].set_color(c_border)
    ax4.spines['left'].set_color(c_border)
    ax4.spines['top'].set_color(c_border)
    ax4.spines['bottom'].set_color(c_border)
    ax4.spines['right'].set_linewidth(line_width)
    ax4.spines['left'].set_linewidth(line_width)
    ax4.spines['top'].set_linewidth(line_width)
    ax4.spines['bottom'].set_linewidth(line_width)

    ax4.tick_params(axis='x',colors=c_tick)
    ax4.tick_params(axis='y',colors=c_tick)
    
    ax5.spines['right'].set_color(c_border)
    ax5.spines['left'].set_color(c_border)
    ax5.spines['top'].set_color(c_border)
    ax5.spines['bottom'].set_color(c_border)
    ax5.spines['right'].set_linewidth(line_width)
    ax5.spines['left'].set_linewidth(line_width)
    ax5.spines['top'].set_linewidth(line_width)
    ax5.spines['bottom'].set_linewidth(line_width)

    ax5.tick_params(axis='x',colors=c_tick)
    ax5.tick_params(axis='y',colors=c_tick)
    
    ax6.spines['right'].set_color(c_border)
    ax6.spines['left'].set_color(c_border)
    ax6.spines['top'].set_color(c_border)
    ax6.spines['bottom'].set_color(c_border)
    ax6.spines['right'].set_linewidth(line_width)
    ax6.spines['left'].set_linewidth(line_width)
    ax6.spines['top'].set_linewidth(line_width)
    ax6.spines['bottom'].set_linewidth(line_width)

    ax6.tick_params(axis='x',colors=c_tick)
    ax6.tick_params(axis='y',colors=c_tick)

# 绘制单个图
def draw_image(
                shot,
                time,
                fig,ax1,ax2,ax3,ax4,ax5,ax6,
                color_list,
                gfile_data,
                limit_data,data
               ):
        # print(time)
        lab = ""
        struct = "2M"
        screen_Draw_2M_stru_color_block(ax1,color_list=color_list)
        

        # 绘图 
        screen_draw_psi_fig(ax1,gfile_data,struct,lab)
        screen_draw_prof(ax2,ax3,ax4,ax5,ax6,limit_data,data,shot,time,False)
        # 对齐ylabel
    #     # 对齐ylabel
        fig.align_ylabels()
        buf = BytesIO()
        plt.savefig(buf,bbox_inches = 'tight')
        tmp_shot_path = server_path+f"/static/tmp/{shot}/"
        if not os.path.exists(tmp_shot_path):
            os.makedirs(tmp_shot_path)
        png_path = tmp_shot_path+f"{shot}_{time}.png"
        plt.savefig(png_path,bbox_inches = 'tight')
        frame = imageio.imread(buf)
        buf.close()
        plt.clf()
        return frame
       

R_Z = read_R_Z()

server_path = f"/home/{user}/swswf"
metadata = dict(title="Movie", artist="sourabh")
writer = anime.PillowWriter(fps=5, metadata=metadata)

g_fig = None
g_ax1 = None
g_ax2 = None 
g_ax3 = None
g_ax4 = None 
g_ax5 = None
g_ax6 = None 

      
def draw(shot):
    
    # 边框的颜色
    c_border = "#00FFFB"
    # 刻度线颜色
    c_tick = "#00FFFB"
    # 图的背景颜色
    c_bg = "#000105"
    # 画布背景颜色
    plt.rcParams['axes.facecolor']='#000105'

    print("开始绘制:",shot)
    time_start = tm.time()  # 记录开始时间
    # 每一帧持续的时间
    duration = 0.2
    shot_str = built_shot(shot)
        # 获取工作路径
   
    efit_path = f"/home/{user}/swswf/workflow/data/EFIT_FIT/out/{shot_str}/"
    json_path = efit_path+shot_str+".json"
   
   
    # 新建tmp目录下的tmp_gif,tmp_json文件夹
    source_time_list = get_file_name(efit_path) 
    #---------------------------------------绘制并返回数据----------------------------------------------------
    

    # 获取绘图数据
    shot = int(shot)
    shot_str = built_shot(shot)
    afile_data_list = []
    gfile_data_list = []
    colors_list = []
    time_list = []

    data = [[],[],[],[],[],[]]
    limit_data = [[],[],[],[],[],[]]

    
    # 读取json
    with open(json_path, 'r') as f:
        str_json = f.read()
        json_data = json.loads(str_json)

    # 获取数据
    for i,time in enumerate(source_time_list):

        # 获取afile gfile数据
        time_str = built_time(time)
        afile_path = efit_path+time_str+"/a"+shot_str+"."+time_str
        gfile_path = efit_path+time_str+"/g"+shot_str+"."+time_str
        if not os.path.exists(afile_path) or not os.path.exists(gfile_path):
            continue
        afile_data = read_a_(afile_path)
        afile_data_list.append(afile_data)
        gfile_data = read_g_(gfile_path)
        gfile_data_list.append(gfile_data)


        # 获取颜色数据
        colors = []
        if 'color_block' in json_data.keys():
            PF = json_data["color_block"]
            PF_keys = ["PF1L","PF2L","PF3L","PF4L","PF5L","PF6L","PF7L","PF8L","I_CS_1a_2M"]
            
            for PF_key in PF_keys:
                pf_l_key_len = len(PF[PF_key])
                color = "white"
                if i < pf_l_key_len:
                    if PF[PF_key][i]>=0.1:
                        color = "red"
                    elif -0.1<PF[PF_key][i]<0.1:
                        color = "white"
                    else:
                        color = "blue"
                colors.append(color)
        else:
            for index in range(9):
                colors.append("white")
        lab = ""
        colors_list.append(colors)

        # 能读到数据的所有time
        time_list.append(int(time))

        data[0] = time_list
        data[1] = json_data["Yact"]
        data[2].append(afile_data["rout"])
        data[3].append(afile_data["aout"])
        data[4].append(afile_data["eout"])
        data[5].append((afile_data["doutu"]+afile_data["doutl"])/2)

    # 获取每个list的最大值和最小值
    for i in range(6):
        limit_data[i].append(min(data[i]))
        limit_data[i].append(max(data[i]))

    #--------------new---------------------------------
    
    gif_name = f"current_2m_screen_{shot}.gif"
    gif_path = server_path+"/static/"+gif_name
   
    global g_fig
    global g_ax1
    global g_ax2,g_ax3,g_ax4,g_ax5,g_ax6
    
    if g_fig:
        fig = g_fig
    else:
        fig = plt.figure(figsize=(11,6.08),dpi=100)#10.4
        plt.subplots_adjust(top = 0.98, bottom = 0, right = 1, left = 0, hspace=0.5,wspace=0.28)
        plt.margins(0,0)
        g_fig = fig
    
    ax1 = plt.subplot2grid((58,128),(0,10),rowspan=53,colspan=38)
    
    if g_ax2:
        ax2 = g_ax2
    else:
        ax2 = plt.subplot2grid((58,128),(4,70),rowspan=9,colspan=46)#54 46
        g_ax2 = ax2
        
    if g_ax3:
        ax3 = g_ax3
    else:
        ax3 = plt.subplot2grid((58,128),(14,70),rowspan=9,colspan=46)# 49
        g_ax3 = ax3
        
    if g_ax4:
        ax4 = g_ax4
    else:
        ax4 = plt.subplot2grid((58,128),(24,70),rowspan=9,colspan=46)
        g_ax4 = ax4
     
    if g_ax5:
        ax5 = g_ax5
    else:
        ax5 = plt.subplot2grid((58,128),(34,70),rowspan=9,colspan=46)
        g_ax5 = ax5  
    
    if g_ax6:
        ax6 = g_ax6
    else:
        ax6 = plt.subplot2grid((58,128),(44,70),rowspan=9,colspan=46)
        g_ax6 = ax6

    
    set_color(fig,ax1,ax2,ax3,ax4,ax5,ax6,c_border,c_tick,c_bg)


    ax1 = screen_Draw_2M_stru_bg(ax1,R_Z=R_Z)
    max_cpu = mp.cpu_count()
    cpu_num = 10
    if cpu_num > max_cpu -1:
        cpu_num = max_cpu - 1
    
    pool = mp.Pool(processes=cpu_num)
    frames = []
    result = []


    # ----------------绘图----------------------------
    for i,time in enumerate(time_list):
        current_data = [[],[],[],[],[],[]]
        time_str = built_time(time)
        color_list = colors_list[i]
        gfile_data = gfile_data_list[i]

        for index in range(6):
            current_data[index] = data[index][:i+1]

            # 绘图 
        p =  pool.apply_async(draw_image,(
                shot,
                time,
                fig,ax1,ax2,ax3,ax4,ax5,ax6,
                color_list,
                gfile_data,
                limit_data,current_data))
        
        result.append(p)
        
    pool.close()
    pool.join()
    print("times :",len(time_list))
    for i in result:
        img = i.get()
        frames.append(img)
    pool.terminate()
    if len(frames) > 1:
        print("生成gif...")
        imageio.mimsave(gif_path, frames, 'GIF', duration=0.2)       
        dic = {}
        dic["speed"] = duration
        dic["shot"] = str(shot)
        with open(server_path+"/static/"+"current_2m_screen.json", 'w') as f:
            dic["url"] = f"/static/{gif_name}"
            dic["time_list"] = []
            json.dump(dic, f)
        SwDB.set_das_current_shot(shot,1,1,1)
        sw_ftp_hl2m_screem_gif.upload(shot)
    time_end = tm.time()
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    print("time_sum",time_sum)
    



if __name__ == '__main__':
    # draw(1525)
    # print("第一次绘制")
    draw(1579)
    # print("以后第二次绘制")
    # draw(1260)
    # print("以后第三次绘制")
    # draw(1260)