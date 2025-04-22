#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from matplotlib.animation import FuncAnimation
from fargo3dplot import *
import os 
import fnmatch
#%%
direct = '/home/sareh/IPMWorkshop/fargo3d/outputs/KH/'  # change this address to where your outputs are

#%% ======================================
#   this section of script plots a single outputh with number nout    
#==========================================
nout = 13
fig, ax = plt.subplots(figsize=(7,6), ncols=2, nrows=2, sharex=True, sharey=True)

grid = Grid(direct)
z = grid.zmid
y = grid.ymid

# Get the point from the points list at index i
dens = ReadField(directory=direct, name='dens', nout=nout)
pressure = ReadField(directory=direct, name='press', nout=nout)
vz = ReadField(directory=direct, name='vz', nout=nout)
vy = ReadField(directory=direct, name='vy', nout=nout)
p0 = ax[0,0].pcolormesh(y,z, dens.field); plt.colorbar(p0)
p1 = ax[0,1].pcolormesh(y,z, pressure.field); plt.colorbar(p1)
p2 = ax[1,0].pcolormesh(y,z, vz.field); plt.colorbar(p2)
p3 = ax[1,1].pcolormesh(y,z, vy.field); plt.colorbar(p3)
ax[0,0].set(xlim=[0,4], ylim=[0,1], ylabel=r'$z$', title=r'$\rho$')
ax[1,0].set(xlabel=r'$y$', ylabel=r'$z$', title=r'$v_z$')
ax[1,1].set(xlabel=r'$y$', title=r'$v_y$')
ax[0,1].set_title(r'$P$')
fig.suptitle(f'time={dens.time}')


#%% =========================================
# The below section makes an animation of your outputs
#===========================================
#Pause toggle
is_paused = False
fig, ax = plt.subplots(figsize=(7,6), ncols=2, nrows=2, sharex=True, sharey=True)
def on_key(event):
    global is_paused
    if event.key == ' ':
        is_paused = not is_paused
    elif event.key == 'escape':
        plt.close()

fig.canvas.mpl_connect('key_press_event', on_key)
grid = Grid(direct)
z = grid.zmid
y = grid.ymid
nfinal = len(fnmatch.filter(os.listdir(direct), 'gasdens*.dat'))-1
nout  = 0
# Get the point from the points list at index i
dens = ReadField(directory=direct, name='dens', nout=nout)
pressure = ReadField(directory=direct, name='press', nout=nout)
vz = ReadField(directory=direct, name='vz', nout=nout)
vy = ReadField(directory=direct, name='vy', nout=nout)
p0 = ax[0,0].pcolormesh(y,z, dens.field, vmin=0, vmax=3)
p1 = ax[0,1].pcolormesh(y,z, pressure.field, vmin=0, vmax=0.5 )
p2 = ax[1,0].pcolormesh(y,z, vz.field, vmin=-1, vmax=1)
p3 = ax[1,1].pcolormesh(y,z, vy.field, vmin=-2, vmax=2)
plt.colorbar(p0)
plt.colorbar(p1)
plt.colorbar(p2)
plt.colorbar(p3)
ax[0,0].set(xlim=[0,4], ylim=[0,1], ylabel=r'$z$', title=r'$\rho$')
ax[1,0].set(xlabel=r'$y$', ylabel=r'$z$', title=r'$v_z$')
ax[1,1].set(xlabel=r'$y$', title=r'$v_y$')
ax[0,1].set_title(r'$P$')
fig.suptitle(f'time={dens.time}')


def animate(nout):
    if not is_paused:
        for i in range(2):
            for j in range(2):
                ax[i,j].clear() 
        # Get the point from the points list at index i
        dens = ReadField(directory=direct, name='dens', nout=nout)
        pressure = ReadField(directory=direct, name='press', nout=nout)
        vz = ReadField(directory=direct, name='vz', nout=nout)
        vy = ReadField(directory=direct, name='vy', nout=nout)
        p0 = ax[0,0].pcolormesh(y,z, dens.field, vmin=0, vmax=3)
        p1 = ax[0,1].pcolormesh(y,z, pressure.field, vmin=0, vmax=0.5 )
        p2 = ax[1,0].pcolormesh(y,z, vz.field, vmin=-1, vmax=1)
        p3 = ax[1,1].pcolormesh(y,z, vy.field, vmin=-2, vmax=2)

        fig.suptitle(f'time={dens.time}')
        ax[0,0].set(xlim=[0,4], ylim=[0,1], ylabel=r'$z$', title=r'$\rho$')
        ax[1,0].set(xlabel=r'$y$', ylabel=r'$z$', title=r'$v_z$')
        ax[1,1].set(xlabel=r'$y$', title=r'$v_y$')
        ax[0,1].set_title(r'$P$')

ani = FuncAnimation(fig, animate, frames=nfinal, interval=200, repeat=True)
#ani.save(filename=direct+"KH.mkv", writer="ffmpeg")


