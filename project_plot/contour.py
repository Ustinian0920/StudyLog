import matplotlib.pyplot as plt
import numpy as np
import random
r1 = np.linspace(-5,-3,50)
r2 = np.linspace(-3,-1,40)
r3 = np.linspace(-1,1,30)
r4 = np.linspace(1,3,40)
r5 = np.linspace(3,5,50)
r = np.hstack((r1,r2,r3,r4,r5))


z1 = np.linspace(-3,-2,50)
z2 = np.linspace(-2,-1,40)
z3 = np.linspace(-1,1,30)
z4 = np.linspace(1,2,40)
z5 = np.linspace(2,3,50)
z = np.hstack((z1,z2,z3,z4,z5))

R,Z = np.meshgrid(r,z)
P = (R+random.uniform(-1,1))**2+(Z+random.uniform(-1,1))**2+random.uniform(-1,1)

print(type(R[0][0]))

def plot_background():
    fig = plt.figure(figsize=(10.4,6.08),dpi=100)
    plt.subplots_adjust(top = 0.98, bottom = 0, right = 1, left = 0, hspace=0.5,wspace=0.28)
    plt.margins(0,0)
    ax1 = plt.subplot2grid((58,128),(0,10),rowspan=53,colspan=38)
    ax2 = plt.subplot2grid((58,128),(4,70),rowspan=9,colspan=49)
    ax3 = plt.subplot2grid((58,128),(14,70),rowspan=9,colspan=49)
    ax4 = plt.subplot2grid((58,128),(24,70),rowspan=9,colspan=49)
    ax5 = plt.subplot2grid((58,128),(34,70),rowspan=9,colspan=49)
    ax6 = plt.subplot2grid((58,128),(44,70),rowspan=9,colspan=49)
    axs = [ax1,ax2,ax3,ax4,ax5,ax5,ax6]
    for ax in axs[1:-1]:
        ax.set_xticklabels(["1"],color="white")

def plot_contour(ax1):
    ax1.contour(R,Z,P,np.linspace(0,0.05,5),colors="red")
    ax1.contour(R,Z,P,np.linspace(0.5,4,6),colors="#fed631")
    ax1.contour(R,Z,P,np.linspace(4,6,7),colors="#3dfffe")
    ax1.contour(R,Z,P,[4],colors="red")
    ax1.contour(R,Z,P,np.linspace(6,52,20),colors="#fed631")

def plot_waveform():
    fig = None
    axs = []
    return fig,axs

def plot_overlay(axs):
    return axs

def plot_param(axs):
    return axs

# ax1.contour(X,Y,Z)
# ax1.contour(X,Y,Z)
# ax1.contour(X,Y,Z)

plt.show()

