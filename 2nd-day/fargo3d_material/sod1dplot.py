#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from matplotlib.animation import FuncAnimation
from fargo3dplot import *
import os 
import fnmatch
#%%
# Sod shock tube analytical solution (from Toro's book, simplified)
def exact_sod_solution(x, t, x0=0.5, gamma=1.4):
    from scipy.optimize import fsolve
    # Initial states
    rho_L, u_L, P_L = 1.0, 0.0, 1.0
    rho_R, u_R, P_R = 0.125, 0.0, 0.1

    # Sound speeds
    c_L = np.sqrt(gamma * P_L / rho_L)
    c_R = np.sqrt(gamma * P_R / rho_R)

    # Function to solve for P_star (pressure in the star region)
    def f(P):
        if P < P_L:  # rarefaction
            A_L = 2 / ((gamma + 1) * rho_L)
            B_L = (gamma - 1) / (gamma + 1) * P_L
            f_L = (2 * c_L / (gamma - 1)) * ((P / P_L) ** ((gamma - 1) / (2 * gamma)) - 1)
        else:  # shock
            A_L = 2 / ((gamma + 1) * rho_L)
            B_L = (gamma - 1) / (gamma + 1) * P_L
            f_L = (P - P_L) * np.sqrt(A_L / (P + B_L))
        
        if P < P_R:  # rarefaction
            A_R = 2 / ((gamma + 1) * rho_R)
            B_R = (gamma - 1) / (gamma + 1) * P_R
            f_R = (2 * c_R / (gamma - 1)) * ((P / P_R) ** ((gamma - 1) / (2 * gamma)) - 1)
        else:  # shock
            A_R = 2 / ((gamma + 1) * rho_R)
            B_R = (gamma - 1) / (gamma + 1) * P_R
            f_R = (P - P_R) * np.sqrt(A_R / (P + B_R))
        
        return f_L + f_R + (u_R - u_L)

    # Solve for P_star
    P_star = fsolve(f, 0.5)[0]

    # Compute u_star
    if P_star < P_L:
        f_L = (2 * c_L / (gamma - 1)) * ((P_star / P_L) ** ((gamma - 1) / (2 * gamma)) - 1)
    else:
        A_L = 2 / ((gamma + 1) * rho_L)
        B_L = (gamma - 1) / (gamma + 1) * P_L
        f_L = (P_star - P_L) * np.sqrt(A_L / (P_star + B_L))
    
    u_star = u_L - f_L

    # Compute density in star regions
    if P_star < P_L:
        rho_L_star = rho_L * (P_star / P_L) ** (1 / gamma)
    else:
        rho_L_star = rho_L * ((P_star / P_L + (gamma - 1) / (gamma + 1)) / ((gamma - 1) / (gamma + 1) * P_star / P_L + 1))

    if P_star < P_R:
        rho_R_star = rho_R * (P_star / P_R) ** (1 / gamma)
    else:
        rho_R_star = rho_R * ((P_star / P_R + (gamma - 1) / (gamma + 1)) / ((gamma - 1) / (gamma + 1) * P_star / P_R + 1))

    # Rarefaction fan edges
    c_star = c_L * (P_star / P_L) ** ((gamma - 1) / (2 * gamma))
    x_head = x0 - c_L * t
    x_tail = x0 + (u_star - c_star) * t
    x_contact = x0 + u_star * t

    # Shock speed
    S = x0 + t * np.sqrt((P_star - P_R) * (gamma + 1) / (2 * gamma * P_R) + (gamma - 1) / (2 * gamma)) * np.sign(u_star)

    # Allocate output
    rho = np.zeros_like(x)
    u = np.zeros_like(x)
    P = np.zeros_like(x)

    for i in range(len(x)):
        xi = x[i]
        if xi < x_head:
            rho[i] = rho_L
            u[i] = u_L
            P[i] = P_L
        elif xi < x_tail:
            u[i] = (2 / (gamma + 1)) * (c_L + (xi - x0) / t)
            c = c_L - (gamma - 1) / 2 * u[i]
            rho[i] = rho_L * (c / c_L) ** (2 / (gamma - 1))
            P[i] = P_L * (c / c_L) ** (2 * gamma / (gamma - 1))
        elif xi < x_contact:
            rho[i] = rho_L_star
            u[i] = u_star
            P[i] = P_star
        elif xi < S:
            rho[i] = rho_R_star
            u[i] = u_star
            P[i] = P_star
        else:
            rho[i] = rho_R
            u[i] = u_R
            P[i] = P_R

    return rho, u, P

#%%========================================================================

direct = '/home/sareh/IPMWorkshop/fargo3d/outputs/sod1d/'  # change this address to where your outputs are


fig, ax = plt.subplots(figsize=(5,7), ncols=1, nrows=3, sharex=True, sharey=True)


nfinal = len(fnmatch.filter(os.listdir(direct), 'gasdens*.dat'))-1
grid = Grid(direct)
x = grid.zmid

# The initial output
dens = ReadField(directory=direct, name='dens', nout=0)
pressure = ReadField(directory=direct, name='press', nout=0)
vz = ReadField(directory=direct, name='vz', nout=0)
p0 = ax[0].plot(x, dens.field, c='tab:blue')
p1 = ax[1].plot(x, pressure.field, c='tab:red')
p2 = ax[2].plot(x, vz.field, c='tab:green')
ax[2].set(xlim=[0,1], ylim=[0,1.01], xlabel='x', ylabel=r'$v$')
ax[0].set_title(f'time={dens.time}')
ax[1].set_ylabel(r'$P$')
ax[0].set_ylabel(r'$\rho$')
#

# Pause toggle
is_paused = False

def on_key(event):
    global is_paused
    if event.key == ' ':
        is_paused = not is_paused
    elif event.key == 'escape':
        plt.close()

fig.canvas.mpl_connect('key_press_event', on_key)

def animate(nout):
    if not is_paused:
        for i in range(3):
            ax[i].clear()
        # Get the point from the points list at index i
        dens = ReadField(directory=direct, name='dens', nout=nout)
        pressure = ReadField(directory=direct, name='press', nout=nout)
        vz = ReadField(directory=direct, name='vz', nout=nout)
        ax[0].plot(x, dens.field, c=p0[0].get_color())
        ax[1].plot(x, pressure.field, c=p1[0].get_color())
        ax[2].plot(x, vz.field, c=p2[0].get_color())
        ax[2].set(xlim=[0,1], ylim=[0,1.01], xlabel='x', ylabel=r'$v$')
        ax[1].set_ylabel(r'$P$')
        ax[0].set_ylabel(r'$\rho$')
        ax[0].set_title(f'time={dens.time}')
        rho, u, P = exact_sod_solution(x, dens.time)
        ax[0].plot(x, rho, c=p0[0].get_color(), ls='--')
        ax[1].plot(x, P, c=p1[0].get_color(), ls='--')
        ax[2].plot(x, u, c=p2[0].get_color(), ls='--')

ani = FuncAnimation(fig, animate, frames=nfinal, interval=500, repeat=True)
#ani.save(filename=direct+"sod1d.mkv", writer="ffmpeg")


