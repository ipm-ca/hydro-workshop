#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from matplotlib.animation import FuncAnimation
from fargo3dplot import *
import os 
import fnmatch
#%%
direct = '/home/sareh/IPMWorkshop/fargo3d/outputs/gjup/'  # change this address to where your outputs are

#%% ======================================
#   this section of script plots a single outputh with number nout    
#==========================================
nout = 1
fig, ax = plt.subplots()

grid = Grid(direct)
x = grid.xmid
y = grid.ymid

PlotField(directory=direct, field='dens', nout=nout, fig=fig, ax=ax,  perturbation=True,\
          settitle=True, vmin=-0.3, vmax=0.3, cmap='bwr')


#%% =========================================
# The below section makes an animation of your outputs
#===========================================
#Pause toggle
is_paused = False
fig, ax = plt.subplots()
left, bottom, width, hight = ax.get_position().bounds

def on_key(event):
    global is_paused
    if event.key == ' ':
        is_paused = not is_paused
    elif event.key == 'escape':
        plt.close()

fig.canvas.mpl_connect('key_press_event', on_key)

grid = Grid(direct)
x = grid.xmid
y = grid.ymid
     
nfinal = len(fnmatch.filter(os.listdir(direct), 'gasdens*.dat'))-1
PlotField(directory=direct, field='dens', nout=0, fig=fig, ax=ax,  perturbation=True,\
          settitle=True, vmin=-0.3, vmax=0.3, cmap='bwr')

def animate(nout):
    if not is_paused:
        fig.clf()
        ax = fig.add_axes([left, bottom, width, hight])
        # Get the point from the points list at index i
        PlotField(directory=direct, field='dens', nout=nout, fig=fig, ax=ax,  perturbation=True,\
                  settitle=True, vmin=-0.3, vmax=0.3, cmap='bwr')


ani = FuncAnimation(fig, animate, frames=nfinal, interval=200, repeat=True)
#ani.save(filename=direct+"KH.mkv", writer="ffmpeg")


