import numpy as np
import math
import matplotlib.pyplot as plt
from pathlib import Path
from sw_viewer_tools import read_R_Z

g_draw = "2A"

pi = math.pi
digifaw_font_path = "/Users/lianke/Desktop/swf/input/digifaw.ttf"

R_Z = read_R_Z()


afile_data_list = []
for i in range(10):
    afile_data_list.append({
        "rout":i,
        "aout":i,
        "eout":i,
        "doutu":i,
        "doutl":i
        } 
    )

max_afile_data_list = []
for i in range(20):
    max_afile_data_list.append({
        "rout":i,
        "aout":i,
        "eout":i,
        "doutu":i,
        "doutl":i
        } 
    )

json_data = {
    "Yact":list(range(10)),
    "X":list(range(10))
}

max_json_data = {
    "Yact":list(range(20)),
    "X":list(range(20))
}

time_list = list(range(10))
max_time_list = list(range(20))
shot = 36000
time = 10

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
    

# 读取单个Gfile
def read_g(gfile_path):
    # info = get_sw_path_info()
    # sw_framework_root = info['sw_framework_root']
    # if not sw_framework_root in sys.path:
    #     sys.path.append(sw_framework_root)
        
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

#——----------------------------大屏------------------------------------------------


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
    ax1.set_xlabel('R(m)', fontsize=font_size-2,color="white")
    ax1.set_ylabel('Z(m)', fontsize=font_size-2,color="white")
    
    return ax1

def screen_Draw_2A_stru_bg(ax1):

   
    # 线条透明度
    alpha = 0.9
    # y轴label的字体大小
    font_size = 18
    # xy轴刻度值的字体大小
    tick_size = 12


    ## 真空室 VV ## 绿圈
    X1=[1.070 ,1.840 ,2.310 ,2.310, 1.840, 1.070, 1.070]
    X2=[1.095, 1.815, 2.270 ,2.270 ,1.815,1.095 ,1.095]
    Y1=[1.215, 1.215 ,0.436 ,-0.436, -1.215, -1.215 ,1.215]
    Y2=[1.185 ,1.185 ,0.430, -0.430 ,-1.185, -1.185 ,1.185]
    ax1.plot(X1,Y1,'lime',X2,Y2,'lime')
    ## 欧姆线圈 E ## 紫色方块
    def rect_E(r,z,w,h):
        r1=r-w/2
        r2=r+w/2
        z1=z-h/2
        z2=z+h/2
        R=[r1,r2,r2,r1,r1,r2,r1,r2]
        Z=[z1,z1,z2,z2,z1,z2,z2,z1]
        ax1.plot(R,Z,'violet')#紫色方块 violet

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
    ## 极向场线圈  ## 蓝色方块
    def rect_E1(r,z,w,h):
        r1=r-w/2
        r2=r+w/2
        z1=z-h/2
        z2=z+h/2
        R=[r1,r2,r2,r1,r1,r2,r1,r2]
        Z=[z1,z1,z2,z2,z1,z2,z2,z1]
        ax1.plot(R,Z,'c') #蓝色方块
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
    ax1.set_yticklabels([-2,-1.5,-1.0,-0.5,0.0,0.5,1.0,1.5],fontsize=tick_size)
    ax1.set_xticklabels([1.0,1.0,1.5,2.0,2.5],fontsize=tick_size)
    ax1.set_xlabel('R(m)', fontsize=font_size-2,color="white")
    ax1.set_ylabel('Z(m)', fontsize=font_size-2,color="white")

    return ax1
    ## 初始化结束 ##

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
    bottom_xlim = min(max_time_list)
    top_xlim = max(max_time_list)
    
    btw_xlim = top_xlim-bottom_xlim
    
    y_tick = [float(f%bottom_ylim),float(f%mid_ylim),float(f%top_ylim)]
    
   
    
    ax6.plot(time_list,y["d"],col,linewidth=line_width)
    ax6.set_ylim(bottom_ylim-btw_ylim*0.05,top_ylim+btw_ylim*0.05)
    
    ax6.set_xlim(max_time_list[0],max_time_list[-1])
    ax6.set_ylabel(ax6_lb,color="white",fontsize=font_size)
    ax6.set_xlabel("Time(ms)",color="white",fontsize=font_size-2)
  
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
    bottom_xlim = min(max_time_list)
    top_xlim = max(max_time_list)
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
    ax2.set_ylabel(ax2_lb,color="white",fontsize=font_size-3)
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
    
    bottom_xlim = min(max_time_list)
    top_xlim = max(max_time_list)
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
    ax3.set_ylabel(ax3_lb,color="white",fontsize=font_size-2)
    ax3.set_xticks(x_tick)
    ax3.set_xticklabels(x_tick,color="#000105")
    ax3.set_yticks(y_tick)
    y_tick = [float(f%(bottom_ylim/100)),float(f%(mid_ylim/100)),float(f%(top_ylim/100))]
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
    ax4.set_ylabel(ax4_lb,color="white",fontsize=font_size-2)
    ax4.set_xticks(x_tick)
    ax4.set_xticklabels(x_tick,color="#000105")
    ax4.set_yticks(y_tick)
    y_tick = [float(f%(bottom_ylim/100)),float(f%(mid_ylim/100)),float(f%(top_ylim/100))]
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
    ax5.set_ylabel(ax5_lb,color="white",fontsize=font_size)
    ax5.set_xticks(x_tick)
    ax5.set_xticklabels(x_tick,color="#000105")
    ax5.set_yticks(y_tick)
    y_tick = [float(f%(bottom_ylim)),float(f%(mid_ylim)),float(f%(top_ylim))]
    ax5.set_yticklabels(y_tick,fontsize=tick_size)
    ax5.grid(True,color="#00FFFB",linestyle='--',alpha=grid_alpha)

fig = plt.figure(figsize=(10.4,6.08),dpi=100)#10.4
plt.subplots_adjust(top = 0.98, bottom = 0, right = 1, left = 0, hspace=0.5,wspace=0.28)
plt.margins(0,0)
ax1 = plt.subplot2grid((58,128),(0,10),rowspan=53,colspan=38)
ax2 = plt.subplot2grid((58,128),(4,70),rowspan=9,colspan=49)#54 46
ax3 = plt.subplot2grid((58,128),(14,70),rowspan=9,colspan=49)# 49
ax4 = plt.subplot2grid((58,128),(24,70),rowspan=9,colspan=49)
ax5 = plt.subplot2grid((58,128),(34,70),rowspan=9,colspan=49)
ax6 = plt.subplot2grid((58,128),(44,70),rowspan=9,colspan=49)

# # 颜色设置
axs = [ax1,ax2,ax3,ax4,ax5,ax6]
def set_color(fig,c_border,c_tick,c_bg):
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
        

# 修改背景颜色
plt.rcParams['axes.facecolor']='#000105'

c_border = "#00FFFB"#0591ff
c_tick = "#00FFFB"
c_bg = "#000105"
set_color(fig,c_border,c_tick,c_bg)




if __name__ == "__main__":
    gfile_data = read_g("/Users/lianke/Desktop/swf/036000/00310/g036000.00310")
    if g_draw=="2A":
        screen_Draw_2A_stru_bg(ax1)
    else:
        screen_Draw_2M_stru_bg(ax1,R_Z)
    screen_draw_psi_fig(ax1,gfile_data,g_draw,"12311")
    screen_draw_prof(ax2,ax3,ax4,ax5,ax6,json_data,max_json_data,afile_data_list,max_afile_data_list,time_list,max_time_list,shot,time,False)
    plt.show()