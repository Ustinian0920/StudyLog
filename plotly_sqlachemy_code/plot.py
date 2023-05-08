import plotly as py
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json
from plotly.subplots import make_subplots
import re
def plot_scatter_line():
    data1 = {
        'x':[1,2,3,4],
        'y':[16,5,11,9],
        'type':'scatter'
    }
    data2 = {
        'x':[1,2,3,4],
        'y':[10,15,13,17],
        'type':'scatter'
    }
    data =[data1,data2]
    layout = go.Layout(
        title='折线图可视化作图',
    )
    fig = go.Figure(data=data, layout=layout)
    return fig

def f(x, y):
    return (1 - x / 2 + x ** 5 + y ** 3) * np.exp(-x ** 2 -y ** 2)

def plot_subplots():
    # 定义等高线高度函数

    # 数据数目
    n = 256
    # 定义x, y
    x = np.linspace(-3, 3, n)
    y = np.linspace(-3, 3, n)

    # 生成网格数据
    X, Y = np.meshgrid(x, y)

    z=f(X,Y)
    print(np.shape(z))
    print(len(z))
    print(len(z[0]))
    fig = make_subplots(rows=2, cols=2,
        start_cell="bottom-left", # 'bottom-left', 'top-left
        vertical_spacing=0.2,
        subplot_titles=["子图1","","子图3","子图4"],  # 每个子图的名字
        specs=[[{"type": "xy"}, {"type": "polar"}],
           [{"type": "contour"}, {"type": "scene"}]],  # 通过type来指定类型
    )  

    fig.add_trace(go.Bar(y=[2, 3, 1]),
                row=1,col=1)

    fig.add_trace(go.Barpolar(theta=[0, 45, 90], r=[2, 3, 1]),
                row=1,col=2)

    fig.add_trace(go.Contour(x=x,y=y,z=z),
                row=2,col=1)

    fig.add_trace(go.Scatter3d(x=[1,2,3], y=[1,2,3],
                            z=[0.5, 1, 2], mode="lines"),
                row=2,col=2)

    # 自定义x轴
    fig.update_xaxes(title_text="xaxis—1 标题", row=1, col=1)  # 正常显示
    fig.update_xaxes(title_text="xaxis-2 标题", range=[10, 50], row=1, col=2)  # 设置范围range
    fig.update_xaxes(title_text="xaxis-3 标题", showgrid=False, row=2, col=2)  # 不显示网格线

    # 自定义y轴
    fig.update_yaxes(title_text="yaxis 1 标题", row=1, col=1)
    fig.update_yaxes(title_text="yaxis 2 标题", range=[40, 80], row=1, col=2)
    fig.update_yaxes(title_text="yaxis 3 标题", showgrid=False, row=2, col=2)

    fig.update_layout(height=600, 
                    width=800,
                    title_text="多行多列子图制作")
    return fig


def plot_hitmap():
    data = np.arange(2000).reshape(40,50)
    fig = px.imshow(data,color_continuous_scale="gray",title="R(m)")  # 参数设置
    return fig

def save_fig_to_json(fig,path):
    json_str = fig.to_json()
    dic = json.loads(json_str)
    print(type(dic))
    with open(path,"w") as f:
        json.dump(dic,f)



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




def plot_equilibrium():
    
    loc = locals()
    with open("/Users/lianke/Desktop/plotly_code/ids.json","r") as f:
        data = json.load(f)

    gfile_data = {}
    exec(f'rleft = data{PathBuilter.for_data("equilibrium/time_slice(itime)/boundary/b_flux_pol_norm")}')
    rleft = loc["rleft"]
    exec(f'rdim = data{PathBuilter.for_data("equilibrium/grids_ggd(itime)/grid(i1)/space(i2)/objects_per_dimension(i3)/object(i4)/measure")}')
    rdim = loc["rdim"]
    nw = 129
    nh = 129
    exec(f'zmid = data{PathBuilter.for_data("equilibrium/time_slice(itime)/boundary/geometric_axis/z")}')
    zmid = loc["zmid"]

    exec(f'zdim = data{PathBuilter.for_data("equilibrium/time_slice(itime)/boundary/psi")}')
    zdim = loc["zdim"]
    print(f'psirz = data{PathBuilter.for_data("equilibrium/time_slice(itime)/profiles_2d(i1)/psi")}')
    exec(f'psirz = data{PathBuilter.for_data("equilibrium/time_slice(itime)/profiles_2d(i1)/psi")}')
    psirz = loc["psirz"]
    exec(f'simag = data{PathBuilter.for_data("equilibrium/time_slice(itime)/global_quantities/psi_axis")}')
    simag = loc["simag"]
    exec(f'sibry = data{PathBuilter.for_data("equilibrium/time_slice(itime)/global_quantities/psi_boundary")}')
    sibry = loc["sibry"]

    gfile_data["rgefit"] = np.linspace(rleft,rleft+rdim,nw)
    gfile_data["zgefit"] = np.linspace(zmid-zdim/2,zmid+zdim/2,nw)
    gfile_data["psirz"] = np.mat(psirz).reshape(nw,nh)

    gfile_data["ssimag"] = simag
    gfile_data["ssibry"] = sibry




    x = gfile_data['rgefit']
    y = gfile_data['zgefit']

    z = (gfile_data['psirz'] - gfile_data['ssimag']) / (gfile_data['ssibry'] - gfile_data['ssimag']) 



    fig = go.Figure(data=go.Contour(z=z,x=x,y=y,
                    ncontours=30,
                    contours_coloring="lines"))
   
    
    fig.update_layout(width=600,height=800)

    return fig


def animation():
    
    loc = locals()
    with open("/Users/lianke/Desktop/plotly_code/ids.json","r") as f:
        data = json.load(f)

    gfile_data = {}
    exec(f'rleft = data{PathBuilter.for_data("equilibrium/time_slice(itime)/boundary/b_flux_pol_norm")}')
    rleft = loc["rleft"]
    exec(f'rdim = data{PathBuilter.for_data("equilibrium/grids_ggd(itime)/grid(i1)/space(i2)/objects_per_dimension(i3)/object(i4)/measure")}')
    rdim = loc["rdim"]
    nw = 129
    nh = 129
    exec(f'zmid = data{PathBuilter.for_data("equilibrium/time_slice(itime)/boundary/geometric_axis/z")}')
    zmid = loc["zmid"]

    exec(f'zdim = data{PathBuilter.for_data("equilibrium/time_slice(itime)/boundary/psi")}')
    zdim = loc["zdim"]
    print(f'psirz = data{PathBuilter.for_data("equilibrium/time_slice(itime)/profiles_2d(i1)/psi")}')
    exec(f'psirz = data{PathBuilter.for_data("equilibrium/time_slice(itime)/profiles_2d(i1)/psi")}')
    psirz = loc["psirz"]
    exec(f'simag = data{PathBuilter.for_data("equilibrium/time_slice(itime)/global_quantities/psi_axis")}')
    simag = loc["simag"]
    exec(f'sibry = data{PathBuilter.for_data("equilibrium/time_slice(itime)/global_quantities/psi_boundary")}')
    sibry = loc["sibry"]

    gfile_data["rgefit"] = np.linspace(rleft,rleft+rdim,nw)
    gfile_data["zgefit"] = np.linspace(zmid-zdim/2,zmid+zdim/2,nw)
    gfile_data["psirz"] = np.mat(psirz).reshape(nw,nh)

    gfile_data["ssimag"] = simag
    gfile_data["ssibry"] = sibry

    x = gfile_data['rgefit']
    y = gfile_data['zgefit']

    z = (gfile_data['psirz'] - gfile_data['ssimag']) / (gfile_data['ssibry'] - gfile_data['ssimag']) 


    fig = go.Figure(
    data=[go.Contour(x=x, y=y,z=z,ncontours=10,contours_coloring="lines")],
    layout=go.Layout(
        xaxis=dict(range=[1,3], autorange=False),
        yaxis=dict(range=[-3, 3], autorange=False),
        title="Start Title",
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Play",
                          method="animate",
                          args=[None])])]
    ),
    frames=[go.Frame(data=[go.Contour(x=x, y=y,z=z,ncontours=10,contours_coloring="lines")]),
            go.Frame(data=[go.Contour(x=x, y=y,z=z,ncontours=11,contours_coloring="lines")]),
            go.Frame(data=[go.Contour(x=x, y=y,z=z,ncontours=12,contours_coloring="lines")]),
            go.Frame(data=[go.Contour(x=x, y=y,z=z,ncontours=13,contours_coloring="lines")]),
            go.Frame(data=[go.Contour(x=x, y=y,z=z,ncontours=14,contours_coloring="lines")]),
            go.Frame(data=[go.Contour(x=x, y=y,z=z,ncontours=15,contours_coloring="lines")]),
            go.Frame(data=[go.Contour(x=x, y=y,z=z,ncontours=16,contours_coloring="lines")]),
            go.Frame(data=[go.Contour(x=x, y=y,z=z,ncontours=17,contours_coloring="lines")]),
            go.Frame(data=[go.Contour(x=x, y=y,z=z,ncontours=18,contours_coloring="lines")]),
                     ]
)
    fig.update_layout(height=300,width=400)
    return fig

if __name__=="__main__":
    path = "plot.json"
    fig = plot_equilibrium()
    save_fig_to_json(fig,path)
    fig.show()

    # fig = 
    # fig.show()
  



