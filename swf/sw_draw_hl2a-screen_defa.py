import sys
import re 
import os
module_path=os.path.join(os.path.dirname(os.path.realpath(__file__)),"module")
sys.path.append(module_path)
framework_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__))+"/../")
sys.path.append(framework_path)

from sw_viewer_tools import *
import time as tm
import matplotlib.animation as anime
import multiprocessing as mp
from PIL import Image
from io import BytesIO, TextIOWrapper
import imageio.v2 as imageio
from matplotlib import font_manager
# 读取单个Afile
def read_a_(afile_path):
    from data_parser import ParserFactory,SWMapper
    parser = ParserFactory.getParser("afile", afile_path)
    # 转字典
    afile_data = parser.read().toDict()
    
 
    return afile_data
def get_defa_data_path(shot_str):
    path = os.path.dirname(os.path.realpath(__file__))+"/"+shot_str+"/"
    return path
def read_a_json(json_path):
    with open(json_path, 'r') as f:
        str_json = f.read()
        json_data = json.loads(str_json)
    
    afile_data = {}

    afile_data["X"] = json_data["X"]
    afile_data["Yact"] = json_data["Yact"]
    afile_data["rout"] = json_data["R0"]
    afile_data["aout"] = json_data["a"]
    afile_data["eout"] = json_data["k"]
    afile_data["color_block"] = json_data["color_block"]
    return afile_data
# 读取单个Gfile
def read_g_(gfile_path):
   
        
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


# 读取HL2M-TF和HL2M-vv绘图数据
R_Z = read_R_Z()

server_path = os.path.dirname(os.path.realpath(__file__))
metadata = dict(title="Movie", artist="sourabh")
writer = anime.PillowWriter(fps=5, metadata=metadata)
print(f"server_path{server_path}")
      

def draw_image(
                shot,
                time,
                fig,ax1,ax2,ax3,ax4,ax5,ax6,
                color_list,
                gfile_data,
                current_json_data,json_data,current_afile_data_list,afile_data_list,current_time_list,max_time_list,
               ):
        
        # print(time)
        lab = ""
        struct = "2M"
        
        b_list = screen_Draw_2M_stru_color_block(ax1,color_list=color_list)
        

        # 绘图 
        c_list = screen_draw_psi_fig(ax1,gfile_data,struct,lab)
        screen_draw_prof(ax2,ax3,ax4,ax5,ax6,current_json_data,json_data,current_afile_data_list,afile_data_list,current_time_list,max_time_list,shot,time,True)
        # 对齐ylabel
    #     # 对齐ylabel
        fig.align_ylabels()
        buf = BytesIO()
        plt.savefig(buf,bbox_inches = 'tight')
        frame = imageio.imread(buf)
        buf.close()
        plt.clf()
        return frame
       

g_fig = None
g_ax1 = None
g_ax2 = None 
g_ax3 = None
g_ax4 = None 
g_ax5 = None
g_ax6 = None 

                
def draw(shot):
   
    print("开始绘制:",shot)
    time_start = tm.time()  # 记录开始时间
    # 提取数据
    png_path_list = []
    # 每一帧持续的时间
    duration = 0.2
  
    
    shot_str = built_shot(shot)
        # 获取工作路径
   
    static_path = os.path.join(server_path,"static")
    # for f in os.listdir(static_path):
    #     m = re.match(r'current_2m_screen_\d+\.gif',f)
    #     if m:
    #         f_path = os.path.join(static_path,f)
    #         os.remove(f_path)
    #         print("clean:",f)
    
    efit_path = os.path.abspath(os.path.join(os.path.join(server_path,os.path.pardir),os.path.pardir))+"/workflow/data/EFIT_FIT/out/"+shot_str+"/"
    
    json_path = efit_path+shot_str+".json"
    struct = "2M"
    # 当前时间片列表
    current_afile_data_list = []
    max_time_list = []
    current_json_data = {"X":[],"Yact":[]}
   
    # 新建tmp目录下的tmp_gif,tmp_json文件夹
    time_list = get_file_name(efit_path) 
    #---------------------------------------绘制并返回数据----------------------------------------------------
    

    # 获取绘图数据
    shot = int(shot)
    shot_str = built_shot(shot)
    afile_data_list = []
    current_time_list = []
    current_afile_data_list = []
    max_time_list = []
    current_json_data = {"X":[],"Yact":[]}
    for time in time_list:
        max_time_list.append(int(time))
    # 读取json和afile
    with open(json_path, 'r') as f:
        str_json = f.read()
        json_data = json.loads(str_json)
    for time in time_list:
        time_str = built_time(time)
        afile_path = efit_path+time_str+"/a"+shot_str+"."+time_str
        if not os.path.exists(afile_path):
            print(afile_path)
            continue
        afile_data = read_a_(afile_path)
        afile_data_list.append(afile_data)
    #--------------new---------------------------------
    # 修改背景颜色
    plt.rcParams['axes.facecolor']='#000105'
    gif_name = f"default_2m_screen.gif"
    gif_path = server_path+"/static/"+gif_name
   
    global g_fig
    global g_ax1
    global g_ax2,g_ax3,g_ax4,g_ax5,g_ax6
    
    if g_fig:
        fig = g_fig
    else:
        fig = plt.figure(figsize=(10.4,6.08),dpi=100)#10.4
        plt.subplots_adjust(top = 0.98, bottom = 0, right = 1, left = 0, hspace=0.5,wspace=0.28)
        plt.margins(0,0)
        g_fig = fig
        print("已经生成了fig")
    
    # 下面的也可以像fig一样处理,但是需要清理绘图
    # if g_ax1 :
    #     ax1 = g_ax1
    #     print("已经生成过 ax1")
    # else:
    #     ax1 = plt.subplot2grid((58,128),(0,10),rowspan=52,colspan=42)
    #     g_ax1 = ax1
        # ax1 = plt.subplot2grid((58,128),(4,70),rowspan=9,colspan=46)#54 46
        
    ax1 = plt.subplot2grid((58,128),(0,10),rowspan=53,colspan=38)
    
    if g_ax2:
        ax2 = g_ax2
    else:
        ax2 = plt.subplot2grid((58,128),(4,70),rowspan=9,colspan=49)#54 46
        g_ax2 = ax2
        
    if g_ax3:
        ax3 = g_ax3
    else:
        ax3 = plt.subplot2grid((58,128),(14,70),rowspan=9,colspan=49)# 49
        g_ax3 = ax3
        
    if g_ax4:
        ax4 = g_ax4
    else:
        ax4 = plt.subplot2grid((58,128),(24,70),rowspan=9,colspan=49)
        g_ax4 = ax4
     
    if g_ax5:
        ax5 = g_ax5
    else:
        ax5 = plt.subplot2grid((58,128),(34,70),rowspan=9,colspan=49)
        g_ax5 = ax5  
    
    if g_ax6:
        ax6 = g_ax6
    else:
        ax6 = plt.subplot2grid((58,128),(44,70),rowspan=9,colspan=49)
        g_ax6 = ax6


    


    # 
    # 
    # 
   
    # # 颜色设置
    axs = [ax1,ax2,ax3,ax4,ax5,ax6]
    def set_color(c_border,c_tick,c_bg):
        line_width=2
        fig.patch.set_facecolor(c_bg)
        for ax in axs:
            directions = ["right","left","top","bottom"]
            for direction in directions:
                ax.spines[direction].set_color(c_border)
                ax.spines[direction].set_linewidth(line_width)
            ax.tick_params(axis='x',colors=c_tick)
            ax.tick_params(axis='y',colors=c_tick)
        

    c_border = "#00FFFB"#0591ff
    c_tick = "#00FFFB"
    c_bg = "#000105"
    set_color(c_border,c_tick,c_bg)
    ax1 = screen_Draw_2M_stru_bg(ax1,R_Z=R_Z)
    time_len = len(time_list)
    max_cpu = mp.cpu_count()
    print("cpu:",max_cpu)
    cpu_num = 10
    if cpu_num > max_cpu -1:
        cpu_num = max_cpu - 1
    
    pool = mp.Pool(processes=cpu_num)
    frames = []
    result = []
    for i,time in enumerate(time_list):
        time_str = built_time(time)
        
        gfile_path = efit_path+time_str+"/g"+shot_str+"."+time_str
        if not os.path.exists(gfile_path):
            print(afile_path)
            continue
        gfile_data = read_g_(gfile_path)
        
        # 大于0:红色
        # 等于0:白色
        # 小于0:蓝色
        color_list = []
        if 'color_block' in json_data.keys():
            PF = json_data["color_block"]
            PF_keys = PF.keys()
            
            for PF_key in PF_keys:
                if PF[PF_key][i]>=0.5:
                    color = "red"
                elif -0.5<PF[PF_key][i]<0.5:
                    color = "white"
                else:
                    color = "blue"
                color_list.append(color)
        else:
            for index in range(9):
                color_list.append("white")
        lab = ""
        # lab='shot:'+str(shot)+'  time:'+str(int(gfile_path[-5:]))#label shot:36000 time:300
        # fig,ax1,ax2,ax3,ax4,ax5,ax6=screen_Draw_2M_stru(figsize=(12.24,7.68),dpi=100,color_list=color_list,R_Z=R_Z)
        current_time_list.append(int(time))
        current_afile_data_list.append(afile_data_list[i])
        current_json_data["X"].append(json_data["X"][i])
        current_json_data["Yact"].append(json_data["Yact"][i])
            # 绘图 
        p =  pool.apply_async(draw_image,(
            shot,
            time,
            fig,ax1,ax2,ax3,ax4,ax5,ax6,
            color_list,
            gfile_data,
            current_json_data,
            json_data,
            current_afile_data_list,
            afile_data_list,
            current_time_list,
            max_time_list,))
        
        result.append(p)
        
    pool.close()
    pool.join()
    print("times :",len(time_list))
    print(len(result))
    for i in result:
        img = i.get()
        frames.append(img)
    print(len(frames))
    pool.terminate()
    if len(frames) > 1:
        print("生成gif...")
        imageio.mimsave(gif_path, frames, 'GIF', duration=0.2)       
        dic = {}
        dic["speed"] = duration
        dic["shot"] = str(shot)
        with open(server_path+"/static/"+"default_2m_screen.json", 'w') as f:
            dic["url"] = f"/static/{gif_name}"
            dic["time_list"] = time_list
            json.dump(dic, f)
    time_end = tm.time()
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    print("time_sum",time_sum)


if __name__ == '__main__':
    #draw(1260)
    print("第一次绘制")
    draw(36000)
    # a = sorted([f.name for f in matplotlib.font_manager.fontManager.ttflist])
    # for index,i in enumerate(a):
    #     print(i)
    #     if i=="Times New Roman":
    #         print(i)
    #         break
    
    
    # print("以后第二次绘制")
    # draw(1260)
    # print("以后第三次绘制")
    # draw(1260)